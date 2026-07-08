# Field Experiment 187: Current-To-Controlled Gap Matrix

Date: 2026-06-27

## Purpose

Combine the controlled provenance closure, current archive inventory, and
current QC-evidence synthesis into one strict gap matrix.

This run distinguishes QC context from controlled evidence. It does not relabel
current files as controlled evidence, run field FWI, launch GPU/HPC work, make
a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/187_gssi51600s_current_to_controlled_gap_matrix
```

Key artifacts:

```text
data/field_current_to_controlled_gap_matrix_rows.csv
data/field_current_to_controlled_gap_matrix_summary.json
figures/field_current_to_controlled_gap_matrix.png
docs/FIELD_CURRENT_TO_CONTROLLED_GAP_MATRIX.md
scripts/script_snapshot_manifest.json
```

## Result

```text
closure groups:                       6
metadata closure groups:              3
file closure groups:                  3
current DZT files:                    4
current DZX sidecars:                 4
current archive QC context ready:     true
controlled evidence ready:            false
required real files:                  9
accepted controlled files:            0
remaining real files:                 9
open metadata gaps:                   3
open file gaps:                       3
current files promoted to controlled: 0
measured-field claim ready:           false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

Gap matrix:

| Priority | Closure group | Required files | Accepted files | Remaining files | Gap status |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | session_metadata_real_values | 0 | 0 | 0 | open_metadata_gap |
| 2 | target_truth_provenance | 0 | 0 | 0 | open_metadata_gap |
| 3 | profile_geometry_provenance | 0 | 0 | 0 | open_metadata_gap |
| 4 | acquisition_profile_files | 3 | 0 | 3 | open_file_gap |
| 5 | time_zero_reference_files | 3 | 0 | 3 | open_file_gap |
| 6 | amplitude_reference_files | 3 | 0 | 3 | open_file_gap |

## Interpretation

The current archive is useful QC context: it contains four DZT files and four
DZX sidecars, and the current QC synthesis is ready. None of those files are
promoted to controlled evidence.

The controlled packet still needs three real metadata/provenance closure
records and nine real classified files: three controlled profile repeats, three
time-zero references, and three amplitude references.

## Decision

Use this matrix as the current field-side gap statement. Keep measured-field
claims, field FWI, heavy GPU work, field 3D/HPC, and neural-network training
blocked until the controlled archive is filled and passes the acceptance gates.

## Validation

Focused test:

```text
tests/test_gssi_field_current_to_controlled_gap_matrix.py
3 passed
```

Figure validation:

```text
field_current_to_controlled_gap_matrix.png
2770x851, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_current_to_controlled_gap_matrix.py
sha256=bcb02c920be13700b6e1488a78227393cdd62bba3627afd7ba14d3f23dc70393

tests/test_gssi_field_current_to_controlled_gap_matrix.py
sha256=39c629df459a012f11b24185beeff7db7c98113abd77c4aa3632a27f76447868
```
