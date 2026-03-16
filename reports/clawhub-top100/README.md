# ClawHub Top-100 Security Scan

We used Prism Scanner v0.1.0 to scan 100 randomly sampled code-containing skills from the [ClawHub skill repository](https://github.com/openclaw/skills) (`openclaw/skills`). 99 of 100 were successfully scanned; 1 was skipped due to a structural anomaly.

## Key Findings

- **42% of skills rated Danger (D) or Critical (F)**
- 1,474 total security findings, including 34 CRITICAL-level issues
- 38% have undeclared network access; 25% read environment variables (API keys, passwords)
- 2 skills attempt to install persistent backdoors
- 1 skill has a complete data exfiltration chain

## Contents

| File | Description |
|------|-------------|
| `ClawHub-Top100-Security-Report.md` | Full report with methodology, grade distribution, severity breakdown, top-10 riskiest skills, and recommendations |
| `_aggregate_stats.json` | Aggregate statistics (grade distribution, severity counts, rule hit counts, behavior tags) |
| `scans/*.json` | 99 individual scan results in Prism JSON format |

## How to Read Individual Reports

Each JSON file in `scans/` follows the Prism Scanner output schema:

```bash
# Re-scan any skill yourself
prism scan https://github.com/openclaw/skills/tree/main/skills/<author>/<skill>
```

## Methodology

See [ClawHub-Top100-Security-Report.md](ClawHub-Top100-Security-Report.md#0-methodology) for full details on sampling, scan configuration, and limitations.
