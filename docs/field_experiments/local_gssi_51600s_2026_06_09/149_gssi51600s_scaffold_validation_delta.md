# Field Experiment 149: Scaffold Validation Delta

Date: 2026-06-18

## Purpose

Compare the current-archive packet validation from run `144` with the
controlled-collection scaffold validation from run `148`.

This is CPU-only synthesis of saved packet-validation outputs. It does not run
FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/149_gssi51600s_scaffold_validation_delta
```

Key artifacts:

```text
data/field_scaffold_validation_delta_summary.json
data/field_scaffold_validation_table_delta.csv
data/field_scaffold_validation_gate_delta.csv
figures/field_scaffold_validation_delta.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_scaffold_validation_delta
current rows -> scaffold rows:         11 -> 12
filled rows:                           9 -> 12
filled-row delta:                      +3
missing required values:               67 -> 60
missing-required delta:                -7
cross-table failures:                  0 -> 0
ready acceptance gates:                0 -> 0
target-truth row evidence:             0 -> 1
short-repeat target evidence:          0 -> 1
time-zero reference evidence:          0 -> 0
amplitude reference evidence:          0 -> 0
planned time-zero references:          3
planned amplitude references:          3
ready for collection:                  true
ready for packet acceptance:           false
ready for current archive field FWI:   false
ready for heavy field work:            false
ready for field 3D/HPC:                false
gpu priority:                          none
```

## Interpretation

The scaffold improves structural readiness: it creates coherent target,
profile, acquisition-repeat, and reference IDs; filled rows increase from 9 to
12; and missing required values drop from 67 to 60. It also changes
target-truth and short-repeat evidence from absent to structurally present.

The scaffold still lacks measured target geometry, time-zero values, amplitude
metrics, survey coordinates, Tx/Rx offsets, coupling notes, and session details.
All acceptance gates remain blocked, so the scaffold is a collection worksheet,
not a field-inversion launch gate.

## Validation

Focused test:

```text
tests/test_gssi_field_scaffold_validation_delta.py
3 passed
```

Figure validation:

```text
field_scaffold_validation_delta.png: 2654x971,
nonwhite=0.1221, dynamic range=255
```
