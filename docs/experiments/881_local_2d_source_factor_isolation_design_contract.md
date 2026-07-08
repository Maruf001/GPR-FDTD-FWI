# Experiment 881: Local 2D Source-Factor Isolation Design Contract

Date: 2026-06-25

## Purpose

Turn the two blocked variable-radius source/time-zero cases from run `160` into
a concrete next-experiment design.

Run `160` showed that broad variable-radius robustness is not ready, and that
the sensitive cases are not explained by time-zero shift alone. This run asks
what bounded follow-up is needed before any broader source robustness, FDTD, GPU,
or field-transfer claim.

This is cached design synthesis only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/167_local_2d_source_factor_isolation_design_contract
```

Key artifacts:

```text
data/local_2d_source_factor_isolation_design_rows.csv
data/local_2d_source_factor_isolation_gates.csv
data/local_2d_source_factor_isolation_design_contract_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_ISOLATION_DESIGN_CONTRACT.md
figures/local_2d_source_factor_isolation_design_contract.png
scripts/run_local_2d_source_factor_isolation_design_contract.py
scripts/test_local_2d_source_factor_isolation_design_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitive cases:                         2
design rows:                             12
variant count per case:                  6
gate count:                              4
time-factor rows:                        4
amplitude-factor rows:                   6
frequency-factor rows:                   6
general source/time-zero claim ready:    false
time-zero-only explanation ready:        false
CPU design ready:                        true
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The two sensitive cases are:

| Case | Run | Reference delta mm | Driver |
| --- | --- | ---: | --- |
| max amplitude stress | 233_coordinate_optimizer_variable_radius_location_only_seed21 | 5.0 | amplitude/frequency effect without time-shift observed |
| max geometry instability | 221_coordinate_optimizer_variable_radius_target_order_210_seed13 | 3.3541019662496847 | amplitude/frequency effect without time-shift observed |

Each sensitive case gets six variants:

```text
nominal_replay
time_shift_only
amplitude_only
frequency_only
amplitude_frequency_only
combined_observed
```

## Interpretation

The next local 2D source investigation should isolate time shift, amplitude
scale, and frequency/source scale in the two sensitive variable-radius cases.
This is the missing attribution step between the matched-pair result from run
`159`/`160` and any broader source robustness claim.

The design keeps the acceptance observable tied to matched geometry delta and
radius delta, with a 1 mm pass threshold. That prevents a broad robustness claim
from being promoted just because source perturbations were replayed.

## Decision

Use this run as the design contract for a future bounded CPU experiment. Keep
new FDTD, GPU work, field transfer, broad source robustness, and time-zero-only
explanation blocked until the factorial variants are executed and attributed.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_isolation_design_contract.py
sha256: 83a3119a412c2e3f31e41decf6424c89faf462b1796a846bca0962a11f943226

test_local_2d_source_factor_isolation_design_contract.py
sha256: 71e2ce0db3beca319a67544197e867960ed5d6e9f48a80937d278f7c9447fcca
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script, not by editing the frozen snapshot.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_isolation_design_contract.py
3 passed
```

Figure check:

```text
local_2d_source_factor_isolation_design_contract.png
2104x778, dynamic range=255
```
