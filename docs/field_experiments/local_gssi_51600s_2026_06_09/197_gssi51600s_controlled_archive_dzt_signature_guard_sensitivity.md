# Field Experiment 197: Controlled Archive DZT Signature Guard Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the run `196` DZT signature guard against controlled positive and
negative synthetic files.

Run `196` calibrated the guard against observed real GSSI files and old
synthetic placeholders. This run adds a controlled sensitivity suite: one valid
synthetic binary file and five invalid cases covering tiny files, text
placeholders, wrong binary prefixes, wrong extensions, and missing files.

This is a CPU-only guard sensitivity run. It does not create real measured
evidence, accept the archive, run field FWI, launch GPU/HPC work, run field 3D,
or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/197_gssi51600s_controlled_archive_dzt_signature_guard_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_dzt_signature_guard_sensitivity_rows.csv
data/field_controlled_archive_dzt_signature_guard_sensitivity_summary.json
figures/field_controlled_archive_dzt_signature_guard_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_DZT_SIGNATURE_GUARD_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_dzt_signature_guard_sensitivity.py
scripts/test_gssi_field_controlled_archive_dzt_signature_guard_sensitivity.py
synthetic_signature_cases/
```

## Result

```text
scenarios:                         6
expected passes:                   1
expected failures:                 5
observed passes:                   1
observed failures:                 5
unexpected outcomes:               0
signature guard sensitivity ready: true
checksum/intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

Scenario outcomes:

| Scenario | Expected pass | Observed pass | Exists | Extension | Size | Header |
| --- | --- | --- | --- | --- | --- | --- |
| valid_signature_min_size | true | true | true | true | true | true |
| tiny_valid_prefix | false | false | true | true | false | true |
| tiny_text_placeholder | false | false | true | true | false | false |
| large_wrong_prefix | false | false | true | true | true | false |
| wrong_extension | false | false | true | false | true | true |
| missing_file | false | false | false | true | false | false |

## Interpretation

The DZT signature guard behaves as expected across the sensitivity suite. It
accepts only the valid synthetic binary case and rejects tiny files, text
placeholders, wrong binary prefixes, wrong extensions, and missing files.

## Decision

Keep the signature guard in the controlled archive preflight path. Do not run
checksum/intake acceptance, field FWI, GPU work, or field 3D/HPC until real
controlled files pass the guard and downstream gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_dzt_signature_guard_sensitivity.py
4 passed
```

Figure validation:

```text
field_controlled_archive_dzt_signature_guard_sensitivity.png
2284x842, dynamic range=255
```
