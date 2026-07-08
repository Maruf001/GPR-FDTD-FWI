# Experiment 883: Local 2D Source-Factor Full-Factorial Design Contract

Date: 2026-06-25

## Purpose

Revise the source-factor isolation design after run `169` showed that the
six-variant run `167` contract was not a full three-factor isolation.

The corrected design covers all combinations of time shift, amplitude scale,
and frequency/source scale for the two sensitive variable-radius cases.

This is a design contract only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/170_local_2d_source_factor_full_factorial_design_contract
```

Key artifacts:

```text
data/local_2d_source_factor_full_factorial_design_rows.csv
data/local_2d_source_factor_full_factorial_gates.csv
data/local_2d_source_factor_full_factorial_design_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_FULL_FACTORIAL_DESIGN_CONTRACT.md
figures/local_2d_source_factor_full_factorial_design_contract.png
scripts/run_local_2d_source_factor_full_factorial_design_contract.py
scripts/test_local_2d_source_factor_full_factorial_design_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitive cases:                         2
design rows:                             16
variant count per case:                  8
gate count:                              5
cached pair-observed design rows:        5
cached available design rows:            7
required counterfactual design rows:     9
new variant rows added after audit:      4
time-factor rows:                        8
amplitude-factor rows:                   8
frequency-factor rows:                   8
full-factorial design ready:             true
observed signature covered:              true
CPU execution contract ready:            true
cached execution ready:                  false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Interpretation

The revised design closes the run `169` design gap by using all eight
source-factor combinations:

```text
nominal_replay
time_shift_only
amplitude_only
frequency_only
time_amplitude_only
time_frequency_only
amplitude_frequency_only
combined_observed
```

Seven case-variant rows have cached inputs available: two nominal baselines and
five pair-delta signatures. Nine case-variant rows still require new
counterfactual diagnostics before this can be treated as an executed isolation
experiment.

## Decision

Use this as the executable source-factor isolation contract. Keep cached
execution, new FDTD, GPU work, field transfer, broad source robustness, and
time-zero-only explanation blocked until the required counterfactual diagnostics
exist and pass.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_full_factorial_design_contract.py
sha256: 5ef15ddc921bc3236ab763c7aecf17222aaed35274b114d25fc555d5e83169cb

test_local_2d_source_factor_full_factorial_design_contract.py
sha256: f13a7829c876fb8635c5e401e4d0f49da6456c7a8da96728158da826d599a1f3
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_full_factorial_design_contract.py
3 passed
```

Figure check:

```text
local_2d_source_factor_full_factorial_design_contract.png
1780x771, dynamic range=255
```
