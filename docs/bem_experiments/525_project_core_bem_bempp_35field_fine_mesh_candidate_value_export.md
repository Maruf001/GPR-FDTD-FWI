# BEM Experiment 525: Bempp 35-Field Fine-Mesh Candidate Value Export

Date: 2026-06-30

## Purpose

Run the full 8x20 Bempp-side candidate value export over the required
31-receiver by nine-frequency grid.

Run `524` showed that the 8x20 mesh is feasible at the 400 MHz and 3 GHz
endpoints and that the high-frequency response changes materially from the
4x12 smoke mesh. This run applies the 8x20 mesh to all nine frequencies and
writes the two BEM-side candidate return-file tables.

## Output

```text
outputs/bem_experiments/525_project_core_bem_bempp_35field_fine_mesh_candidate_value_export
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_candidate_bem_source_hash_manifest.csv
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_candidate_bem_scattered_norm_values.csv
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_frequency_rows.csv
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_summary.json
figures/project_core_bem_bempp_35field_fine_mesh_candidate_value_export.png
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                          9
receiver count:                           31
candidate return files:                   2
candidate BEM source-hash entries:        279
candidate BEM scattered-norm entries:     279
candidate source-hash values present:     279
candidate scattered-norm values present:  279
frequency solves ready:                   9
frequency solve failures:                 0
fine mesh matches 8x20 reference:         true
fine-mesh candidate export ready:         true
accepted BEM return files:                0
accepted real return files:               0
matched FDTD return files present:        false
accepted evidence ready:                  false
real BEM/FDTD comparison ready:           false
```

Candidate scattered-norm range:

```text
minimum: 0.056617878872083346
mean:    0.18989628517914978
maximum: 0.42334644432527074
```

The full nine-frequency solve took about 192 seconds.

## Interpretation

The BEM side now has complete 8x20 fine-mesh candidate values in the 35-field
return-file schema. This closes the BEM-side mesh blocker that remained after
run `521`.

The result remains candidate-only. The matched FDTD-side source-hash and
scattered-norm return files are still absent, and the accepted evidence writer
must remain blocked until both sides exist and pass schema/provenance checks.

## Decision

Use run `525` as the current BEM-side value-export checkpoint. The next useful
BEM work is to validate and sensitivity-harden this fine-mesh candidate export,
then turn to the matched FDTD return-file path or an accepted-writer gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export.py
5 passed
```

Figure check:

```text
2608x845, dynamic range=255
```
