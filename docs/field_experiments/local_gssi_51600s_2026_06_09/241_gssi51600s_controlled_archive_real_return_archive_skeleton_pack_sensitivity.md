# Field Experiment 241: Controlled Archive Real Return Archive Skeleton Pack Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `240` empty archive skeleton pack validator.

Run `240` validated the run `239` skeleton under the exact expected state. This
run checks whether the validator fails closed when counts, directory rows,
placeholder-file flags, blank templates, or downstream readiness states are
damaged.

It does not create placeholder DZT files, contain real measured files, accept
an archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/241_gssi51600s_controlled_archive_real_return_archive_skeleton_pack_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_archive_skeleton_pack_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_archive_skeleton_pack_sensitivity_summary.json
figures/field_controlled_archive_real_return_archive_skeleton_pack_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_ARCHIVE_SKELETON_PACK_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_return_archive_skeleton_pack_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_return_archive_skeleton_pack_sensitivity.py
```

## Result

```text
scenarios:                         26
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        25
observed failure scenarios:        25
unexpected outcomes:                0
sensitivity ready:                  true
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The exact run `239` skeleton passes. Twenty-five damaged variants fail as
expected, including count drift, missing expected-file rows, directory drift,
placeholder-file creation, prefilled signoff/provenance templates, and false
archive/downstream readiness.

## Interpretation

The empty real-return archive skeleton is now guarded from the current consumer
side. It remains a staging aid only, not real field evidence.

## Decision

Use runs `239-241` as the guarded empty real-return archive skeleton pack.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_archive_skeleton_pack_sensitivity.py
6 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_archive_skeleton_pack_sensitivity.png
3581x886, dynamic range=255
```
