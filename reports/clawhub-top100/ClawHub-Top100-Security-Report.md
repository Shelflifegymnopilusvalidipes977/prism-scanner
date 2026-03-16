# ClawHub Skill Security Scan Report

**Scanner**: Prism Scanner v0.1.0
**Date**: 2026-03-16
**Total Findings**: 1,474 security findings across 99 skills

---

## 0. Methodology

### Data Source

This scan is based on the official ClawHub GitHub registry `openclaw/skills` (snapshot as of 2026-03-16).

### Sampling Process

1. **Total population**: The registry contains **7,605 skills** across approximately 10,400 author directories.
2. **Filter for code-containing skills**: We excluded prompt-only skills (those containing only `SKILL.md` / `README.md` with no executable code). Skills containing at least one code file (`.py`, `.js`, `.ts`, or `.sh`) were retained, yielding **3,440 code-containing skills**.
3. **Systematic sampling**: The 3,440 code-containing skills were sorted alphabetically, then sampled at equal intervals (every 34th skill), producing **100 evenly distributed samples** covering diverse authors and functional categories.
4. **Scan execution**: Of the 100 targets, 1 failed due to an anomalous directory structure that the scanner could not parse. **99 skills were successfully scanned**.

### Scan Configuration

- **Engines**: AST analysis + pattern matching + metadata analysis (3 layers, 38 detection rules)
- **Mode**: Offline (`--offline`) — no external threat intelligence services were queried
- **Average scan time**: < 1 second per skill

### Limitations

- This is a static code analysis. No dynamic sandbox analysis was performed; false positives and false negatives are possible.
- Sample coverage is approximately 2.9% (99 / 3,440). Statistical conclusions represent trends within the sample.
- Prompt-only skills (~4,165) were not included in this scan. Their primary risk vector is prompt injection, which requires separate evaluation.

---

## 1. Key Findings

- **42% of skills were rated "Danger" or "Critical"** (Grade D/F — 42 out of 99)
- **48% of skills were rated "Safe"** (Grade A — 48 out of 99)
- **34 CRITICAL-severity** findings were detected
- **1 skill** exhibited a confirmed data exfiltration chain (S8)
- **2 skills** attempted to install persistence mechanisms on the host system

---

## 2. Security Grade Distribution

| Grade | Meaning | Count | Percentage | Distribution |
|-------|---------|-------|------------|-------------|
| **A** | Safe | 48 | 48.5% | ████████████████████████ |
| **B** | Low Risk | 0 | 0.0% | |
| **C** | Caution | 9 | 9.1% | ████ |
| **D** | Danger | 23 | 23.2% | ███████████ |
| **F** | Critical | 19 | 19.2% | █████████ |

---

## 3. Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| CRITICAL | 34 | 2.3% |
| HIGH | 47 | 3.2% |
| MEDIUM | 1,292 | 87.7% |
| LOW | 101 | 6.9% |
| INFO | 0 | 0.0% |

---

## 4. Most Frequently Triggered Rules (Top 15)

| Rank | Rule ID | Hits | Description |
|------|---------|------|-------------|
| 1 | S4 | 1,152 | Outbound network requests |
| 2 | S5 | 148 | Environment variable access |
| 3 | S12 | 34 | Unsafe deserialization |
| 4 | P5 | 27 | Known malicious signatures |
| 5 | M1 | 22 | Capability baseline deviation |
| 6 | S1 | 19 | Shell command execution |
| 7 | P8 | 19 | Network IOC matches |
| 8 | S6 | 15 | Dynamic code execution (eval/exec) |
| 9 | S9 | 11 | SSRF detection |
| 10 | P7 | 7 | High-entropy strings |
| 11 | S13 | 5 | Persistence mechanisms |
| 12 | P4 | 4 | Hardcoded IPs / suspicious domains |
| 13 | P6 | 2 | Prompt injection patterns |
| 14 | P9 | 2 | Code obfuscation |
| 15 | S10 | 2 | Download-and-execute chains |

---

## 5. Behavior Tag Distribution

Prism Scanner assigns behavioral tags to each skill. The following shows tag frequency across all scanned skills:

| Behavior Tag | Count | Percentage |
|-------------|-------|------------|
| network_outbound | 38 | 38.4% |
| reads_env_vars | 25 | 25.3% |
| executes_shell | 9 | 9.1% |
| dynamic_execution | 6 | 6.1% |
| ssrf_risk | 5 | 5.1% |
| unsafe_deserialization | 4 | 4.0% |
| installs_persistence | 2 | 2.0% |
| uses_obfuscation | 1 | 1.0% |
| downloads_and_executes | 1 | 1.0% |
| exfiltrates_data | 1 | 1.0% |
| writes_system_files | 1 | 1.0% |

---

## 6. Top 10 Riskiest Skills

| Rank | Skill | Grade | CRITICAL | HIGH | MEDIUM | Total |
|------|-------|-------|----------|------|--------|-------|
| 1 | henrino3/heimdall | F | 12 | 5 | 8 | 25 |
| 2 | haiyangchenbj/invassistant | F | 4 | 1 | 170 | 179 |
| 3 | pitertxus/openclaw-memory-pensieve-algorand | F | 1 | 2 | 199 | 211 |
| 4 | johnjerry8749/weather-py | F | 2 | 1 | 80 | 85 |
| 5 | adlai88/polymarket-elon-tweets | F | 2 | 0 | 78 | 84 |
| 6 | xqw1377-prog/musk-insider-pro | F | 2 | 2 | 9 | 17 |
| 7 | larryfang/em-intel | F | 1 | 5 | 72 | 118 |
| 8 | cassh100k/soulkeeper | F | 1 | 2 | 24 | 28 |
| 9 | griffithkk3-del/lark-wiki-writer | F | 1 | 1 | 22 | 28 |
| 10 | jachian-lee/feishu-doc-reviewer | D | 0 | 1 | 119 | 122 |

---

## 7. Critical Risk Cases

### Data Exfiltration (S8)

The following skill was detected to have a complete source-to-sink data flow chain from sensitive data to a network egress point:

- `larryfang/em-intel`

### Persistence Mechanisms (S13)

The following skills were detected attempting to install persistent footholds on the host system:

- `cassh100k/soulkeeper`
- `henrino3/heimdall`

---

## 8. Findings-per-Skill Distribution

| Findings Range | Skill Count | Percentage |
|---------------|-------------|------------|
| 0 | 48 | 48.5% |
| 1–5 | 16 | 16.2% |
| 6–10 | 5 | 5.1% |
| 11–20 | 12 | 12.1% |
| 21–50 | 10 | 10.1% |
| 50+ | 8 | 8.1% |

---

## 9. Recommendations

### For Skill Developers

1. **Never hardcode credentials** — use environment variables or a secrets manager
2. **Declare all capabilities** — accurately list network, filesystem, and shell access in `SKILL.md`
3. **Scan before publishing** — `pip install prism-scanner && prism scan .`

### For ClawHub (Platform)

1. **Integrate Prism Scanner into the Skill publish pipeline** — similar to `npm audit`, automatically gate high-risk skills
2. **Conduct a full registry scan** — flag or delist Grade F skills
3. **Display security grades on Skill pages** — give users informed choice

### For Enterprise Users

1. **Deploy Prism Platform** — enable organization-wide Agent/Skill security governance
2. **Establish an approval workflow** — prevent employees from installing unvetted skills
3. **Schedule periodic re-scans** — defend against supply-chain poisoning attacks

---

## Appendix

### Tool Information

- **Prism Scanner v0.1.0** — open-source AI Agent security scanner
- **Repository**: https://github.com/aidongise-cell/prism-scanner
- **Install**: `pip install prism-scanner`
- **License**: Apache 2.0

### Detection Rule Coverage

| Layer | Rules | Count |
|-------|-------|-------|
| Layer 1 — Code Behavior Analysis | S1–S14 (AST) + P1–P9 (pattern matching) | 23 |
| Layer 2 — Metadata Analysis | M1–M6 (permissions / dependencies / author) | 5 |
| Layer 3 — Local Residue Scanning | R1–R10 (persistence / config pollution / credential residue) | 10 |
| **Total** | | **38** |

### Raw Data

All 99 individual JSON scan reports are archived in the `clawhub-scan-results/` directory for independent verification.

---

*This report was generated by Prism Scanner v0.1.0. Results are based on static code analysis and may contain false positives. For questions or false positive reports, please file a [GitHub Issue](https://github.com/aidongise-cell/prism-scanner/issues).*
