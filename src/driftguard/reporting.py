from __future__ import annotations

import json


def report_to_json(report: dict) -> str:
    return json.dumps(report, indent=2, sort_keys=True)


def report_to_markdown(report: dict) -> str:
    summary = report.get("summary", {})
    counts = summary.get("severity_counts", {})
    findings = report.get("findings", [])
    lines = [
        "# DriftGuard Report",
        "",
        f"- Target: {report.get('target_path', '')}",
        f"- Chain: {report.get('chain', '')}",
        (
            "- Findings: "
            f"{summary.get('total_findings', 0)} "
            f"(HIGH: {counts.get('HIGH', 0)}, MED: {counts.get('MED', 0)}, LOW: {counts.get('LOW', 0)})"
        ),
        f"- rulepack_hash: {report.get('rulepack_hash', '')}",
        f"- report_hash: {report.get('report_hash', '')}",
        "",
        "## Findings",
        "| ID | Severity | Source | File | Line | Message |",
        "|---|---|---|---|---:|---|",
    ]

    for finding in findings:
        lines.append(
            "| {id} | {severity} | {source} | {file} | {line} | {message} |".format(
                id=finding.get("id", ""),
                severity=finding.get("severity", ""),
                source=finding.get("source", ""),
                file=finding.get("file", ""),
                line=finding.get("line", 0),
                message=str(finding.get("message", "")).replace("|", "\\|"),
            )
        )

    return "\n".join(lines) + "\n"
