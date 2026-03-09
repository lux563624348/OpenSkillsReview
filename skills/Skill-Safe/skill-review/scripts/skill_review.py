#!/usr/bin/env python3
"""
Skill Review - Security scanner for MCP servers and agent skills.

Scans folders for malware, spyware, backdoors, crypto-mining, and
other malicious code patterns.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".bat",
    ".cmd",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".pl",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
}
SPECIAL_FILENAMES = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Makefile",
    "Procfile",
}
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    description: str
    recommendation: str
    regex: str
    extensions: Optional[Sequence[str]] = None


@dataclass
class Finding:
    rule_id: str
    severity: str
    description: str
    recommendation: str
    file_path: str
    line_number: int
    line_content: str


@dataclass
class ScanSummary:
    target_path: str
    scan_timestamp: str
    files_scanned: int = 0
    files_skipped: int = 0
    total_lines: int = 0
    findings: List[Finding] = field(default_factory=list)
    verdict: str = "approved"
    verdict_reason: str = ""


RULES: Sequence[Rule] = (
    Rule(
        rule_id="reverse_shell",
        severity="critical",
        description="Potential reverse shell or remote command channel.",
        recommendation="Reject unless there is a documented, legitimate admin-only use case.",
        regex=r"/dev/tcp/|nc\s+-e|ncat\s+.*--exec|bash\s+-i\s+>&|pty\.spawn\(|socat\s+.*tcp",
        extensions=(".py", ".sh", ".bash", ".zsh", ".js", ".ts"),
    ),
    Rule(
        rule_id="download_and_execute",
        severity="critical",
        description="Downloads remote content and executes it directly.",
        recommendation="Reject. Replace with pinned artifacts and signature/hash verification.",
        regex=(
            r"(curl|wget)\s+[^|;\n]*\|\s*(bash|sh)\b|"
            r"(Invoke-WebRequest|iwr|irm)[^;\n]*(iex|Invoke-Expression)"
        ),
        extensions=(".sh", ".bash", ".zsh", ".ps1", ".cmd", ".bat", ".py"),
    ),
    Rule(
        rule_id="crypto_mining_indicator",
        severity="critical",
        description="Cryptocurrency mining indicator detected.",
        recommendation="Reject. This is a strong cryptojacking indicator.",
        regex=r"xmrig|ethminer|cpuminer|cgminer|minerd|stratum\+tcp|mining[_\-\s]?pool|hashrate",
    ),
    Rule(
        rule_id="persistence_modification",
        severity="critical",
        description="Attempts to create persistence via scheduler/service startup.",
        recommendation="Reject unless strictly required and explicitly approved.",
        regex=(
            r"crontab\s+-|/etc/cron|schtasks\s+/create|"
            r"systemctl\s+(enable|start)\b|/etc/systemd|launchctl\s+load\b|"
            r"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\b"
        ),
    ),
    Rule(
        rule_id="obfuscated_exec",
        severity="high",
        description="Potential obfuscated or encoded dynamic execution.",
        recommendation="Require code transparency and remove hidden execution flows.",
        regex=r"(base64\.b64decode|atob\s*\().*(eval|exec)|(eval|exec)\s*\([^)]*(base64|decode)",
        extensions=(".py", ".js", ".ts", ".mjs", ".cjs"),
    ),
    Rule(
        rule_id="dynamic_execution",
        severity="high",
        description="Dynamic code execution primitive.",
        recommendation="Avoid dynamic execution or prove all inputs are trusted and static.",
        regex=r"\beval\s*\(|\bexec\s*\(|new\s+Function\s*\(|Function\s*\(",
        extensions=(".py", ".js", ".ts", ".mjs", ".cjs"),
    ),
    Rule(
        rule_id="mcp_suspicious_command",
        severity="high",
        description="Suspicious MCP launch command in config.",
        recommendation="Validate command source and pin to trusted local binaries only.",
        regex=r'"command"\s*:\s*"[^"]*(curl|wget|powershell|cmd(\.exe)?|bash\s+-c|sh\s+-c)[^"]*"',
        extensions=(".json", ".yaml", ".yml", ".toml"),
    ),
    Rule(
        rule_id="keylogging_or_surveillance",
        severity="high",
        description="Possible keylogging, screenshot, or surveillance behavior.",
        recommendation="Reject unless this behavior is explicit, user-consented, and documented.",
        regex=r"pynput|keyboard\.hook|GetAsyncKeyState|CGEventTapCreate|pyautogui\.screenshot|mss\(",
    ),
    Rule(
        rule_id="bulk_secret_access",
        severity="high",
        description="Broad access to environment variables or secrets.",
        recommendation="Limit to specific keys and document why each secret is required.",
        regex=r"dict\(os\.environ\)|os\.environ\.items\(|for\s+\w+\s+in\s+os\.environ|process\.env",
        extensions=(".py", ".js", ".ts"),
    ),
    Rule(
        rule_id="sensitive_path_access",
        severity="high",
        description="References sensitive credential/key locations.",
        recommendation="Reject or require strict justification and least-privilege handling.",
        regex=r"~/.ssh|id_rsa|id_ed25519|\.aws/credentials|\.git-credentials|/etc/shadow|keychain",
    ),
    Rule(
        rule_id="unsafe_subprocess_shell",
        severity="medium",
        description="Spawns shell commands with shell=True.",
        recommendation="Prefer argument arrays and avoid shell interpolation.",
        regex=r"subprocess\.(run|Popen|call)\([^)]*shell\s*=\s*True",
        extensions=(".py",),
    ),
    Rule(
        rule_id="external_post_exfiltration",
        severity="medium",
        description="Outbound POST request pattern that may exfiltrate data.",
        recommendation="Review endpoints and payload contents for least-data transmission.",
        regex=r"(requests|httpx|axios)\.post\s*\(|fetch\s*\([^)]*method\s*:\s*['\"]POST['\"]|curl\s+[^;\n]*\s(-d|--data)\s",
    ),
    Rule(
        rule_id="unsafe_runtime_flags",
        severity="medium",
        description="Potentially unsafe runtime flags found.",
        recommendation="Remove permissive flags or document strict containment controls.",
        regex=r"--dangerously-skip-permissions|--allow-all|--disable-sandbox|--unsafe|--no-sandbox",
    ),
    Rule(
        rule_id="large_encoded_blob",
        severity="medium",
        description="Large encoded blob may indicate hidden payload.",
        recommendation="Inspect decoded content and justify why embedding is required.",
        regex=r"[A-Za-z0-9+/]{180,}={0,2}",
    ),
)


def compile_rules() -> List[tuple[Rule, re.Pattern[str]]]:
    return [(rule, re.compile(rule.regex, re.IGNORECASE)) for rule in RULES]


def should_scan_file(path: Path) -> bool:
    if path.name in SPECIAL_FILENAMES:
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    return False


def is_probably_binary(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            sample = fh.read(4096)
    except OSError:
        return True
    if b"\x00" in sample:
        return True
    return False


def walk_targets(target: Path) -> Iterable[Path]:
    if target.is_file():
        yield target
        return
    for root, dirnames, filenames in os_walk(target):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            yield root / name


def os_walk(target: Path):
    import os

    for root, dirs, files in os.walk(target):
        yield Path(root), dirs, files


def scan_target(target: Path, max_file_size: int) -> ScanSummary:
    summary = ScanSummary(
        target_path=str(target.resolve()),
        scan_timestamp=datetime.now(timezone.utc).isoformat(),
    )
    compiled = compile_rules()

    for file_path in walk_targets(target):
        if not file_path.is_file():
            continue
        if not should_scan_file(file_path):
            summary.files_skipped += 1
            continue
        try:
            if file_path.stat().st_size > max_file_size:
                summary.files_skipped += 1
                continue
        except OSError:
            summary.files_skipped += 1
            continue
        if is_probably_binary(file_path):
            summary.files_skipped += 1
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            summary.files_skipped += 1
            continue

        if target.is_dir():
            try:
                rel_path = str(file_path.relative_to(target))
            except ValueError:
                rel_path = str(file_path)
        else:
            rel_path = file_path.name
        lines = content.splitlines()
        summary.files_scanned += 1
        summary.total_lines += len(lines)

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if (
                stripped.startswith("regex=")
                or '"pattern":' in stripped
                or "'pattern':" in stripped
                or (
                    (stripped.startswith('r"') or stripped.startswith("r'"))
                    and ("|" in stripped or r"\s" in stripped)
                )
            ):
                continue
            for rule, pattern in compiled:
                if rule.extensions and file_path.suffix.lower() not in rule.extensions:
                    continue
                if pattern.search(line):
                    summary.findings.append(
                        Finding(
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            description=rule.description,
                            recommendation=rule.recommendation,
                            file_path=rel_path,
                            line_number=idx,
                            line_content=line.strip()[:240],
                        )
                    )
    determine_verdict(summary)
    return summary


def determine_verdict(summary: ScanSummary) -> None:
    severity_counts = count_by_severity(summary.findings)
    critical = severity_counts.get("critical", 0)
    high = severity_counts.get("high", 0)
    medium = severity_counts.get("medium", 0)

    if critical > 0 or high >= 3:
        summary.verdict = "reject"
        summary.verdict_reason = (
            f"Detected {critical} critical and {high} high severity findings."
        )
    elif high > 0 or medium > 0:
        summary.verdict = "caution"
        summary.verdict_reason = (
            f"Detected {high} high and {medium} medium severity findings."
        )
    else:
        summary.verdict = "approved"
        summary.verdict_reason = "No critical/high/medium findings detected."


def count_by_severity(findings: Sequence[Finding]) -> Dict[str, int]:
    counts: Dict[str, int] = {key: 0 for key in SEVERITY_ORDER}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    return counts


def findings_sorted(findings: Sequence[Finding]) -> List[Finding]:
    return sorted(
        findings,
        key=lambda f: (
            -SEVERITY_ORDER.get(f.severity, -1),
            f.file_path.lower(),
            f.line_number,
            f.rule_id,
        ),
    )


def to_json(summary: ScanSummary) -> str:
    payload = {
        "target_path": summary.target_path,
        "scan_timestamp": summary.scan_timestamp,
        "files_scanned": summary.files_scanned,
        "files_skipped": summary.files_skipped,
        "total_lines": summary.total_lines,
        "verdict": summary.verdict,
        "verdict_reason": summary.verdict_reason,
        "severity_counts": count_by_severity(summary.findings),
        "findings": [asdict(finding) for finding in findings_sorted(summary.findings)],
    }
    return json.dumps(payload, indent=2)


def to_markdown(summary: ScanSummary) -> str:
    severity_counts = count_by_severity(summary.findings)
    lines: List[str] = [
        "# Skill Review Security Report",
        "",
        f"- **Scan timestamp (UTC):** {summary.scan_timestamp}",
        f"- **Target path:** `{summary.target_path}`",
        "",
        "## Verdict",
        "",
        f"**{summary.verdict.upper()}** - {summary.verdict_reason}",
        "",
        "## Scan Summary",
        "",
        f"- **Files scanned:** {summary.files_scanned}",
        f"- **Files skipped:** {summary.files_skipped}",
        f"- **Total lines scanned:** {summary.total_lines}",
        f"- **Findings:** {len(summary.findings)}",
        f"- **Critical:** {severity_counts.get('critical', 0)}",
        f"- **High:** {severity_counts.get('high', 0)}",
        f"- **Medium:** {severity_counts.get('medium', 0)}",
        f"- **Low:** {severity_counts.get('low', 0)}",
        "",
        "## Findings",
        "",
    ]
    sorted_findings = findings_sorted(summary.findings)
    if not sorted_findings:
        lines.append("No suspicious patterns detected.")
        return "\n".join(lines)

    for finding in sorted_findings:
        lines.extend(
            [
                f"### {finding.rule_id} ({finding.severity})",
                f"- **File:** `{finding.file_path}`:{finding.line_number}",
                f"- **Description:** {finding.description}",
                f"- **Recommendation:** {finding.recommendation}",
                f"- **Snippet:** `{finding.line_content}`",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Security review scanner for MCP servers and skills."
    )
    parser.add_argument("target_path", help="Path to skill folder, MCP repo, or config file.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON report instead of Markdown.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write report to file. Default: stdout.",
    )
    parser.add_argument(
        "--output-under-skill",
        action="store_true",
        help="Write Markdown report to <target>/skill-review-report.md (directory targets only).",
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=1_500_000,
        help="Skip files larger than this many bytes (default: 1500000).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    target = Path(args.target_path)
    if not target.exists():
        print(f"Error: target path not found: {target}", file=sys.stderr)
        return 2
    if args.output_under_skill and args.json:
        print("Error: --output-under-skill cannot be used with --json.", file=sys.stderr)
        return 2
    if args.output_under_skill and target.is_file():
        print("Error: --output-under-skill requires a directory target.", file=sys.stderr)
        return 2

    summary = scan_target(target, max_file_size=args.max_file_size)
    output = to_json(summary) if args.json else to_markdown(summary)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    elif args.output_under_skill:
        report_path = target / "skill-review-report.md"
        report_path.write_text(output, encoding="utf-8")
        print(f"Markdown report written to {report_path}")
    else:
        print(output)

    if summary.verdict == "reject":
        return 2
    if summary.verdict == "caution":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
