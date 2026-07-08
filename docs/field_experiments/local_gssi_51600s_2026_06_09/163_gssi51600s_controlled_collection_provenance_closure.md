# Field Experiment 163: Controlled Collection Provenance Closure

Date: 2026-06-22

## Purpose

Collapse the raw provenance-gate findings from run `162` into a short list of
field-day closure actions.

Run `162` showed that the dry-run packet is structurally valid but not
provenance-valid. This run answers the next practical question:

```text
What real values and real files are required before the packet can pass
provenance and become measured field evidence?
```

This is CPU-only synthesis. It does not run DZT preprocessing, FDTD, FWI, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/163_gssi51600s_controlled_collection_provenance_closure
```

Key artifacts:

```text
data/field_controlled_collection_provenance_closure_findings.csv
data/field_controlled_collection_provenance_closure_actions.csv
data/field_controlled_collection_provenance_closure_summary.json
figures/field_controlled_collection_provenance_closure.png
docs/FIELD_COLLECTION_PROVENANCE_CLOSURE.md
```

## Result

```text
source structural ready:                  true
source provenance ready:                  false
source provenance findings:               42
closure action groups:                    6
real files required:                      9
controlled profile files required:        3
time-zero reference files required:        3
amplitude-reference files required:       3
placeholder findings:                     32
missing file-reference findings:          9
future-date findings:                     1
current archive can close without data:   false
collection-day execution ready:           true
provenance acceptance ready:              false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The 42 findings reduce to six closure actions:

| Priority | Closure group | Findings | Real files required |
| ---: | --- | ---: | ---: |
| 1 | session metadata real values | 9 | 0 |
| 2 | target truth provenance | 2 | 0 |
| 3 | profile geometry provenance | 1 | 0 |
| 4 | acquisition profile files | 12 | 3 |
| 5 | time-zero reference files | 9 | 3 |
| 6 | amplitude reference files | 9 | 3 |

## Interpretation

The packet problem is now concrete. It is not an abstract validation failure:
the next controlled collection needs one real session record, one real target
truth/provenance record, one real profile-geometry provenance entry, three
controlled profile-repeat files, three time-zero reference files, and three
amplitude-reference files.

The current archive cannot be promoted to measured-field evidence by
relabeling. It needs real measured files and measured metadata, then the
structural validator and provenance gate must be rerun.

## Decision

Use this closure table as the current field-side checkpoint and collection-day
acceptance checklist. Do not launch current-archive field FWI, heavy GPU work,
field 3D/HPC, or neural-network training from the dry-run packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_provenance_closure.py
3 passed
```

Figure validation:

```text
field_controlled_collection_provenance_closure.png:
2263x835, dynamic range=255
```
