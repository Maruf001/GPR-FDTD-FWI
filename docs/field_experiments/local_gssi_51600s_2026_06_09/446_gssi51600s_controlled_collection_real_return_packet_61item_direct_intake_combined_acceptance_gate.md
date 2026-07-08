# Field Experiment 446: Direct Intake Combined Acceptance Gate

Date: 2026-06-30

## Purpose

Combine the guarded metadata JSON contract and guarded DZT file contract into
one direct-intake acceptance gate.

Runs `440-442` define and guard the 24 metadata JSON files. Runs `443-445`
define and guard the nine DZT files. This run answers the next practical
question:

```text
What complete 33-file state is required before parser, provenance, archive,
field FWI, or field 3D/HPC reruns are allowed?
```

This is a CPU-only synthesis run. It does not create measured files, parse DZT
files, run FDTD, run FWI, use GPU kernels, run field FWI, run 3D/HPC work, or
train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/446_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_file_requirement_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_component_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source metadata contract ready:            true
source metadata validator ready:           true
source metadata sensitivity ready:         true
source DZT contract ready:                 true
source DZT validator ready:                true
source DZT sensitivity ready:              true
total required files:                      33
DZT files required:                        9
metadata JSON files required:              24
DZT check requirements:                    54
metadata field requirements:               129
total file/check/field requirements:       216
real DZT files present now:                0
metadata JSON files present now:           0
accepted files now:                        0
combined gate contract ready:              true
parser acceptance ready:                   false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The acceptance gate has eight components:

| Component | Required | Complete now |
| --- | ---: | ---: |
| DZT files present | 9 | 0 |
| DZT receipt and parser checks | 54 | 0 |
| Metadata JSON files present | 24 | 0 |
| Metadata schema fields | 129 | 0 |
| DZT-metadata links | 9 | 0 |
| Parser acceptance | 33 | 0 |
| Provenance acceptance | 33 | 0 |
| Archive acceptance | 33 | 0 |

## Decision

Use this combined gate before parser, provenance, archive, field FWI, or field
3D/HPC reruns. The current archive remains blocked because no real DZT or
metadata files are present or accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate.py
3 passed
```

Figure check:

```text
2465x845, dynamic range=255
```
