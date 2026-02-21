from __future__ import annotations

import argparse
import sys

from driftguard.integration.prspec_engine import run_scan
from driftguard.reporting import report_to_json, report_to_markdown


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="driftguard")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a path for findings")
    scan_parser.add_argument("path", help="Target file or directory")
    scan_parser.add_argument("--chain", default="base", help="Target chain (default: base)")
    scan_parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format",
    )
    scan_parser.add_argument("--output", help="Optional output file path")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command != "scan":
        parser.error("Unsupported command")

    report = run_scan(target_path=args.path, chain=args.chain)
    rendered = report_to_markdown(report) if args.format == "md" else report_to_json(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    else:
        print(rendered)

    print(f"rulepack_hash: {report['rulepack_hash']}")
    print(f"report_hash: {report['report_hash']}")

    high_count = report.get("summary", {}).get("severity_counts", {}).get("HIGH", 0)
    if high_count > 0:
        raise SystemExit(2)

    raise SystemExit(0)


if __name__ == "__main__":
    main()
