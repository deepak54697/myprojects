# Helpdesk Ticket Analyzer

A Python automation project that turns a helpdesk CSV export into ticket counts, category trends and a high-priority unresolved count.

Created as a portfolio demonstration for **Deepak Puligilla**, with AI assistance. Uses synthetic data; it is not connected to a workplace ticketing system.

## Why it exists

Support teams need a quick overview of their queue. This tool automates basic counting while validating input, rather than quietly producing misleading totals from duplicate IDs or invalid statuses.

## Run it

Requires Python 3.10+. No external packages.

```bash
python analyze.py examples/tickets.csv
python -m unittest discover -s tests -v
```

Expected sample result: **6 tickets**, **2 high/critical unresolved tickets**. Full results are saved to `reports/summary.json`; rerunning overwrites that file. Use `python3` if that is your system's Python command.

## CSV contract

Required columns: `ticket_id`, `status`, `priority`, `category`.

- Status: `open`, `in progress`, `resolved`, `closed`.
- Priority: `low`, `medium`, `high`, `critical`.
- Status, priority and category are trimmed and lowercased.
- IDs must be non-empty and unique; ID matching is case-sensitive.
- Missing columns, missing values, extra unnamed fields and invalid statuses/priorities stop processing with an error.
- Additional named columns are ignored, including requester names and descriptions.

An unresolved urgent ticket means status open/in progress AND priority high/critical. This is a demonstration rule, not an SLA calculation. Output retains category labels, so avoid putting personal information in categories. Do not commit real workplace exports.

## What this demonstrates

CSV handling, validation, aggregation with `Counter`, JSON reporting, automated tests and translating a support workflow into code.

## Validation and limitations

Tests and the sample command were run in Linux. This tool has no dashboard, API integration, date filtering or SLA tracking yet. Empty input with valid headers produces zero counts. Tests cover duplicates, missing data, invalid statuses and urgent-ticket classification.

## Next improvements

Add date filtering, a chart and configurable mappings for different ticket systems. Run and modify the code yourself before describing it in interviews; explain why resolved high-priority tickets do not count as urgent backlog.
