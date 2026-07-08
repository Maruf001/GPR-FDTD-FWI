# BEM Experiment 729: Producer Input Strict-Contract Handoff Template Pack

Date: 2026-07-01

## Purpose

Create updated matched-FDTD producer input templates after strict contract-hash
acceptance was added to the shared exporter.

The earlier handoff templates left `input_contract_sha256` blank. That was
appropriate before the exact-hash policy was defined, but runs `717-728` now
define and validate the exact hashes. This run pre-fills those hashes and
leaves only real solver provenance and returned FDTD values blank.

This is CPU-only template generation. It does not run FDTD, write live producer
files, execute the exporter on live files, create real evidence, run a real
BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation claims.

## Output

```text
outputs/bem_experiments/729_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack
```

Key artifacts:

```text
data/strict_contract_matched_fdtd_producer_input_templates/
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_action_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
template files:                         2
template rows:                        558
columns per template:                  11
prefilled exact contract hashes:      558
blank real solver provenance cells:  2232
blank returned FDTD values:           558
live input files present:               0
template live evidence files:           0
completed actions:                      1
exporter execution ready:           false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                      false
```

## Interpretation

The templates now remove one avoidable source of producer error: the exact
contract hash is prefilled for every required row. The files are still handoff
templates only because the real solver run identifiers, solver statuses, solver
log hashes, real-export flags, and returned FDTD values remain blank.

## Decision

Use these templates for future matched-FDTD producer handoff. Do not treat them
as live evidence or exporter-ready inputs.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack.py
3 passed
```

Figure check:

```text
2285x844, dynamic range=255
```
