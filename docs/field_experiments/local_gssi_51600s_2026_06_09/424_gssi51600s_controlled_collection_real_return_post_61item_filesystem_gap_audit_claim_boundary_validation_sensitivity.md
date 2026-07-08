# Field Experiment 424: Post Filesystem-Gap-Audit Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `423` validator against controlled damage to the run `422`
claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/424_gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                      32
expected pass scenarios:                    1
observed pass scenarios:                    1
expected failure scenarios:                 31
observed failure scenarios:                 31
unexpected outcomes:                        0
validation sensitivity ready:               true
validator accepts exact run 422:            true
validator rejects damaged variants:         true
real packet files present:                  false
real packet accepted:                       false
controlled field evidence ready:            false
field FWI ready:                            false
field 3D/HPC ready:                         false
GPU priority:                               none
```

The damaged variants cover claim-count drift, audit-readiness drift, metric
drift, source sensitivity drift, premature real-file and evidence promotion,
downstream promotion, GPU-priority drift, claim-row damage, blocked-row damage,
figure damage, and script-snapshot damage.

## Decision

Use runs `422-424` as the guarded post-filesystem-gap field claim-boundary
block. The next field progress still requires real measured packet files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3797x918, dynamic range=255
```
