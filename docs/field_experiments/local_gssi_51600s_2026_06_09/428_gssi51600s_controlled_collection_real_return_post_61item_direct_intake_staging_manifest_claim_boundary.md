# Field Experiment 428: Post Direct-Intake Staging Manifest Claim Boundary

Date: 2026-06-30

## Purpose

Fold the guarded direct-intake staging manifest from runs `425-427` into the
field claim boundary.

Run `425` converted the 33 direct real-input gaps into a staging manifest:
nine measured DZT files, fifteen global metadata JSON files, and nine per-file
metadata JSON files. Runs `426-427` validated and sensitivity-hardened that
manifest. This run records that result as the current guarded field claim
state.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/428_gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claim boundary ready:                     true
claims:                                   29
guarded claims:                           25
blocked claims:                           4
direct-intake staging manifest ready:     true
direct real-input slots:                  33
measured DZT files required:              9
global metadata JSON files required:      15
per-file metadata JSON files required:    9
staging actions:                          5
filesystem gaps:                          33
staged real files:                        0
accepted measured-evidence files:         0
template/synthetic allowed rows:          0
real packet files present:                false
real packet accepted:                     false
provenance acceptance ready:              false
archive acceptance ready:                 false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
GPU priority:                             none
```

The new guarded claim records the current real-packet intake shape: 33 direct
real-input slots split into 9 measured DZT files, 15 global metadata JSON
files, and 9 per-file metadata JSON files. It also records the no-evidence
state: zero real files staged, zero measured-evidence files accepted, and zero
template or synthetic substitutions allowed.

## Decision

Use run `428` as the current field claim boundary after the direct-intake
staging manifest. Field evidence, provenance acceptance, archive acceptance,
field FWI, GPU work, and field 3D/HPC remain blocked until real files are
staged and pass the parser, provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_direct_intake_staging_manifest_claim_boundary.py
16 passed
```

Figure check:

```text
3869x886, dynamic range=255
```
