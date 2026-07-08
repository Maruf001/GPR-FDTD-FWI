# Experiment 912: Local 2D Source-Factor Geometry-Instability Neighbor-State Design

Date: 2026-06-25

## Purpose

Design a bounded CPU audit for whether the geometry-instability lower-x
preference is caused by the non-target neighbor rebar state.

Run `234` ruled out objective-window selection: every established objective
window selected `x=188 mm` instead of the `x=190 mm` truth. This run keeps the
target candidate set fixed and varies only the neighbor state:

```text
target candidates: x=188,189,190 mm; z=90 mm; radius=5 mm
observed truth:    x=190,250,310 mm; z=90,90,90 mm; radii=5,6,8 mm
```

This is command design only. It does not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/236_local_2d_source_factor_geometry_instability_neighbor_state_design
```

Key artifacts:

```text
data/local_2d_source_factor_geometry_instability_neighbor_state_commands.csv
data/local_2d_source_factor_geometry_instability_neighbor_state_validation.csv
data/local_2d_source_factor_geometry_instability_neighbor_state_summary.json
commands/run_local_2d_source_factor_geometry_instability_neighbor_state.sh
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_NEIGHBOR_STATE_DESIGN.md
figures/local_2d_source_factor_geometry_instability_neighbor_state_design.png
scripts/run_local_2d_source_factor_geometry_instability_neighbor_state_design.py
scripts/test_local_2d_source_factor_geometry_instability_neighbor_state_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source execution run:             234
source all objectives lower x:    true
commands generated:               3
commands passing gates:           3
predicted runner experiment IDs:  1371, 1372, 1373
estimated candidate-objectives:   9
execution ready:                  true
full batch ready:                 false
GPU work ready:                   false
field transfer ready:             false
```

Designed commands:

| Design | Neighbor state changed | Initial x | Initial z | Initial radii | Expected output |
| --- | --- | --- | --- | --- | --- |
| `truth_neighbor_positions_base` | neighbor x/z to truth | `188,250,310` | `100,90,90` | `6,6,6` | `1371_local_2d_source_factor_geomx_neighbor_positions_base_cpu` |
| `truth_neighbor_radii_base` | neighbor radii to truth | `188,248,312` | `100,90,95` | `6,6,8` | `1372_local_2d_source_factor_geomx_neighbor_radii_base_cpu` |
| `truth_neighbor_full_base` | neighbor x/z/radii to truth | `188,250,310` | `100,90,90` | `6,6,8` | `1373_local_2d_source_factor_geomx_neighbor_full_base_cpu` |

## Interpretation

This design is narrower than a new source-factor sweep. It tests whether the
target-0 lower-x preference is compensation for wrong neighbor positions, wrong
neighbor radii, or both.

## Decision

Use run `236` as the source for the next three-command CPU execution audit.
Do not launch broad source-factor batches, GPU work, field transfer, or claims
from the current evidence.

## Milestone Snapshot

This is a result-driven local 2D command-design milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_design.py
sha256: 25186e022f8098d7ee342007a9170935212f522d934f3e0726ed0718c7860200

test_local_2d_source_factor_geometry_instability_neighbor_state_design.py
sha256: 5cb1b5819488297b3095d22926198bcdd017bce6d15056bb12a6cc1255177876
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_neighbor_state_design.py
3 passed
```

Compile check:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_design.py: pass
tests/test_local_2d_source_factor_geometry_instability_neighbor_state_design.py: pass
```

Figure check:

```text
1817x738, dynamic range=255
```
