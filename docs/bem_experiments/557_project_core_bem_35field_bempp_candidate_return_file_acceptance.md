# BEM Experiment 557: Bempp Candidate Return File Acceptance

Date: 2026-06-30

## Purpose

Promote the real fine-mesh Bempp candidate values from run `525` into two
schema-conforming BEM-side return CSV files for the 35-field comparison track.

Run `525` solved the BEM side on the 8-by-20 finite-cylinder mesh and produced
candidate values for 31 receivers across 9 frequencies. This run checks those
values against the return-file schema from run `506`, writes accepted BEM-side
return files, and keeps the matched-FDTD and downstream gates closed.

This is CPU-only file acceptance. It does not rerun Bempp, run FDTD, write FDTD
return files, compare BEM with FDTD, launch GPU/HPC work, or promote field
transfer.

## Output

```text
outputs/bem_experiments/557_project_core_bem_35field_bempp_candidate_return_file_acceptance
```

Key artifacts:

```text
data/accepted_bempp_return_files/bem_source_hash_manifest.csv
data/accepted_bempp_return_files/bem_scattered_norm_values.csv
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_acceptance_rows.csv
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_summary.json
figures/project_core_bem_35field_bempp_candidate_return_file_acceptance.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source candidate ready:                    true
accepted BEM return files:                 2 / 2
accepted BEM return rows:                  558 / 558
accepted source-hash rows:                 279
accepted scattered-norm rows:              279
unique source-hash identities:             279
unique scattered-norm identities:          279
source-hash value domain accepted:         true
scattered-norm value domain accepted:      true
accepted norm min:                         0.056617878872083346
accepted norm mean:                        0.18989628517914978
accepted norm max:                         0.42334644432527074
matched-FDTD return files:                 0
BEM/FDTD comparison ready:                 false
3D validation claim ready:                 false
field transfer ready:                      false
GPU priority:                              none
```

## Interpretation

The BEM half of the future 35-field comparison is no longer only a candidate
table. It now has two accepted return files with 279 source hashes and 279
positive scattered-field norms.

This does not close the comparison. The FDTD half is still absent, so
BEM/FDTD comparison evidence, 3D validation claims, field transfer, field FWI,
and GPU/HPC escalation remain blocked.

## Decision

Use run `557` as the accepted BEM-side return-file source for the future
35-field comparison. The next BEM-side work should either validate this
acceptance more aggressively or produce the two matched-FDTD return CSV files
required by runs `555` and `556`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance.py
5 passed
```

Figure check:

```text
2537x841, dynamic range=255
```
