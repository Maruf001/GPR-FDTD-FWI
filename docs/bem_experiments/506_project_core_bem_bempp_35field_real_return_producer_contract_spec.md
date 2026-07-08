# BEM Experiment 506: Bempp 35-Field Real-Return Producer Contract Spec

Date: 2026-06-30

## Purpose

Make the exact 35-field BEM/FDTD real-return producer contract explicit.

Runs `500-505` showed that the templates, consumers, and historical Bempp
metadata are useful, but no exact producer writes the accepted real-return
files. This run converts that blocker into a concrete implementation contract:
which files must be written, what schema they must use, and which producer
scripts are missing.

## Output

```text
outputs/bem_experiments/506_project_core_bem_bempp_35field_real_return_producer_contract_spec
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_producer_rows.csv
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_schema_rows.csv
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_implementation_blocker_rows.csv
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_summary.json
figures/project_core_bem_bempp_35field_real_return_producer_contract_spec.png
scripts/script_snapshot_manifest.json
```

## Result

```text
producer contract spec ready:              true
required return files:                     4
required real entries:                     1116
required scorecard rows:                   279
schema contract rows:                      4
schema contract ready:                     true
implementation blockers:                  3
BEM exporter available:                    false
FDTD exporter available:                   false
return-file writer available:              false
exact Bempp producer candidates:           0
Bempp-tagged 31x9 metadata matches:        1
real return production ready:              false
real BEM/FDTD comparison ready:            false
3D validation ready:                       false
GPU/HPC ready:                             false
field FWI ready:                           false
GPU priority:                              none
```

The four required files are:

| File | Producer | Rows | Required value |
| --- | --- | ---: | --- |
| `fdtd_source_hash_manifest.csv` | FDTD | 279 | returned FDTD source hash |
| `bem_source_hash_manifest.csv` | BEM | 279 | returned BEM source hash |
| `fdtd_scattered_norm_values.csv` | FDTD | 279 | returned FDTD scattered-field norm |
| `bem_scattered_norm_values.csv` | BEM | 279 | returned BEM scattered-field norm |

The three missing implementation pieces are:

| Blocker | Affected files | Required script |
| --- | ---: | --- |
| FDTD exporter missing | 2 | `run_project_core_fdtd_35field_real_return_exporter.py` |
| BEM exporter missing | 2 | `run_project_core_bem_bempp_35field_real_return_exporter.py` |
| Accepted return-file writer missing | 4 | `run_project_core_bem_fdtd_35field_real_return_files_writer.py` |

## Decision

Use this contract as the implementation target for the real-return producer
branch. Do not rerun the real return-file acceptance gate or promote real
BEM/FDTD comparison evidence until the exporter and writer scripts exist and
produce accepted real files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec.py
4 passed
```

Figure check:

```text
2410x845, dynamic range=255
```
