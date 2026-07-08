# Field Experiment 200: Integrated Archive Acceptance Contract Refresh

Date: 2026-06-28

## Purpose

Refresh the controlled real-archive acceptance contract after integrating the
DZT signature guard into archive preflight.

Runs `198` and `199` showed that the old shape-only archive preflight can mark a
synthetic placeholder archive as ready. The integrated shape-plus-signature
preflight prevents that false-ready decision. This run updates the real-archive
acceptance contract so DZT signature checks are now explicit acceptance stages.

This run does not ingest real field files, modify the pending archive, run field
FWI, launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/200_gssi51600s_controlled_archive_integrated_acceptance_contract_refresh
```

Key artifacts:

```text
data/field_controlled_archive_integrated_acceptance_contract_rows.csv
data/field_controlled_archive_integrated_acceptance_contract_refresh_summary.json
figures/field_controlled_archive_integrated_acceptance_contract_refresh.png
docs/FIELD_CONTROLLED_ARCHIVE_INTEGRATED_ACCEPTANCE_CONTRACT_REFRESH.md
scripts/run_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py
scripts/test_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py
```

## Result

```text
source contract stages:              8
refreshed contract stages:           10
metadata values required:            11
real files required:                 9
DZT signature slots required:        9
DZT size floor bytes:                65536
GSSI header prefix hex:              ff07
legacy false-ready candidates:       1
false-ready prevented by signature:  1
integrated-ready candidates:         0
contract refresh ready:              true
real archive acceptance ready:       false
checksum intake ready:               false
controlled evidence ready:           false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

The refreshed contract inserts two explicit stages after archive layout:

| New stage | Required items | Current blockers | Purpose |
| --- | ---: | ---: | --- |
| dzt_signature_preflight | 9 | 9 | Require each controlled DZT file to exceed the size floor and match the GSSI binary header |
| integrated_archive_preflight | 2 | 2 | Accept no archive for checksum/intake unless both shape checks and DZT signature checks pass |

## Interpretation

The field archive gate is now stricter and safer. A placeholder archive that
only has the right file paths is no longer enough. Each expected controlled
`.DZT` file must also pass a conservative GSSI binary signature guard before
checksum/intake acceptance can proceed.

The refreshed contract does not close the real-data gap. The nine real measured
files and measured metadata are still absent, so real archive acceptance and
field FWI remain blocked.

## Decision

Use this refreshed contract as the current field-side archive acceptance gate.

Keep checksum/intake, controlled evidence, real archive acceptance, field FWI,
GPU work, and field 3D/HPC blocked until a real archive passes the integrated
gate and all downstream checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_signature_preflight_integration_audit.py
tests/test_gssi_field_controlled_archive_signature_preflight_validator.py
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py
10 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py: pass
tests/test_gssi_field_controlled_archive_integrated_acceptance_contract_refresh.py: pass
```

Figure check:

```text
3076x895, dynamic range=255
```
