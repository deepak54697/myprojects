"""Summarise a helpdesk CSV without copying ticket descriptions or requester data."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED = {'ticket_id', 'status', 'priority', 'category'}
STATUSES = {'open', 'in progress', 'resolved', 'closed'}
PRIORITIES = {'low', 'medium', 'high', 'critical'}


def summarize(path):
    counts = {key: Counter() for key in ('status', 'priority', 'category')}
    seen = set()
    urgent = 0
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError('CSV must include: ' + ', '.join(sorted(REQUIRED)))
        for line, row in enumerate(reader, start=2):
            if None in row or any(not (row.get(key) or '').strip() for key in REQUIRED):
                raise ValueError(f'Invalid or missing values on CSV row {line}')
            ticket_id = row['ticket_id'].strip()
            if ticket_id in seen:
                raise ValueError(f'Duplicate ticket ID on CSV row {line}')
            status, priority = row['status'].strip().lower(), row['priority'].strip().lower()
            if status not in STATUSES or priority not in PRIORITIES:
                raise ValueError(f'Unknown status or priority on CSV row {line}')
            seen.add(ticket_id)
            category = row['category'].strip().lower()
            for key, value in [('status', status), ('priority', priority), ('category', category)]:
                counts[key][value] += 1
            urgent += int(status in {'open', 'in progress'} and priority in {'high', 'critical'})
    return {'total_tickets': len(seen), 'urgent_unresolved': urgent,
            'counts': {key: dict(sorted(value.items())) for key, value in counts.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--output', type=Path, default=Path('reports'))
    args = parser.parse_args()
    try:
        report = summarize(args.csv_file)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(2, f'Could not analyze tickets: {exc}\n')
    print(f"Total tickets: {report['total_tickets']}")
    print(f"High/critical unresolved: {report['urgent_unresolved']}")
    for category, count in report['counts']['category'].items():
        print(f'  {category}: {count}')
    print(f'Summary saved to {args.output.resolve()}')


if __name__ == '__main__':
    main()
