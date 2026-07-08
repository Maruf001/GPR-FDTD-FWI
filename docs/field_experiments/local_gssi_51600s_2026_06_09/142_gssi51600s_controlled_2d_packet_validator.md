# Field Experiment 142: Controlled 2D Packet Validator

Date: 2026-06-18

## Purpose

Validate the generated controlled-acquisition packet from run `141` before any
future field inversion proposal.

This is CPU-only field-readiness tooling. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/142_gssi51600s_controlled_2d_packet_validator
```

Key artifacts:

```text
data/controlled_2d_packet_validation_summary.json
data/controlled_2d_packet_validation_findings.csv
data/controlled_2d_packet_table_status.csv
data/controlled_2d_packet_acceptance_status.csv
```

## Result

```text
tables:                              5
total rows:                          5
filled rows:                         0
validation rules:                   51
required-field evaluations:         51
blocking findings:                  51
missing required values:            51
dtype failures:                      0
cross-table failures:                0
acceptance gates:                    7
packet acceptance ready:             false
current archive field FWI ready:     false
current archive heavy field ready:   false
field 3D/HPC ready:                  false
gpu priority:                        none
```

## Interpretation

The blank run `141` packet fails by design. All required fields are currently
empty, and all seven acceptance gates remain false. This gives a concrete
future handoff rule: field inversion or heavy field compute should not be
proposed until a filled controlled-acquisition packet passes this validator.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_2d_packet_validator.py
4 passed
```
