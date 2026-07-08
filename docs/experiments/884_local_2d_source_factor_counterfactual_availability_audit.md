# Experiment 884: Local 2D Source-Factor Counterfactual Availability Audit

Date: 2026-06-25

## Purpose

Check whether the nine required full-factorial counterfactual diagnostics from
run `170` can be reconstructed from existing cached optimizer artifacts.

This is an availability audit only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/172_local_2d_source_factor_counterfactual_availability_audit
```

Key artifacts:

```text
data/local_2d_source_factor_counterfactual_availability_rows.csv
data/local_2d_source_factor_counterfactual_availability_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_COUNTERFACTUAL_AVAILABILITY_AUDIT.md
figures/local_2d_source_factor_counterfactual_availability_audit.png
scripts/run_local_2d_source_factor_counterfactual_availability_audit.py
scripts/test_local_2d_source_factor_counterfactual_availability_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required counterfactual rows:            9
controlled counterfactuals in cache:     0
candidate profile proxy rows:            9
source-grid frequency supported rows:    9
source-grid time supported rows:         9
CPU backend available:                   true
no-fit-amplitude available:              true
source-frequency grid available:         true
source-time grid available:              true
replication-cases available:             true
existing runner controls ready:          true
cache reconstruction ready:              false
bounded CPU executor wrapper needed:     true
runner code extension needed:            false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Interpretation

The current cache does not contain controlled counterfactual diagnostics for the
nine missing source-factor rows. Candidate tables do contain source-profile
proxy matches, but those are fitted profile outputs, not controlled replication
cases.

The existing coordinate optimizer already exposes the controls needed for a
bounded CPU wrapper: `--backend cpu`, `--replication-cases`,
`--source-frequency-scales`, `--source-time-shift-ps-values`, and
`--no-fit-amplitude`.

## Decision

Build a bounded CPU executor wrapper around the existing coordinate optimizer
controls. Do not launch new FDTD, GPU work, field transfer, broad source
robustness, or time-zero-only explanation from the current cache.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_counterfactual_availability_audit.py
sha256: 287440fddbc083ba9d32bab10359278f3d1307b8e9f593d5dc5c7a97bcc416ff

test_local_2d_source_factor_counterfactual_availability_audit.py
sha256: d13020d6238bec2d385b10e1667f09a8f1cbee3f3434580bf3151b9211b73096
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_counterfactual_availability_audit.py
4 passed
```

Figure check:

```text
local_2d_source_factor_counterfactual_availability_audit.png
1420x772, dynamic range=255
```
