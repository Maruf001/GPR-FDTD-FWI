# Field Experiment 340: Current 61-Item Field Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `339` field claim-boundary validator with controlled
damaged variants.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/340_gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          15
expected pass:                      1
observed pass:                      1
expected failures:                  14
observed failures:                  14
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 338:              true
rejects damaged variants:           true
claims:                             15
guarded claims:                     11
blocked claims:                     4
packet items required:              61
metadata requirements:              36
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The validator accepts exact run `338` artifacts and rejects damaged variants for
claim-count drift, refreshed-row drift, packet-count drift, source-readiness
drift, downstream promotion, GPU-priority drift, figure-validation drift, and
script-snapshot drift.

## Decision

Use runs `338-340` as the current guarded 61-item field claim-boundary block.
Measured-packet acquisition remains the field-side blocker.

## Validation

Focused sensitivity test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3617x904, dynamic range=255
```
