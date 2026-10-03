# IT Support Toolkit

A Python command-line tool that gathers basic workstation diagnostics and turns them into a readable HTML report and structured JSON output.

Built as a portfolio project by **Deepak Puligilla**, focused on IT support and automation opportunities in Adelaide. Developed with AI assistance; this is a demonstration project, not a deployed enterprise product.

## The problem

A support ticket often starts with limited information. A repeatable check helps a technician identify low disk space and record basic operating-system details before investigating further.

## Features

- Operating-system, architecture and Python-version summary.
- Disk-space check with a configurable warning threshold.
- Optional DNS resolution check for a specified hostname.
- JSON output for other tools and an HTML report for support handover.
- Standard-library implementation: no external Python packages.
- Read-only system checks, with no automatic repairs.

## Quick start

Requires Python 3.10 or newer. Download this repository and open a terminal in its folder.

```bash
python support_check.py
```

Open `reports/report.html` in your browser. On systems where Python is named `python3`, use that command instead.

```bash
python support_check.py --threshold 20 --output reports
python support_check.py --disk-path .
python support_check.py --dns example.com
python -m unittest discover -s tests -v
```

The DNS check is opt-in and sends a DNS request through your configured resolver. Default checks do not collect usernames, hostnames, IP addresses or serial numbers. Reports still reveal OS details; review before sharing. Repeated runs overwrite reports in the selected output folder.

## Example

Open [the synthetic example report](examples/report.html), or inspect [the sample JSON](examples/report.json). These samples use fictional values and do not describe a real device.

## Design choices

Diagnostics, presentation and CLI handling are separate functions. JSON includes a schema version to support future consumers. HTML escapes report values, and tests cover warning boundaries, failed DNS resolution and HTML escaping.

## Limitations and validation

This is an initial version: no RAM, event-log, service or installed-software checks. A DNS result does not establish internet access or prove that a service is available. DNS duration depends on the system resolver. Disk checks target one filesystem at a time. Warnings are findings, not diagnoses.

Tests and a CLI smoke test were run in Linux during development. The included GitHub Actions workflow is configured for Windows and Linux, but its hosted runs and testing on a physical Windows workstation remain outstanding.

## Next improvements

- Validate on a Windows workstation and record results.
- Add a support ticket summary and remediation guidance.
- Add opt-in Windows event-log checks with personal data redaction.

## Interview discussion

Be ready to explain disk threshold calculations, DNS limitations, why checks are read-only, JSON versus HTML, error handling and the HTML-escaping test. Run the tool yourself and extend a feature before claiming independent implementation experience.
