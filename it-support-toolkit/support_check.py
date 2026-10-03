"""Read-only support diagnostics. Python 3.10+, standard library only."""
import argparse
import html
import json
import platform
import shutil
import socket
from datetime import datetime, timezone
from pathlib import Path


def disk_status(free, total, threshold=15):
    if total <= 0:
        raise ValueError('Disk total must be positive')
    percentage = round(free / total * 100, 1)
    return {'status': 'warning' if percentage < threshold else 'pass',
            'free_percent': percentage, 'free_gib': round(free / 1024**3, 2),
            'total_gib': round(total / 1024**3, 2)}


def dns_check(target):
    try:
        socket.getaddrinfo(target, None)
        return {'status': 'pass', 'message': 'DNS resolution succeeded'}
    except socket.gaierror:
        return {'status': 'warning', 'message': 'DNS resolution failed; check spelling, network and DNS settings'}


def collect(disk_path, threshold, dns_target=None):
    usage = shutil.disk_usage(disk_path)
    checks = {'disk': disk_status(usage.free, usage.total, threshold)}
    if dns_target:
        checks['dns'] = dns_check(dns_target)
    return {'schema_version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'system': {'os': platform.system(), 'release': platform.release(),
                       'architecture': platform.machine(), 'python': platform.python_version()},
            'checks': checks}


def render_html(report):
    escape = lambda value: html.escape(str(value))
    sections = []
    for name, values in report['checks'].items():
        rows = ''.join(f'<tr><th>{escape(k)}</th><td>{escape(v)}</td></tr>' for k, v in values.items())
        sections.append(f'<section><h2>{escape(name.title())}</h2><table>{rows}</table></section>')
    system = ' · '.join(escape(v) for v in report['system'].values())
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IT Support Diagnostic Report</title><style>
body{{font:16px system-ui;background:#eef3f8;color:#172b46;margin:0;padding:32px}}
main{{max-width:850px;margin:auto}}header,section{{background:white;border-radius:14px;padding:24px;margin-bottom:18px}}
h1{{margin:8px 0}}p{{color:#50627b}}table{{border-collapse:collapse;width:100%}}
th,td{{padding:12px;text-align:left;border-bottom:1px solid #e6ecf2}}small{{color:#50627b}}
</style><main><header><small>DEEPAK PULIGILLA · PORTFOLIO PROJECT</small>
<h1>IT Support Diagnostic Report</h1><p>{system}</p><small>{escape(report['created_utc'])}</small></header>
{''.join(sections)}<p>Read-only checks. DNS success does not establish internet connectivity.
Review findings before taking any remedial action.</p></main></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disk-path', default=str(Path.cwd().anchor))
    parser.add_argument('--threshold', type=float, default=15, help='Warn below this free-space percentage')
    parser.add_argument('--dns', help='Optional hostname to resolve; makes a DNS request')
    parser.add_argument('--output', type=Path, default=Path('reports'))
    args = parser.parse_args()
    if not 0 <= args.threshold <= 100:
        parser.error('--threshold must be between 0 and 100')
    if args.dns and (not args.dns.strip() or len(args.dns) > 253 or any(c.isspace() for c in args.dns)):
        parser.error('--dns must be a hostname without spaces')
    try:
        report = collect(args.disk_path, args.threshold, args.dns)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        (args.output / 'report.html').write_text(render_html(report), encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Diagnostics could not complete: {exc}\n')
    print(f"Reports saved to {args.output.resolve()}")
    print('Overall: ' + ('WARNING' if any(c['status'] == 'warning' for c in report['checks'].values()) else 'PASS'))


if __name__ == '__main__':
    main()
