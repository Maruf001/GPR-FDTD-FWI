# Experiment 856: Close-Spacing Matched Source3 Probe Queue

Date: 2026-06-19

## Purpose

Turn the run `855` confound audit into an executable, skip-existing queue for
the only narrow synthetic 2D extension that would support spacing-only
source-density wording.

This is CPU-only queue synthesis. It does not run FDTD, FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/112_close_spacing_matched_source3_probe_queue
```

Key artifacts:

```text
data/close_spacing_matched_source3_probe_queue_summary.json
data/close_spacing_matched_source3_probe_rows.csv
data/close_spacing_matched_source3_probe_family_rows.csv
data/close_spacing_matched_source3_reference_runtime_rows.csv
data/close_spacing_matched_source3_probe_commands.sh
figures/close_spacing_matched_source3_probe_queue.png
figures/FIGURE_NOTES.md
```

## Result

Superseded endpoint note: experiments `857-859` run and aggregate all three
queued `close14_source3_txrx40` seeds (`13`, `21`, and `34`) under a resource
guard. Experiments `860-862` run and aggregate all three reciprocal
`close50_source3_txrx45` seeds. Use
`outputs/summary_tables/120_close_spacing_matched_source3_probe_queue` as the
current queue state.

```text
policy label:                         close_spacing_matched_source3_probe_queue
queue status:                         ready_but_not_launched
probe families:                       2
seed probe count:                     6
existing seed probes:                 0
missing seed probes:                  6
estimated missing GPU runtime:        7732.67 s
estimated missing GPU runtime:        128.88 min
max reference single-seed runtime:    1521.50 s
ready for matched narrow queue:       true
ready for spacing-only claim now:     false
ready for broad GPU queue:            false
maximum parallel GPU jobs:            1
RAM limit:                            80%
GPU utilization limit:                90%
autonomous GPU launch ready:          false
gpu priority:                         narrow_conditional_not_launched
```

Probe families:

| Family | Missing seeds | Estimated runtime | Purpose |
| --- | ---: | ---: | --- |
| `close14_source3_txrx40` | 13, 21, 34 | 57.30 min | match close50 Tx/Rx40 while retaining close14 spacing |
| `close50_source3_txrx45` | 13, 21, 34 | 71.57 min | match close14 Tx/Rx45 while retaining close50 spacing |

## Interpretation

The old close50 `270/280` branch should not be repeated. It was target2-only
and later close50 threshold/source-count evidence already resolved the useful
within-family question.

The only defensible new synthetic 2D extension is a matched source3 control:

```text
close14 source3 Tx/Rx40 seeds 13/21/34
close50 source3 Tx/Rx45 seeds 13/21/34
```

These two families test whether the saved close50/close14 source3 contrast
survives when the Tx/Rx offset is matched both ways. Experiments `857-862`
now complete and aggregate both matched families. The archive supports guarded
acquisition/geometry-aware contrast wording, not a spacing-only causal claim.

The generated command file was intentionally a contract, not an autonomous
launch. Any future GPU extension should use `run_resource_guarded_command.py`,
launch at most one seed at a time, monitor resources, and stop if GPU
utilization would exceed `90%` or RAM would exceed `80%`.

Current endpoint after experiments `857-862`:

```text
current queue output:                 outputs/summary_tables/120_close_spacing_matched_source3_probe_queue
queue status:                         complete_ready_for_aggregation
existing seed probes:                 6
missing seed probes:                  0
missing probes:                       none
estimated remaining GPU runtime:      0.00 min
ready for spacing-only claim now:     false
ready for broad GPU queue:            false
```

Completed matched-control aggregates:

```text
close14 source3 Tx/Rx40 aggregate: outputs/experiments/1351_coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
  truth rows: 6/6
  confidence labels: strong=6
  minimum radius margin abs: 0.003136

close50 source3 Tx/Rx45 aggregate: outputs/experiments/1355_coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
  truth rows: 0/6
  confidence labels: moderate=4, strong=2
  selected branch in all rows: x=299 mm, z=90 mm, r=7.5 mm
```

Interpretation update:

```text
The matched-source3 queue is complete. The result supports a guarded
acquisition/geometry-aware contrast, not a simple spacing-only causal claim.
Close14 source3 survives the matched Tx/Rx40 control; close50 source3 does not
survive the reciprocal Tx/Rx45 control and repeatedly selects a near-truth
wrong branch.
```

## Validation

Focused queue tests:

```text
tests/test_close_spacing_matched_source3_probe_queue.py
4 passed
```

Figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.0423, dynamic range=255
```
