# Field Experiment 289: Claim Boundary After Positive Control Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `288` field claim-boundary validator with controlled
damaged variants.

This run checks that the validator accepts the exact run `287` claim boundary
and rejects damaged variants that alter claim counts, current packet counts,
real measured data state, blocked claims, downstream guardrails, figure
validation, or script snapshots.

This uses saved artifacts only. It does not stage real measured field data,
modify the real return inbox, accept provenance, accept a real archive, run
field FWI, or launch GPU/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/289_gssi51600s_controlled_collection_real_return_claim_boundary_after_positive_control_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_validation_sensitivity_rows.csv
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_validation_sensitivity_summary.json
figures/field_controlled_collection_real_return_claim_boundary_after_positive_control_validation_sensitivity.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_CLAIM_BOUNDARY_AFTER_POSITIVE_CONTROL_VALIDATION_SENSITIVITY.md
```

## Result

```text
scenarios:                    16
expected pass:                1
observed pass:                1
expected failures:            15
observed failures:            15
unexpected outcomes:          0
sensitivity ready:            true
exact run accepted:           true
damaged variants rejected:    true
real measured data present:   false
field FWI ready:              false
field 3D/HPC ready:           false
gpu priority:                 none
```

## Interpretation

The run `288` validator accepts the exact run `287` claim boundary and rejects
controlled damaged variants that alter claim counts, current packet counts, real
measured data state, blocked claims, downstream guardrails, figure validation,
or script snapshots.

## Decision

Use runs `287-289` as the guarded post-positive-control field claim-boundary
block. Continue to block measured evidence, provenance acceptance, field FWI,
3D/HPC, and GPU work until real measured files, metadata, and checksums are
staged and validated.
