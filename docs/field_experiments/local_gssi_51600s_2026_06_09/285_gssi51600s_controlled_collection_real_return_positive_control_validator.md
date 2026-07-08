# Field Experiment 285: Positive-Control Validator

Date: 2026-06-28

## Purpose

Validate the saved run `284` synthetic positive-control fill smoke from
artifacts.

Run `284` proved that the current return-inbox mechanics can recognize a
complete packet when a private synthetic inbox contains nine non-empty
DZT-shaped files, 32 metadata values, and nine matching checksums. This run
verifies that result from saved rows, summary, figure validation, and script
snapshots.

This is a CPU-only validator. It does not stage real measured field data,
modify the real return inbox, accept provenance, accept a real archive, run
field FWI, run field 3D/HPC, or launch GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/285_gssi51600s_controlled_collection_real_return_positive_control_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_positive_control_validator_checks.csv
data/field_controlled_collection_real_return_positive_control_validator_summary.json
figures/field_controlled_collection_real_return_positive_control_validator.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_POSITIVE_CONTROL_VALIDATOR.md
```

## Result

```text
validation checks:                  6
passed checks:                      6
failed checks:                      0
positive-control validation ready:  true
synthetic mechanics pass:           true
synthetic files present:            9
synthetic metadata present:         32
synthetic checksums present:        9
synthetic checksum matches:         9
real measured data present:         false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The saved positive-control fill smoke is internally consistent: scanner
mechanics pass when a complete synthetic packet is staged, and the
synthetic-only boundary remains intact.

## Decision

Use run `285` as the saved-artifact validator for the positive-control
mechanics smoke. Sensitivity hardening is still required before treating the
block as guarded.
