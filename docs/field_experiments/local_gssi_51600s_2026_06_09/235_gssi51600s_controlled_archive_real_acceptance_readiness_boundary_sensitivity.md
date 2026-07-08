# Field Experiment 235: Controlled Archive Real Acceptance Readiness Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `234` validator for the refreshed real archive-acceptance
readiness boundary.

Run `233` defined the current boundary after adding synthetic completed
worksheet intake. Run `234` validated that boundary under the exact expected
state. This run asks whether the validator rejects controlled damage to the
boundary.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/235_gssi51600s_controlled_archive_real_acceptance_readiness_boundary_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_acceptance_readiness_boundary_sensitivity_scenarios.csv
data/field_controlled_archive_real_acceptance_readiness_boundary_sensitivity_summary.json
figures/field_controlled_archive_real_acceptance_readiness_boundary_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_ACCEPTANCE_READINESS_BOUNDARY_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_acceptance_readiness_boundary_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_sensitivity.py
```

## Result

```text
scenarios:                         21
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        20
observed failure scenarios:        20
unexpected outcomes:                0
sensitivity ready:                  true
real measured files present:        false
real signoff values present:        false
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The exact run `233` boundary passes. Twenty damaged variants fail as expected,
including boundary-count drift, item-name drift, synthetic-only intake
promotion, missing real-file and provenance blockers, missing next-action
fields, and false archive/checksum/evidence/FWI/3D readiness.

## Interpretation

The real archive-acceptance boundary is now guarded from the current consumer
side. Synthetic worksheet mechanics are allowed as a dry-run support layer, but
they are not allowed to become real archive acceptance.

The required next field-side data remain unchanged: nine real measured DZT
files, real operator signoff values, measured provenance values, checksum
intake on staged real files, and controlled-evidence acceptance after rerunning
the real-data gates.

## Decision

Use runs `233-235` as the guarded current real archive-acceptance boundary.
Do not launch field FWI, field 3D/HPC, heavy GPU work, or field evidence
promotion from the current dry-run archive.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_sensitivity.py
6 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_acceptance_readiness_boundary_sensitivity.png
3365x886, dynamic range=255
```
