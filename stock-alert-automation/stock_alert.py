"""Generate low-stock reports from a validated CSV export. Python 3.10+."""
import argparse
import csv
import html
import json
from pathlib import Path

REQUIRED = {'sku', 'name', 'quantity', 'reorder_point', 'target_stock'}


def analyze_inventory(path):
    alerts, seen = [], set()
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or not REQUIRED.issubset(headers):
            raise ValueError('CSV needs unique headers including: ' + ', '.join(sorted(REQUIRED)))
        for line, row in enumerate(reader, start=2):
            if None in row or any(not (row.get(key) or '').strip() for key in REQUIRED):
                raise ValueError(f'Invalid or missing values on row {line}')
            sku, name = row['sku'].strip(), row['name'].strip()
            if sku.casefold() in seen:
                raise ValueError(f'Duplicate SKU on row {line}')
            seen.add(sku.casefold())
            numbers = {}
            for key in ['quantity', 'reorder_point', 'target_stock']:
                value = row[key].strip()
                if not value.isascii() or not value.isdecimal():
                    raise ValueError(f'{key} must be a non-negative whole number on row {line}')
                numbers[key] = int(value)
            if numbers['target_stock'] < numbers['reorder_point']:
                raise ValueError(f'target_stock must be at least reorder_point on row {line}')
            quantity = numbers['quantity']
            if quantity <= numbers['reorder_point']:
                alerts.append({'sku': sku, 'name': name, **numbers,
                               'status': 'out_of_stock' if quantity == 0 else 'low_stock',
                               'suggested_order': max(0, numbers['target_stock'] - quantity)})
    alerts.sort(key=lambda item: (item['quantity'] != 0, item['quantity'], item['sku']))
    return {'products_checked': len(seen), 'alert_count': len(alerts), 'alerts': alerts}


def render_html(report):
    escape = lambda value: html.escape(str(value))
    rows = ''.join('<tr>' + ''.join(f'<td>{escape(item[key])}</td>' for key in
                   ['sku', 'name', 'quantity', 'reorder_point', 'suggested_order', 'status']) + '</tr>'
                   for item in report['alerts'])
    if not rows:
        rows = '<tr><td colspan="6">No products are at or below their reorder point.</td></tr>'
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Stock alerts</title>
<style>body{{font:16px system-ui;margin:32px;background:#eef3f8;color:#172b46}}
main{{max-width:1000px;margin:auto}}header,section{{background:white;padding:24px;border-radius:14px;margin-bottom:20px}}
section{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #dde4ed}}</style>
<main><header><small>DEEPAK PULIGILLA · AUTOMATION PORTFOLIO</small><h1>Inventory stock alerts</h1>
<p>{report['products_checked']} products checked · {report['alert_count']} alerts</p></header>
<section><table><thead><tr><th>SKU</th><th>Product</th><th>On hand</th><th>Reorder point</th><th>Suggested order</th><th>Status</th></tr></thead>
<tbody>{rows}</tbody></table></section><p>Recommendations only. Confirm stock counts and pending deliveries before ordering.</p></main></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory', type=Path)
    parser.add_argument('--output', type=Path, default=Path('reports'))
    args = parser.parse_args()
    try:
        report = analyze_inventory(args.inventory)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'stock-alerts.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        (args.output / 'stock-alerts.html').write_text(render_html(report), encoding='utf-8')
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(2, f'Cannot generate stock alerts: {exc}\n')
    print(f"Checked {report['products_checked']} products; {report['alert_count']} alerts")
    for item in report['alerts']:
        print(f"{item['sku']}: {item['status']} — suggested order {item['suggested_order']}")
    print(f'Reports: {args.output.resolve()}')


if __name__ == '__main__':
    main()
