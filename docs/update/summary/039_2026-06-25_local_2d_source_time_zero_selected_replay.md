# Local 2D Source/Time-Zero Selected Replay

Date: 2026-06-25

## Scope

Execute the run `145` CPU replay contract over five selected cached
coordinate-objective diagnostics.

This does not run FDTD, GPU kernels, field FWI, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/summary_tables/146_local_2d_source_time_zero_selected_replay
```

Tracked experiment note:

```text
docs/experiments/877_local_2d_source_time_zero_selected_replay.md
```

## Result

```text
selected cases:                  5
selected rows:                   42
decision-sensitive cases:        2
geometry-stable cases:           3
max geometry span mm:            126.12394697280925
max time-shift span ps:          50.0
max amplitude span percent:      56.284751892158646
CPU replay complete:             true
new FDTD run ready:              false
GPU work ready:                  false
field transfer ready:            false
```

## Interpretation

The replay result is mixed and useful:

```text
decision-sensitive: broad variable-radius cached cases
stable:             selected close10, close14, and low-effect control cases
```

The immediate next improvement is claim/gate language around source/time-zero
robustness, not new compute.

## Decision

Use run `146` to scope source/time-zero robustness metrics. Keep new FDTD, GPU
work, detector-FWI, field transfer, field FWI, and 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_selected_replay.py
3 passed
```

Figure check:

```text
2464x778, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_selected_replay.py
sha256=0ebbf1c10171082deeaea21ba52de65e4c9791c4ab40f330a092e9196ec96756

test_local_2d_source_time_zero_selected_replay.py
sha256=ce45551fbdf12b39fb365e95a26d5933bedec906d4479dfcc3939c32b8f37f22
```

## Next Marathon Branch

The marathon remains active. The next useful branch is a robustness-gate or
claim-boundary update that consumes run `146` and prevents source/time-zero
sensitive cases from being overclaimed.
