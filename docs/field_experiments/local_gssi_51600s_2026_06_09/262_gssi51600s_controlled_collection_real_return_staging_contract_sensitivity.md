# Field Experiment 262: Controlled Collection Real-Return Staging Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `261` validator for the run `260` controlled collection
real-return staging contract.

This run checks whether the validator accepts the exact saved run `260`
contract and rejects controlled damage to file slots, metadata slots, gate
order, summary counts, input readiness, downstream readiness, figure
validation, and script snapshots.

It does not inspect real measured files, accept a real archive, promote field
evidence, run field FWI, or launch field 3D/HPC/GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/262_gssi51600s_controlled_collection_real_return_staging_contract_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_staging_contract_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_staging_contract_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_staging_contract_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_STAGING_CONTRACT_SENSITIVITY.md
scripts/run_gssi_field_controlled_collection_real_return_staging_contract_sensitivity.py
scripts/test_gssi_field_controlled_collection_real_return_staging_contract_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          37
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         36
observed failure scenarios:         36
unexpected outcomes:                0
sensitivity ready:                  true
exact run 260 accepted:             true
damaged variants rejected:          true
real files present:                 false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The validator accepts the exact run `260` staging contract and rejects every
damaged variant. The rejected cases cover file-slot drift, metadata-slot drift,
gate-order drift, summary-count drift, premature real-data or downstream
promotion, figure validation drift, and script-snapshot drift.

## Decision

Use runs `260-262` as the guarded controlled field real-return staging
contract. Real measured files and metadata remain required before archive
acceptance or downstream field work.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_staging_contract_sensitivity.py
3 passed
```

Figure validation:

```text
4031x890, dynamic range=255
```
