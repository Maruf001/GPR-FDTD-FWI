# Field Experiment 271: Controlled Collection Fill Packet Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `270` validator for the run `269` collection-day fill
packet.

The exact run `269` worklist should pass. Damaged copies should fail when file
rows, metadata rows, checksum rows, acceptance gates, downstream summary
states, figure validation, or script snapshots drift.

This run uses saved artifacts only. It does not ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/271_gssi51600s_controlled_collection_real_return_collection_day_fill_packet_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_fill_packet_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_collection_day_fill_packet_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_fill_packet_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_FILL_PACKET_SENSITIVITY.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_fill_packet_sensitivity.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                           14
expected pass scenarios:              1
observed pass scenarios:              1
expected failure scenarios:          13
observed failure scenarios:          13
unexpected outcomes:                  0
fill packet sensitivity ready:        true
exact run 269 accepted:               true
damaged variants rejected:            true
provenance acceptance ready:          false
real archive acceptance ready:        false
controlled evidence ready:            false
field FWI ready:                      false
field 3D/HPC ready:                   false
GPU priority:                         none
```

Sensitivity coverage:

| Scenario | Expected | Observed | Failed check |
| --- | --- | --- | --- |
| exact run 269 fill packet | pass | pass | none |
| file row removed | fail | fail | source policy and counts |
| file false presence | fail | fail | real DZT file requirement |
| placeholder allowed | fail | fail | real DZT file requirement |
| metadata row removed | fail | fail | source policy and counts |
| metadata false fill | fail | fail | measured metadata requirement |
| checksum row removed | fail | fail | source policy and counts |
| checksum false fill | fail | fail | checksum requirement |
| gate ready true | fail | fail | blocked acceptance gates |
| gate status drift | fail | fail | blocked acceptance gates |
| summary provenance ready | fail | fail | blocked downstream summary |
| summary field FWI ready | fail | fail | blocked downstream summary |
| figure blank | fail | fail | nonblank figure requirement |
| script snapshot count zero | fail | fail | script snapshot requirement |

## Interpretation

The validator accepts the exact run `269` worklist and rejects every damaged
variant tested here. The guarded field state is therefore precise: the packet
is a collection-day worklist that must be filled with real measured files,
measured metadata, and checksums before any provenance acceptance or downstream
field use.

## Decision

Use runs `269-271` as the guarded collection-day fill-packet block. The current
archive remains unaccepted field evidence and does not justify field FWI,
field 3D/HPC, heavy GPU work, or neural-network training.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet_sensitivity.py
3 passed
```

Figure validation:

```text
3257x877, dynamic range=255
```
