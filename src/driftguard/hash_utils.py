from __future__ import annotations

import hashlib
import json
from typing import Any


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _select_hasher():
    try:
        from eth_hash.auto import keccak

        return "keccak256", lambda payload: keccak(payload).hex()
    except Exception:
        return "sha256", lambda payload: hashlib.sha256(payload).hexdigest()


def compute_rulepack_hash(rules: list[dict]) -> str:
    stable_rules = sorted(rules, key=lambda rule: str(rule.get("id", "")))
    payload = _canonical_json(stable_rules)
    algo, hasher = _select_hasher()
    return f"{algo}:{hasher(payload)}"


def compute_report_hash(report: dict) -> str:
    payload = _canonical_json(report)
    algo, hasher = _select_hasher()
    return f"{algo}:{hasher(payload)}"
