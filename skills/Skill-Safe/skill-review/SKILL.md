---
name: skill-review
description: Review MCP servers and agent skills for security risks before installation or execution. Scans for malware, spyware, backdoors, crypto-mining, data exfiltration, persistence mechanisms, and malicious code patterns, then returns an approved/caution/reject verdict.
---

# Skill Review

Security audit workflow for MCP servers and skill folders.

## Use this skill when
- A user asks to review or audit an MCP server or skill for safety.
- A user wants malware, spyware, backdoor, or crypto-mining detection before install.
- A user wants a quick security verdict (`approved`, `caution`, `reject`) with evidence.

## Capabilities
- Scan skill folders for security threats
- Detect data exfiltration patterns
- Identify system modification attempts
- Catch crypto-mining indicators
- Flag arbitrary code execution risks
- Find backdoors and obfuscation techniques
- Output reports in Markdown under each skill

## Workflow
1. Identify the target path (skill folder, MCP repo, or config folder).
2. Run the scanner:
```bash
python3 skills/Skill-Safe/skill-review/scripts/skill_review.py <target-path>
```
3. JSON output (for automation):
```bash
python3 skills/Skill-Safe/skill-review/scripts/skill_review.py <target-path> --json
```
4. Save report:
```bash
python3 skills/Skill-Safe/skill-review/scripts/skill_review.py <target-path> --output security-report.md
```
5. Save Markdown directly under the scanned skill folder:
```bash
python3 skills/Skill-Safe/skill-review/scripts/skill_review.py <target-path> --output-under-skill
```
This writes `<target-path>/skill-review-report.md`.
6. Interpret the verdict:
- `approved`: no high-risk indicators found.
- `caution`: suspicious behavior found; needs manual review.
- `reject`: critical malicious indicators found; block by default.

## Notes
- This is static, pattern-based analysis. False positives and false negatives are possible.
- Treat `critical` findings as block-by-default unless the behavior is explicitly justified.
- Re-run after every significant change to scripts, configs, or dependencies.
