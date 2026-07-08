# Field Experiment 236: Controlled Archive Real Return Intake Contract

Date: 2026-06-28

## Purpose

Join the guarded operator manifest, signoff contract, provenance closure
actions, and real-acceptance boundary into one real-return intake contract.

Runs `221-235` separately defined the archive file slots, worksheet signoff
requirements, synthetic completed-worksheet boundary, and real archive-
acceptance blockers. This run makes the future measured-data return shape
explicit in one place.

It does not contain real measured files, fill real signoff values, accept an
archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/236_gssi51600s_controlled_archive_real_return_intake_contract
```

Key artifacts:

```text
data/field_controlled_archive_real_return_intake_contract_file_rows.csv
data/field_controlled_archive_real_return_intake_contract_provenance_rows.csv
data/field_controlled_archive_real_return_intake_contract_gate_rows.csv
data/field_controlled_archive_real_return_intake_contract_summary.json
figures/field_controlled_archive_real_return_intake_contract.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_INTAKE_CONTRACT.md
scripts/run_gssi_field_controlled_archive_real_return_intake_contract.py
scripts/test_gssi_field_controlled_archive_real_return_intake_contract.py
```

## Result

```text
file contract rows:                 9
directories:                        3
planned file checks:               27
required signoff cells:            27
optional signoff cells:             9
provenance action groups:           6
gates:                             10
real acceptance blockers:           5
contract ready:                     true
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

File requirements:

| File role | Count |
| --- | ---: |
| controlled_profile_repeat | 3 |
| time_zero_reference | 3 |
| amplitude_reference | 3 |

Blocking return gates:

| Gate | Status |
| --- | --- |
| real_measured_file_return | blocked_missing_real_files |
| real_signoff_return | blocked_missing_real_signoff |
| measured_provenance_return | blocked_missing_real_provenance |
| checksum_intake | blocked_until_real_files |
| controlled_evidence_acceptance | blocked_until_real_gates_pass |

## Interpretation

The field side now has a single real-return contract: nine DZT file slots, 27
planned file checks, 27 required signoff cells, six provenance closure actions,
and guarded acceptance gates. The contract is ready as an intake shape, but it
contains no real files or measured signoff/provenance values.

## Decision

Use run `236` as the real-return intake contract for future measured field
files. Real archive acceptance, checksum intake, controlled evidence, field
FWI, and field 3D/HPC remain blocked until real data fill this contract and the
gates are rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_intake_contract.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_intake_contract.png
3220x877, dynamic range=255
```
