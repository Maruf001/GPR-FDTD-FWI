# Experiment 1474: Near/Far Spacing Generalization Probe

Date: 2026-06-28

## Purpose

Execute the neighbor-spacing generalization check from the guarded near/far
interaction design block.

The run repeats the near/far radius-error interaction grid at three neighbor
spacings while keeping the target fixed:

```text
neighbor spacing deltas:   -10 mm, 0 mm, +10 mm
near-radius deltas:        +0.0, +0.5, +1.0, +1.5, +1.9 mm
far-radius deltas:         +0.0, -0.8, -1.6 mm
grid models:               45
objective rows:            270
candidate rows:            1080
```

This is CPU-only. It does not launch GPU work, transfer to field evidence, run
field FWI, promote a physical claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1474_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_probe.png
scripts/script_snapshot_manifest.json
```

## Result

```text
spacing count:                       3
grid models:                         45
objective selection rows:            270
candidate rows:                      1080
all-objectives-truth models:         23
any-failure models:                  22
all-objective failure models:        12
elapsed seconds:                     1757.461
spacing probe ready:                 true
promote revised objective now:       false
broad radius tolerance promoted:     false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

First near-radius delta that causes any objective failure:

| Neighbor spacing | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| 10 mm narrower | +1.5 | +0.5 | +0.5 |
| baseline | +1.5 | +0.5 | +0.5 |
| 10 mm wider | +1.5 | none | none |

First near-radius delta that causes all objectives to fail:

| Neighbor spacing | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| 10 mm narrower | none | +1.5 | +1.5 |
| baseline | +1.5 | +1.5 | +1.5 |
| 10 mm wider | +1.5 | none | none |

## Interpretation

The near/far mechanism is not invariant to neighbor spacing. Narrower spacing
and baseline spacing behave similarly for the first partial failures: far
radius errors move the first failure from near +1.5 mm to near +0.5 mm. Wider
spacing changes that behavior: with far-radius error present, all tested
near-radius values recover the truth across all objectives.

The severe all-objective wrong-lock boundary is also spacing dependent. The
baseline spacing fails across all far-radius settings at near +1.5 mm. The
narrower spacing produces all-objective failures at near +1.5 mm only when a
far-radius error is present. The wider spacing produces all-objective failures
only in the no-far-error slice, while the far-error slices remain stable.

This strengthens the local mechanism story but narrows the claim. The
near-neighbor radius effect is real in the tested synthetic setup, but its
severity depends on neighbor spacing and on the far-neighbor state.

## Decision

Use run `1474` as the first executed neighbor-spacing generalization check.
Do not promote broad radius tolerance, physical transfer, GPU work, field FWI,
or 3D/HPC work from this branch. The next 2D generalization work should
validate this result from saved artifacts, then test source/acquisition
generalization before any broader claim is considered.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_probe_cpu.py
5 passed
```

Figure validation:

```text
3184x1495, dynamic range=255
```
