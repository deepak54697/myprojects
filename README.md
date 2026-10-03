# Deepak Puligilla — IT Support & Automation Portfolio

Practical Python projects exploring workstation troubleshooting and helpdesk reporting. Based in Adelaide, South Australia; seeking IT support, service desk and junior automation opportunities.

| Project | Purpose | Skills |
| --- | --- | --- |
| [IT Support Toolkit](it-support-toolkit) | Disk-space diagnostics, optional DNS checks, HTML and JSON reports | Python, troubleshooting, reporting, tests |
| [Helpdesk Ticket Analyzer](helpdesk-ticket-analyzer) | Validate ticket CSV exports and summarise urgent backlog | Python, data validation, CSV automation, tests |

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

Initial working versions developed with AI assistance. Twelve unit tests and both demo commands passed in Linux during development. These are personal portfolio demonstrations, not production deployments. Windows validation is pending; the CI workflow is configured to test both Windows and Linux.

Read each project's README for design choices, limitations and planned improvements.

[Prepared profile README](docs/profile-README.md)
