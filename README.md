# Deepak Puligilla — IT Support & Automation Portfolio

Practical Python projects exploring workstation troubleshooting and helpdesk reporting. Based in Adelaide, South Australia; seeking IT support, service desk and junior automation opportunities.

| Project | Purpose | Skills |
| --- | --- | --- |
| [IT Support Toolkit](it-support-toolkit) | Disk-space diagnostics, optional DNS checks, HTML and JSON reports | Python, troubleshooting, reporting, tests |
| [Helpdesk Ticket Analyzer](helpdesk-ticket-analyzer) | Validate ticket CSV exports and summarise urgent backlog | Python, data validation, CSV automation, tests |
| [File Organizer](file-organizer) | Preview and sort files into categories without replacing existing files | Python, filesystem operations, error handling, tests |
| [Stock Alert Automation](stock-alert-automation) | Flag low inventory and calculate suggested replenishment | Python, business rules, CSV validation, HTML/JSON reports |

## Run the demos

Requires Python 3.10 or newer. No third-party packages are required.

```bash
cd it-support-toolkit
python support_check.py
python -m unittest discover -s tests -v
```

Open `reports/report.html` in a browser. For the second project, from the repository root:

```bash
cd helpdesk-ticket-analyzer
python analyze.py examples/tickets.csv
python -m unittest discover -s tests -v
```

The sample tickets are fictional. Expected result: 6 tickets and 2 high/critical unresolved tickets.

## Project status

Initial working versions developed with AI assistance. The first two projects previously passed CI on Windows and Linux. The two new projects add 19 tests and have passed local Linux tests and demo commands. The CI workflow now covers all four projects on Windows and Linux. These are personal portfolio demonstrations, not production deployments.

Read each project's README for design choices, limitations and planned improvements.

[Prepared profile README](docs/profile-README.md)

## New project demos

```bash
cd file-organizer
python -c "import shutil; shutil.copytree('examples/inbox', 'demo-inbox')"
python organizer.py demo-inbox
python organizer.py demo-inbox --apply
```

From the repository root, run the stock demo:

```bash
cd stock-alert-automation
python stock_alert.py examples/inventory.csv
```

Open `reports/stock-alerts.html`. Each project's README walks through the code, demo results, limitations and an extension exercise.
