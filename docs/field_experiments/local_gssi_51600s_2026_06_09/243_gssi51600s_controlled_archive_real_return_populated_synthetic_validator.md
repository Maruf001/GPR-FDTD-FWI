# Field Experiment 243: Controlled Archive Real Return Populated Synthetic Validator

Date: 2026-06-28

## Purpose

Validate the run `242` populated synthetic archive smoke from saved artifacts.
The goal is to confirm that a downstream consumer can read the saved file,
signoff, provenance, check, and summary tables and recover the same decision:
the synthetic intake path is mechanically valid, but real archive acceptance is
still blocked.

This is a CPU-only validation run. It does not contain real measured field
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/243_gssi51600s_controlled_archive_real_return_populated_synthetic_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_populated_synthetic_validator_checks.csv
data/field_controlled_archive_real_return_populated_synthetic_validator_summary.json
figures/field_controlled_archive_real_return_populated_synthetic_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_POPULATED_SYNTHETIC_VALIDATOR.md
```

## Result

```text
validation checks:                 6
validation checks passed:          6
blocking failures:                 0
synthetic smoke validation ready:  true
synthetic archive smoke ready:     true
synthetic checksum smoke ready:    true
real files present:                false
real signoff values present:       false
real provenance values present:    false
real archive acceptance ready:     false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The six validation checks confirm:

| Check | Result |
| --- | --- |
| Synthetic files are complete and not real | pass |
| Signoff rows are completed synthetic values | pass |
| Provenance rows are completed synthetic values | pass |
| Archive checks all pass | pass |
| Summary counts are consistent | pass |
| Real archive and downstream states are blocked | pass |

## Interpretation

Run `242` is a reliable positive-control artifact for the archive-intake
mechanics. It proves that the saved synthetic archive root, worksheet values,
provenance values, and checksum checks are internally consistent.

It still does not change the field evidence boundary. Real measured files,
real signoff values, real provenance values, checksum intake on staged real
files, and controlled-evidence acceptance remain required before field evidence
or field FWI can be claimed.

## Decision

Use runs `242`-`243` as the guarded positive-control archive-intake smoke.
Real archive acceptance, controlled field evidence, field FWI, field 3D/HPC,
and GPU escalation remain blocked until real files pass the same checks.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_populated_synthetic_validator.py
6 passed
```

Figure validation:

```text
2645x821, dynamic range=255
```
