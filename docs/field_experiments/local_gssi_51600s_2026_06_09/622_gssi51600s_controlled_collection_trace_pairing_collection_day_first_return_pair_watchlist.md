# Field Experiment 622: Controlled Collection First-Return Pair Watchlist

Date: 2026-07-01

## Purpose

Turn the controlled collection file-slot manifest and clean external return
tree into a nine-pair intake watchlist.

Each pair contains one measured DZT file and one paired metadata JSON file.
This run does not create measured files, parse DZT files, run field FWI, or
launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/622_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_pair_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist.png
```

## Result

```text
source manifest ready:                  true
source hygiene ready:                   true
source hygiene validation ready:        true
source hygiene sensitivity ready:       true
DZT/metadata pair count:                9
required DZT files:                     9
required metadata files:                9
complete pairs:                         0
partial pairs:                          0
DZT files present:                      0
metadata files present:                 0
collection-coupled slots:               18
external return root exists:            true
external tree clean:                    true
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
```

The nine pairs are:

```text
controlled_profile_repeat_01
controlled_profile_repeat_02
controlled_profile_repeat_03
time_zero_reference_01
time_zero_reference_02
time_zero_reference_03
amplitude_reference_01
amplitude_reference_02
amplitude_reference_03
```

## Interpretation

The return tree is ready to receive files, but it still contains no measured
field data. The watchlist makes the first acceptance rule explicit: a measured
DZT file and its paired metadata JSON must arrive together before that pair can
be considered complete.

## Decision

Use this as the first-return intake watchlist. Keep controlled field evidence,
field FWI, and field 3D/HPC blocked until measured pairs are present and pass
preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist.py
3 passed
```

Figure check:

```text
2934x870, dynamic range=255
```
