from __future__ import annotations

import re
from pathlib import Path


BASE_RULEPACK: list[dict] = [
    {
        "id": "DG-BASE-001",
        "title": "Avoid tx.origin authorization",
        "severity": "HIGH",
        "description": "Detects tx.origin in authorization logic.",
        "pattern": r"tx\.origin",
    },
    {
        "id": "DG-BASE-002",
        "title": "Unchecked low-level call",
        "severity": "HIGH",
        "description": "Detects low-level .call usage that may be unchecked.",
        "pattern": r"\.call\s*\{",
    },
    {
        "id": "DG-BASE-003",
        "title": "Missing access control markers",
        "severity": "MED",
        "description": "Detects external/public mutating functions without likely access-control modifiers.",
        "pattern": r"function\s+[A-Za-z0-9_]+\s*\([^)]*\)\s*(?:external|public)(?![^\n;{]*\b(onlyOwner|onlyRole|auth|governance)\b)",
    },
    {
        "id": "DG-BASE-004",
        "title": "Unsafe delegatecall",
        "severity": "HIGH",
        "description": "Detects delegatecall usage.",
        "pattern": r"delegatecall\s*\(",
    },
    {
        "id": "DG-BASE-005",
        "title": "Block timestamp dependence",
        "severity": "MED",
        "description": "Detects block.timestamp usage in logic.",
        "pattern": r"block\.timestamp",
    },
    {
        "id": "DG-BASE-006",
        "title": "Unsafe arithmetic context",
        "severity": "LOW",
        "description": "Detects explicit unchecked arithmetic blocks.",
        "pattern": r"unchecked\s*\{",
    },
    {
        "id": "DG-BASE-007",
        "title": "Unbounded loops",
        "severity": "MED",
        "description": "Detects loops over dynamic array lengths that may cause gas issues.",
        "pattern": r"for\s*\([^)]*;\s*[^;]*\.length",
    },
    {
        "id": "DG-BASE-008",
        "title": "Hardcoded critical addresses",
        "severity": "LOW",
        "description": "Detects hardcoded 0x addresses in contracts.",
        "pattern": r"0x[a-fA-F0-9]{40}",
    },
    {
        "id": "DG-BASE-009",
        "title": "Missing reentrancy guard markers",
        "severity": "MED",
        "description": "External payable function without obvious nonReentrant marker.",
        "pattern": r"function\s+[A-Za-z0-9_]+\s*\([^)]*\)\s*(?:external|public)[^\n{;]*\bpayable\b(?![^\n;{]*\bnonReentrant\b)",
    },
    {
        "id": "DG-BASE-010",
        "title": "Deprecated selfdestruct usage",
        "severity": "LOW",
        "description": "Detects selfdestruct/deprecated teardown patterns.",
        "pattern": r"\bselfdestruct\s*\(",
    },
]


def _iter_solidity_files(target_path: str):
    root = Path(target_path)
    if root.is_file() and root.suffix == ".sol":
        yield root
        return
    for path in root.rglob("*.sol"):
        if path.is_file():
            yield path


def apply_base_rules(target_path: str, chain: str = "base") -> list[dict]:
    findings: list[dict] = []
    if chain.lower() != "base":
        return findings

    compiled_rules = [
        {**rule, "_regex": re.compile(rule["pattern"], re.MULTILINE)} for rule in BASE_RULEPACK
    ]

    for file_path in _iter_solidity_files(target_path):
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        for rule in compiled_rules:
            for match in rule["_regex"].finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append(
                    {
                        "id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": rule["description"],
                        "file": str(file_path),
                        "line": line,
                        "chain": chain,
                        "source": "DriftGuard",
                    }
                )

    return findings
