# Experiment 907: Local 2D Source-Factor Geometry-Instability Objective/Source Discriminant Execution Audit

Date: 2026-06-25

## Purpose

Execute the bounded geometry-instability objective/source commands from run
`224` and determine whether any source-timing or objective-weighting
discriminant reverses the lower-x preference found in run `222`.

This is targeted CPU optimizer work. It does not launch a broad source-factor
batch, GPU work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/226_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit
```

Completed optimizer outputs:

```text
outputs/experiments/1367_local_2d_source_factor_geomxdisc_matched_nominal_source_base_cpu
outputs/experiments/1368_local_2d_source_factor_geomxdisc_time_grid_base_cpu
```

The highband command did not produce an optimizer output because the optimizer
requires the first diagnostic objective variant to be labelled `base`.

## Result

```text
commands in design:                 3
complete optimizer outputs:         2
usable evidence rows:               2
nonzero exits:                      1
required artifacts present:         12 / 18
candidate CSV count:                2
figure file count:                  8
truth x selected count:             0
truth xyz selected count:           0
matched nominal best x:             188.0
time-grid best x:                   188.0
time-grid best source time ps:      -50.0
geometry discriminant evidence ready: false
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

Per-command result:

| Design | Complete | Best x | Best z | Best r | Source time ps | Truth x |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `matched_nominal_source_base` | true | 188.0 | 90.0 | 5.0 | 0.0 | false |
| `shifted_source_highband` | false |  |  |  |  | false |
| `time_grid_base` | true | 188.0 | 90.0 | 5.0 | -50.0 | false |

## Interpretation

The two completed discriminants both preserve the lower-x preference:

- Matched nominal source timing still selects `x=188`.
- Allowing a small source-time grid still selects `x=188`, with best source
  time `-50 ps`.

The highband discriminant was a command-design error, not a scientific result:
`run_multi_rebar_coordinate_optimizer.py` requires the first diagnostic
objective variant to be labelled `base`, so a highband-only objective command
is invalid.

The partial evidence strengthens the blocker: source timing alone does not
explain the geometry-instability lower-x preference. A corrected highband
design must include `base` first if that objective branch is still worth
testing.

## Decision

Do not promote the source-factor branch. Full source-factor batch execution,
GPU work, field transfer, and source-factor claims remain blocked.

The next useful task is a corrected highband-plus-base command design, not a
broader compute run.

## Milestone Snapshot

This is a result-driven local 2D partial execution milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
sha256: cbb9be1a87112710516cb76316bd96296dac19657896e9814df99edf03722778

test_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
sha256: f245dd04a2fd6a82949ec44e04af4b31a0699a0553dc62fd81fccbe37a3a9f4b
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
3 passed
```

Figure check:

```text
local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.png
2032x770, dynamic range=255
```
