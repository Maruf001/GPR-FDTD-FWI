# Field Experiment 152: Recovered Scaffold Type-Aware Validation

Date: 2026-06-18

## Purpose

Rerun the recovered controlled-collection scaffold validation with
reference-type-aware required-field logic.

Run `151` correctly applied recovered session metadata, but the packet
validator still treated every `reference_measurement` row as if it needed both
time-zero and amplitude fields. The scaffold intentionally has separate
`metal_plate_t0` and `amplitude_reflector` rows, so this run validates the same
packet with conditional reference requirements.

This is CPU-only packet validation. It does not run DZT preprocessing, FDTD,
FWI, GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/152_gssi51600s_recovered_scaffold_type_aware_validation
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
policy label:                         gssi51600s_controlled_2d_packet_validator
source packet:                         151 recovered-session scaffold
table count:                           5
total rows:                            12
filled rows:                           12
validation rules:                      51
required-field evaluations:            119
blocking findings:                     44
missing required values:               44
dtype failures:                        0
cross-table failures:                  0
acceptance gates:                      7
ready for packet acceptance:           false
ready for current archive field FWI:   false
ready for heavy field work:            false
ready for field 3D/HPC:                false
gpu priority:                          none
```

Table status:

```text
session_log:            missing required 2
target_truth:           missing required 9
profile_geometry:       missing required 6
acquisition_run:        missing required 9
reference_measurement:  missing required 18
```

Remaining reference blockers are now type-specific:

```text
metal_plate_t0 rows 1-3:
  file_name, measured_time_zero_ns, time_zero_uncertainty_ns

amplitude_reflector rows 4-6:
  file_name, amplitude_metric, amplitude_repeatability_pct
```

Acceptance gates remain blocked:

```text
required_metadata_fields:       false (missing_required=44; dtype_failures=0)
cross_table_links:              false (cross_table_failures=0, but packet incomplete)
target_truth_controls:          false
absolute_time_zero_references:  false
amplitude_references:           false
short_repeat_redundancy:        false
field_fwi_or_heavy_work:        false
```

## Interpretation

The field packet is more actionable after this correction. Run `152` reduces
the recovered scaffold blocker count from run `151`'s over-strict `56` to `44`
without changing the scientific state: it is still a collection worksheet, not
accepted field data.

The remaining blockers correspond to real measurements that must be collected:
date/operator, target truth, surveyed profile geometry, three acquisition file
names, controlled Tx/Rx offset, coupling condition, three timing-reference
files and timing values, and three amplitude-reference files and amplitude
values.

This improves field-side planning and prevents inflated blocker counts, but it
does not enable current-archive field FWI, heavy field GPU work, 3D/HPC work,
or calibrated radius/depth claims.

## Validation

Focused validator test:

```text
tests/test_gssi_field_controlled_2d_packet_validator.py
5 passed
```
