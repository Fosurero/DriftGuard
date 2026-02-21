from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from driftguard.hash_utils import compute_report_hash, compute_rulepack_hash
from driftguard.rules.base.rulepack import BASE_RULEPACK, apply_base_rules


def _ensure_prspec_on_path() -> None:
    current = Path(__file__).resolve()
    repo_root = current.parents[4]
    vendor_prspec = repo_root / "vendor" / "prspec"
    if vendor_prspec.exists() and vendor_prspec.is_dir():
        vendor_prspec_str = str(vendor_prspec)
        if vendor_prspec_str not in sys.path:
            sys.path.insert(0, vendor_prspec_str)


def _normalize_prspec_findings(raw: Any) -> list[dict]:
    if raw is None:
        return []

    if isinstance(raw, dict):
        for key in ("findings", "issues", "results"):
            if isinstance(raw.get(key), list):
                raw = raw[key]
                break
        else:
            raw = [raw]

    if not isinstance(raw, list):
        raw = [raw]

    normalized = []
    for finding in raw:
        if not isinstance(finding, dict):
            continue
        normalized.append(
            {
                "id": str(finding.get("id", finding.get("rule_id", "PRSPEC"))),
                "title": finding.get("title", finding.get("name", "PRSpec finding")),
                "severity": str(finding.get("severity", "MED")).upper(),
                "message": finding.get("message", finding.get("description", "")),
                "file": finding.get("file", finding.get("path", "")),
                "line": finding.get("line", finding.get("line_number", 0)),
                "source": "PRSpec",
            }
        )
    return normalized


def run_scan(target_path: str, chain: str = "base") -> dict:
    _ensure_prspec_on_path()

    prspec_findings: list[dict] = []
    prspec_available = False
    prspec_error = None
    try:
        from prspec.engine.api import scan_path

        prspec_available = True
        raw = scan_path(target_path)
        prspec_findings = _normalize_prspec_findings(raw)
    except Exception as exc:
        prspec_error = str(exc)

    driftguard_findings = apply_base_rules(target_path=target_path, chain=chain)
    findings = prspec_findings + driftguard_findings

    severity_counts = {"HIGH": 0, "MED": 0, "LOW": 0, "INFO": 0}
    for finding in findings:
        sev = str(finding.get("severity", "INFO")).upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    report: dict[str, Any] = {
        "target_path": target_path,
        "chain": chain,
        "findings": findings,
        "summary": {
            "total_findings": len(findings),
            "severity_counts": severity_counts,
            "prspec_available": prspec_available,
        },
        "rulepack_hash": compute_rulepack_hash(BASE_RULEPACK),
        "metadata": {
            "rulepack_size": len(BASE_RULEPACK),
            "prspec_error": prspec_error,
        },
    }

    report_without_hash = json.loads(json.dumps(report, sort_keys=True))
    report["report_hash"] = compute_report_hash(report_without_hash)
    return report
