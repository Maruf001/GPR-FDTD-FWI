# Local 2D Source/Time-Zero Replay Contract

Date: 2026-06-25

## Scope

Turn the broad run `144` source/time-zero audit into a concrete CPU replay
contract over representative cached diagnostics.

This does not run FDTD, GPU kernels, field FWI, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/summary_tables/145_local_2d_source_time_zero_replay_contract
```

Tracked experiment note:

```text
docs/experiments/876_local_2d_source_time_zero_replay_contract.md
```

## Result

```text
source diagnostic files:             648
selected cases:                      5
contract metrics:                    4
contract metrics passed:             4
selected max abs time shift ps:      50.0
selected max amplitude deviation %:  48.64359318220286
selected max unique geometries:      11
CPU replay contract ready:           true
new FDTD run ready:                  false
GPU work ready:                      false
field transfer ready:                false
```

## Interpretation

The replay contract is ready for a CPU-only follow-up. It selects five cached
diagnostics that span high amplitude stress, high geometry instability, stable
50 ps shift, a close14 fixed-radius-like case, and a low-effect control.

## Decision

Use run `145` as the source/time-zero replay contract. Keep new FDTD, GPU work,
field transfer, field FWI, and 3D/HPC blocked unless the CPU replay exposes a
decision-changing gap that cached diagnostics cannot answer.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_replay_contract.py
3 passed
```

Figure check:

```text
2428x778, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_replay_contract.py
sha256=b9b4eb93357f9a243bc988014aef8c620ae0eb7e1fd22fec84d0c9ae8237a5c0

test_local_2d_source_time_zero_replay_contract.py
sha256=44c6310d8c154157a2baff111c11d58b346131ff22726a5b553552eb9f55e8b5
```

## Next Marathon Branch

The marathon remains active. The next useful branch is to execute the CPU
replay analysis over the five selected cached diagnostics and report whether
source/time-zero uncertainty changes geometry decisions enough to require new
simulation.
