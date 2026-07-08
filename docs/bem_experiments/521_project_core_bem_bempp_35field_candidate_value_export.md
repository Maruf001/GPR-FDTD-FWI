# BEM Experiment 521: Bempp 35-Field Candidate Value Export

Date: 2026-06-30

## Purpose

Produce the first Bempp-side candidate return files for the 35-field comparison
schema.

Runs `506-520` established the accepted return-file schema, guarded writer
interface, guarded Bempp exporter interface, guarded FDTD exporter interface,
and final interface-completion boundary. They did not write real returned
values. This run takes the next bounded step: compute Bempp-side candidate
scattered-field norms on the required 31-receiver by nine-frequency grid and
write the two BEM return-file tables in the saved schema.

This is a homogeneous PEC finite-cylinder candidate export. It is not an
accepted BEM/FDTD comparison, not the fine 8x20 reference mesh, not a matched
FDTD return, not a 3D validation claim, not field transfer, and not field FWI.

## Output

```text
outputs/bem_experiments/521_project_core_bem_bempp_35field_candidate_value_export
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_candidate_value_export_candidate_bem_source_hash_manifest.csv
data/project_core_bem_bempp_35field_candidate_value_export_candidate_bem_scattered_norm_values.csv
data/project_core_bem_bempp_35field_candidate_value_export_frequency_rows.csv
data/project_core_bem_bempp_35field_candidate_value_export_summary.json
figures/project_core_bem_bempp_35field_candidate_value_export.png
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate return files:                   2
receiver count:                           31
frequency count:                          9
candidate BEM source-hash entries:        279
candidate BEM scattered-norm entries:     279
candidate source-hash values present:     279
candidate scattered-norm values present:  279
frequency solves ready:                   9
frequency solve failures:                 0
candidate BEM value export ready:         true
accepted BEM return files:                0
accepted real return files:               0
matched FDTD return files present:        false
evidence writer ready:                    false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
```

Candidate scattered-norm range:

```text
minimum: 0.05435364803591665
mean:    0.20767578046348162
maximum: 0.516883390670258
```

The Bempp solves used the local isolated Bempp environment:

```text
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python
```

The total recorded Bempp solve time was about 186 seconds.

## Interpretation

The BEM side has moved from contract-only readiness to candidate-value
production for the required grid. This is a real improvement: the BEM exporter
can now populate the two BEM-side return-file tables with computed values and
lineage hashes.

The result is still not accepted comparison evidence. Three blockers remain:

| Blocker | Current state |
| --- | --- |
| Fine-mesh acceptance | This candidate uses a 4x12 finite-cylinder mesh, not the 8x20 fine-reference mesh. |
| Matched FDTD returns | The two FDTD-side return files are still absent. |
| Evidence writer | The accepted return-file writer remains blocked until both BEM and FDTD values pass provenance and schema checks. |

## Decision

Use run `521` as the current BEM-side candidate-value export checkpoint. The
next useful BEM work is to validate this candidate export from artifacts,
stress-test the validator, and then decide whether to upgrade the candidate
mesh toward the 8x20 fine-reference exporter or build the matched FDTD return
path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_candidate_value_export.py
4 passed
```

Figure check:

```text
2608x845, dynamic range=255
```
