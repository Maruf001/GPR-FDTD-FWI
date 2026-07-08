# Field Experiment 147: Controlled Collection Scaffold

Date: 2026-06-18

## Purpose

Convert the run `146` blocker-prioritization action groups into a
collection-ready packet scaffold for a future controlled 2D GSSI pass.

This is a CPU-only field-planning artifact. It does not run FDTD, FWI, GPU
kernels, field FWI, 3D/HPC work, or neural-network training. The scaffold is
not completed field data.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/147_gssi51600s_controlled_collection_scaffold
```

Key artifacts:

```text
packet_scaffold/session_log.csv
packet_scaffold/target_truth.csv
packet_scaffold/profile_geometry.csv
packet_scaffold/acquisition_run.csv
packet_scaffold/reference_measurement.csv
data/field_controlled_collection_tasks.csv
data/field_controlled_collection_scaffold_status.csv
data/field_controlled_collection_scaffold_summary.json
figures/field_controlled_collection_scaffold.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                    gssi51600s_controlled_collection_scaffold
packet tables:                   5
packet rows:                     12
planned sessions:                1
planned targets:                 1
planned profiles:                1
planned acquisition repeats:     3
planned time-zero references:    3
planned amplitude references:    3
reference uncertainty gate:      0.02 ns
reference depth equivalent:      1.9986 mm
action groups:                   7
new controlled-data groups:      6
blank measured/session fields:   72
planned identifiers only:        true
validator expected to pass:      false
ready for collection:            true
ready for current archive FWI:   false
ready for heavy field work:      false
ready for field 3D/HPC:          false
gpu priority:                    none
```

Planned IDs:

```text
session:  planned_controlled_2d_session_001
target:   T_CONTROL_001
profile:  P_CONTROL_001
time zero references: T0_REF_001, T0_REF_002, T0_REF_003
amplitude references: AMP_REF_001, AMP_REF_002, AMP_REF_003
```

## Interpretation

The scaffold gives the future field pass stable row IDs and a minimum repeat
structure, but it intentionally leaves measured values blank. It should be used
as a collection worksheet, then filled from actual controlled field data and
revalidated with the packet validator.

Current-archive field FWI, heavy field GPU work, and field 3D/HPC remain
blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_scaffold.py
3 passed
```

Figure validation:

```text
field_controlled_collection_scaffold.png: 2569x937,
nonwhite=0.1969, dynamic range=255
```
