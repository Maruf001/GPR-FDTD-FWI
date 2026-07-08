# Field Experiment 244: Controlled Archive Real Return Populated Synthetic Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `243` populated synthetic archive smoke validator. The
goal is to verify that the validator accepts the exact run `242` synthetic
smoke and rejects controlled damage to file rows, signoff rows, provenance
rows, archive-check rows, summary counts, and real/downstream readiness flags.

This is a CPU-only validation run. It does not contain real measured field
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/244_gssi51600s_controlled_archive_real_return_populated_synthetic_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_populated_synthetic_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_populated_synthetic_sensitivity_summary.json
figures/field_controlled_archive_real_return_populated_synthetic_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_POPULATED_SYNTHETIC_SENSITIVITY.md
```

## Result

```text
scenarios:                         37
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        36
observed failure scenarios:        36
unexpected outcomes:               0
sensitivity ready:                 true
synthetic archive smoke ready:     true
synthetic checksum smoke ready:    true
real archive acceptance ready:     false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The exact run `242` populated synthetic archive smoke passes. All 36 damaged
variants fail as expected for synthetic file count drift, file-role drift,
missing synthetic-file flags, real-file promotion, extension/size/header/SHA
drift, signoff row drift, signoff SHA mismatch, real signoff promotion,
provenance row drift, synthetic provenance loss, real provenance promotion,
archive-check drift, summary count drift, and false real archive/downstream
readiness.

## Interpretation

The positive-control archive-intake smoke is now guarded. The field intake path
can be exercised with correctly shaped synthetic files, and the validator
rejects the common ways such a synthetic smoke could be mistaken for real field
evidence.

Real measured files, real operator signoff values, real provenance values,
checksum intake on staged real files, and controlled-evidence acceptance remain
required before field evidence, field FWI, field 3D/HPC, or GPU escalation.

## Decision

Use runs `242`-`244` as the guarded positive-control archive-intake smoke.
Keep real archive acceptance and all downstream field claims blocked until real
files pass the same checks.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_populated_synthetic_sensitivity.py
6 passed
```

Figure validation:

```text
4121x879, dynamic range=255
```
