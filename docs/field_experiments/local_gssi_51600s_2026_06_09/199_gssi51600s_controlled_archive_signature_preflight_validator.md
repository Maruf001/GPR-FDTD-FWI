# Field Experiment 199: Controlled Archive Signature Preflight Validator

Date: 2026-06-27

## Purpose

Validate the run `198` integrated archive preflight from a consumer
perspective.

Run `198` showed that the old shape-only preflight can mark a placeholder
archive as ready. This validator checks that the integrated shape-plus-
signature preflight prevents that false-ready state and keeps downstream gates
blocked.

This is a CPU-only validation run. It does not create measured field evidence,
accept the archive, run DZT preprocessing, launch field FWI, use GPU/HPC, run
field 3D, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/199_gssi51600s_controlled_archive_signature_preflight_validator
```

Key artifacts:

```text
data/field_controlled_archive_signature_preflight_validation_checks.csv
data/field_controlled_archive_signature_preflight_validator_summary.json
figures/field_controlled_archive_signature_preflight_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_SIGNATURE_PREFLIGHT_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_signature_preflight_validator.py
scripts/test_gssi_field_controlled_archive_signature_preflight_validator.py
```

## Result

```text
validation checks:                       7
validation passes:                       7
blocking failures:                       0
source candidate archives:               2
source legacy false-ready candidates:    1
false-ready prevented by signature:      1
source integrated-ready candidates:      0
signature preflight validation ready:    true
checksum/intake ready:                   false
controlled evidence ready:               false
field FWI ready:                         false
field 3D/HPC ready:                      false
GPU priority:                            none
```

## Interpretation

The integrated preflight behaves correctly from a consumer perspective. The
synthetic placeholder archive is blocked despite passing the old shape-only
preflight, the pending archive remains blocked, and no candidate is ready for
checksum/intake.

## Decision

Use the run `198` integrated preflight as the controlled archive gate. Keep
checksum/intake, controlled evidence, field FWI, GPU work, and field 3D/HPC
blocked until a real archive passes it and all downstream gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_signature_preflight_validator.py
4 passed
```

Figure validation:

```text
field_controlled_archive_signature_preflight_validator.png
2249x839, dynamic range=255
```
