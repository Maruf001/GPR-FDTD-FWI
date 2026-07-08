# Field Experiment 180: Current Data Inventory Controlled-Acceptance Audit

Date: 2026-06-27

## Purpose

Inventory the current local GSSI data folder and compare it with the controlled
archive acceptance contract from run `176`.

The current data folder contains real local GSSI files, but the controlled
archive contract requires classified controlled profile repeats, time-zero
references, amplitude references, metadata artifacts, checksums, intake rows,
and provenance reruns. This run checks that the current files are not
accidentally promoted beyond their evidence status.

This run does not relabel current files as controlled evidence, run DZT
preprocessing, run field FWI, launch GPU/HPC work, or make a measured-field
claim.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/180_gssi51600s_current_data_inventory_controlled_acceptance_audit
```

Key artifacts:

```text
data/field_current_data_inventory_files.csv
data/field_current_data_inventory_acceptance_gap.csv
data/field_current_data_inventory_controlled_acceptance_audit_summary.json
figures/field_current_data_inventory_controlled_acceptance_audit.png
docs/FIELD_CURRENT_DATA_INVENTORY_CONTROLLED_ACCEPTANCE_AUDIT.md
scripts/run_gssi_field_current_data_inventory_controlled_acceptance_audit.py
scripts/test_gssi_field_current_data_inventory_controlled_acceptance_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
input data folder:                 data/2026-06-09_GSSI_model_51600S
current files inventoried:         8
current DZT files:                 4
current DZX sidecars:              4
required controlled DZT files:     9
required metadata artifacts:       6
accepted controlled DZT files:     0
accepted metadata artifacts:       0
sidecars complete for current data:true
controlled archive acceptance ready:false
provenance acceptance ready:       false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

Acceptance gap:

| Requirement | Required | Accepted | Ready | Reason |
| --- | ---: | ---: | --- | --- |
| controlled profile repeat files | 3 | 0 | false | current DZT files are not accepted controlled profile repeats |
| time-zero reference files | 3 | 0 | false | no measured time-zero reference files are classified |
| amplitude reference files | 3 | 0 | false | no measured amplitude-reference files are classified |
| metadata artifacts | 6 | 0 | false | controlled archive metadata artifacts are not present in the required layout |
| DZX sidecars | 4 | 4 | true | sidecars exist for current archive DZT files but do not replace controlled metadata |

## Interpretation

The current local data folder contains four DZT files and four DZX sidecars.
Those files are real current-archive files, but they are not accepted as the
controlled collection archive. The required controlled roles, nine measured
files, six metadata artifacts, checksum ledger, intake manifest, and provenance
reruns are still absent.

This distinction matters: the current files can remain QC context, but they
cannot close the controlled archive acceptance gate by relabeling.

## Decision

Keep the current data folder as QC context only.

Do not promote it to the controlled archive, measured-field evidence, field
FWI, GPU work, or 3D/HPC until the run `176` acceptance gates are satisfied
with real classified files and metadata.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_data_inventory_controlled_acceptance_audit.py
sha256: 7ca82ac28a7cc0cdb23dc71275ed8088a30cea270ba2010f0af61694abe9ff3a

test_gssi_field_current_data_inventory_controlled_acceptance_audit.py
sha256: fb0310f957f8234ba675db2d9d8c8cf0d27fafdd0a7ed2135b7c826ec67e14e2
```

Subsequent related field acceptance experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_data_inventory_controlled_acceptance_audit.py
3 passed
```

Figure check:

```text
field_current_data_inventory_controlled_acceptance_audit.png
2140x851, dynamic range=255
```
