# DriftGuard

**Grant-ready security scanner for Base: PR-focused, deterministic, and attestable onchain.**

## Problem on Base
- Smart contract risks still enter pull requests before audits or deployment gates run.
- Security feedback is often inconsistent between contributors, reviewers, and CI systems.
- Teams need verifiable evidence of what was scanned and which ruleset version produced the result.

## What DriftGuard does
- Runs automated PR scanning with optional PRSpec engine integration and Base-focused checks.
- Produces deterministic `rulepack_hash` and `report_hash` values for reproducible security reporting.
- Supports onchain report attestation via `DriftGuardRegistry` on Base.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
driftguard scan examples/vulnerable --chain base --format md
```

## GitHub Action usage
This repo includes `.github/workflows/driftguard.yml` that runs on `pull_request` and uploads `driftguard_report.md` as an artifact.

If you want PR comments, add repository permissions and uncomment/extend the TODO section in the workflow.

## Onchain attestation
DriftGuard computes:
- `rulepack_hash`: deterministic hash of sorted Base rule definitions.
- `report_hash`: deterministic hash of the final scan JSON output.

Deploy and verify flow:
1. Build and test contract artifacts with Foundry.
2. Deploy `DriftGuardRegistry` with a configured `RULEPACK_HASH` and set version metadata.
3. Verify contract source on BaseScan using Foundry verification flags and your API key.

Commented broadcast examples:
```bash
# export PRIVATE_KEY=0x...
# export RPC_URL=https://mainnet.base.org
# export RULEPACK_HASH=0x...
# cd contracts
# forge script script/Deploy.s.sol:Deploy --rpc-url "$RPC_URL" --broadcast

# Optional source verification command pattern:
# forge verify-contract <DEPLOYED_ADDRESS> src/DriftGuardRegistry.sol:DriftGuardRegistry \
#   --chain-id 8453 --watch --etherscan-api-key "$BASESCAN_API_KEY"
```

## Demo output snippet
```md
# DriftGuard Report

- Target: examples/vulnerable
- Chain: base
- Findings: 4 (HIGH: 2, MED: 1, LOW: 1)
- rulepack_hash: keccak256:4c4a...f9e2
- report_hash: keccak256:0b16...d321

## Findings
| ID | Severity | Source | File | Message |
|---|---|---|---|---|
| DG-BASE-001 | HIGH | DriftGuard | examples/vulnerable/Example.sol | tx.origin usage detected |
```