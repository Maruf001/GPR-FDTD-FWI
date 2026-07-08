# Field Experiment 261: Controlled Collection Real-Return Staging Contract Validator

Date: 2026-06-28

## Purpose

Validate the saved run `260` controlled collection real-return staging contract
from its output artifacts.

This run checks the file-slot partition, metadata-slot requirements, gate
order, figure validation, script snapshots, and blocked downstream state.

It does not inspect real measured files, accept a real archive, promote field
evidence, run field FWI, or launch field 3D/HPC/GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/261_gssi51600s_controlled_collection_real_return_staging_contract_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_staging_contract_validator_checks.csv
data/field_controlled_collection_real_return_staging_contract_validator_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_staging_contract_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_STAGING_CONTRACT_VALIDATOR.md
scripts/run_gssi_field_controlled_collection_real_return_staging_contract_validator.py
scripts/test_gssi_field_controlled_collection_real_return_staging_contract_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
passed checks:                      7
failed checks:                      0
validation ready:                   true
source contract ready:              true
file slots:                         9
global metadata fields:             11
file metadata cells:                21
checksum requirements:              9
gate rows:                          7
real files present:                 false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The saved run `260` staging contract is internally consistent: file slots,
metadata slots, checksums, and gate order match the guarded collection-return
requirement, while all real-data and downstream states remain blocked.

## Decision

Use runs `260-261` as the validated field real-return staging contract.
Sensitivity testing remains required before treating the validator itself as
guarded.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_staging_contract_validator.py
3 passed
```

Figure validation:

```text
2897x850, dynamic range=255
```
