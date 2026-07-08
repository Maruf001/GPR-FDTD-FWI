# Field Experiment 304: Real-Return Packet Gap Claim Boundary Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `303` claim-boundary validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `302` field claim
boundary and rejects damaged variants covering claim counts, guarded support
states, claim rows, packet gap counts, false field-state promotion, GPU
priority, figure validation, and script snapshots.

It does not stage measured field data, modify the real return inbox, accept
provenance, accept a real archive, run field FWI, launch GPU work, or start
3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/304_gssi51600s_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity_scenario_rows.csv
data/field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity_summary.json
figures/field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_GAP_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                  26
expected pass:              1
observed pass:              1
expected failures:          25
observed failures:          25
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 302:      true
rejects damaged variants:   true
real measured data present: false
real return execution ready:false
field evidence ready:       false
field FWI ready:            false
field 3D/HPC ready:         false
gpu priority:               none
```

## Interpretation

The validator accepts the exact run `302` claim boundary and rejects damaged
variants covering claim counts, guarded support states, claim rows, packet gap
counts, false field-state promotion, GPU priority, figure validation, and
script snapshots.

## Decision

Use runs `302-304` as the guarded field real-return packet gap claim-boundary
block. The next field-side action remains measured packet staging and
revalidation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_real_return_packet_gap_claim_boundary_validation_sensitivity.py: pass
```

Figure validation:

```text
3797x922, dynamic range=255
```
