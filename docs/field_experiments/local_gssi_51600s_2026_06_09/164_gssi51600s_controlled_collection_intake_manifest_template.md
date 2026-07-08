# Field Experiment 164: Controlled Collection Intake Manifest Template

Date: 2026-06-25

## Purpose

Turn the run `163` provenance-closure actions into a fillable field-day intake
manifest.

Run `163` made the blocker concrete: six closure groups, 11 real metadata
values, and nine real files. This run creates the practical intake sheet for
capturing those values and files during collection.

This is a planning and provenance-control artifact. It does not run DZT
preprocessing, FDTD, FWI, GPU kernels, field FWI, field 3D/HPC work, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/164_gssi51600s_controlled_collection_intake_manifest_template
```

Key artifacts:

```text
data/field_controlled_collection_intake_manifest_template.csv
data/field_controlled_collection_acceptance_checks.csv
data/field_controlled_collection_intake_manifest_summary.json
figures/field_controlled_collection_intake_manifest.png
docs/FIELD_COLLECTION_INTAKE_MANIFEST_TEMPLATE.md
```

## Result

```text
manifest rows:                  20
metadata values required:        11
real files required:             9
controlled profile files:        3
time-zero reference files:       3
amplitude reference files:       3
closure groups:                  6
ready for collection-day use:    true
ready for provenance acceptance: false
ready for field FWI:             false
ready for GPU work:              false
```

The manifest rows cover:

| Group | Metadata values | Real files |
| --- | ---: | ---: |
| session metadata real values | 8 | 0 |
| target truth provenance | 2 | 0 |
| profile geometry provenance | 1 | 0 |
| acquisition profile files | 0 | 3 |
| time-zero reference files | 0 | 3 |
| amplitude reference files | 0 | 3 |

## Interpretation

The field-side blocker is now operationally actionable. The next field day
needs to fill this manifest with measured values, actual file paths, checksums,
operator initials, and collection timestamps. After that, the structural
validator and provenance gate must be rerun.

## Decision

Use this run as the current field-side collection-day intake template. It does
not make the dry-run packet valid and does not justify field FWI, heavy GPU
work, field 3D/HPC, or neural-network training.

## Validation

```text
python -m py_compile run_gssi_field_controlled_collection_intake_manifest_template.py
conda run -n gpr-fdtd-fwi python run_gssi_field_controlled_collection_intake_manifest_template.py
```

Figure check:

```text
1 PNG figure, nonblank dynamic range, 1870x842
```
