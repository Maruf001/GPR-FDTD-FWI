# BEM Experiment 711: Producer Input Handoff Template Pack

Date: 2026-06-30

## Purpose

Create a non-live handoff packet for the two matched-FDTD producer input CSV
files required by the current 35-field BEM/FDTD bridge.

Runs `708-710` showed that the external staging directories exist, but the two
producer input files are absent. This run writes fillable template CSV files
inside the experiment output folder only. It does not write into the live
external staging path.

This is CPU-only template generation and readiness auditing. It does not run
FDTD, execute the input-bound exporter, create accepted return files, run a
real BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation claims.

## Output

```text
outputs/bem_experiments/711_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack
```

Key artifacts:

```text
data/matched_fdtd_producer_input_templates/fdtd_source_hash_manifest_real_input_template.csv
data/matched_fdtd_producer_input_templates/fdtd_scattered_norm_values_real_input_template.csv
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_action_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
template files:                      2
template rows:                       558
columns per template:                11
target live parent paths present:    2
target live input files present:     0
blank solver-provenance cells:       2790
blank required FDTD value cells:     558
real FDTD value count:               0
template live evidence count:        0
complete actions:                    0
exporter execution ready:            false
new FDTD executed:                   false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

## Interpretation

The BEM/FDTD bridge now has an explicit handoff packet for the external
matched-FDTD producer. The packet locks the 558 row identities and column names
but leaves all real solver provenance and real FDTD values blank.

The live external input files remain absent, so this is not evidence and does
not unlock exporter execution.

## Decision

Use these templates to guide real matched-FDTD production. Keep exporter
execution, real BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field
transfer, and field FWI blocked until the live files are filled, staged, and
accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack.py
4 passed
```

Figure check:

```text
2573x848, dynamic range=255
```
