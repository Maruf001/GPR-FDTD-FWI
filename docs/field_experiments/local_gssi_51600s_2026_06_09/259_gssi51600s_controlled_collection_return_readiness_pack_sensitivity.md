# Field Experiment 259: Controlled Collection Return Readiness Pack Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `258` validator for the controlled-collection
return-readiness pack.

This run checks whether the validator accepts the exact saved run `257` pack
and rejects controlled damage to collection rows, support rows, blocker rows,
file counts, guard flags, and downstream readiness states.

This run does not execute future real-archive commands, inspect real measured
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/259_gssi51600s_controlled_collection_return_readiness_pack_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_return_readiness_pack_sensitivity_scenarios.csv
data/field_controlled_collection_return_readiness_pack_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_return_readiness_pack_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_RETURN_READINESS_PACK_SENSITIVITY.md
scripts/run_gssi_field_controlled_collection_return_readiness_pack_sensitivity.py
scripts/test_gssi_field_controlled_collection_return_readiness_pack_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         48
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        47
observed failure scenarios:        47
unexpected outcomes:               0
sensitivity ready:                 true
pack validation ready:             true
collection-return pack ready:      true
collection action groups:          6
real files required:               9
real files present:                false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The collection-return pack validator accepts the exact run `257` pack and
rejects 47 damaged variants. The rejected cases cover collection-row drift,
support/blocker drift, real-file count drift, guard-readiness drift, premature
real-file or provenance acceptance, real-archive acceptance, controlled-field
evidence promotion, field-FWI promotion, field-3D/HPC promotion, and GPU
promotion.

## Decision

Use runs `257-259` as the guarded controlled field collection-return readiness
pack. Real measured files and real measured metadata remain required before
archive acceptance or downstream field work.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_return_readiness_pack_sensitivity.py
5 passed
```

Figure validation:

```text
4445x905, dynamic range=255
```
