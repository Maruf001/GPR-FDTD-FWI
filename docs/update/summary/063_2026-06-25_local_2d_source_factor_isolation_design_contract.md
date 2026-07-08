# Local 2D Source-Factor Isolation Design Contract

Date: 2026-06-25

## Scope

This checkpoint records output `167`, a local 2D design contract that follows
the matched source/time-zero robustness gate from run `160`.

## Output

```text
outputs/summary_tables/167_local_2d_source_factor_isolation_design_contract
```

Tracked note:

```text
docs/experiments/881_local_2d_source_factor_isolation_design_contract.md
```

## Result

```text
sensitive cases:                         2
design rows:                             12
variant count per case:                  6
gate count:                              4
time-factor rows:                        4
amplitude-factor rows:                   6
frequency-factor rows:                   6
general source/time-zero claim ready:    false
time-zero-only explanation ready:        false
CPU design ready:                        true
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The next scientifically useful local 2D source branch is factorial isolation of
time shift, amplitude scale, and frequency/source scale in the two sensitive
variable-radius cases. Do not promote a time-zero-only explanation, broad source
robustness, field transfer, new FDTD, or GPU work from the current matched-pair
evidence.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_isolation_design_contract.py
sha256: 83a3119a412c2e3f31e41decf6424c89faf462b1796a846bca0962a11f943226

test_local_2d_source_factor_isolation_design_contract.py
sha256: 71e2ce0db3beca319a67544197e867960ed5d6e9f48a80937d278f7c9447fcca
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_isolation_design_contract.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_isolation_design_contract.py: pass
tests/test_local_2d_source_factor_isolation_design_contract.py: pass
```

Figure check:

```text
local_2d_source_factor_isolation_design_contract.png
2104x778, dynamic range=255
```

Marathon status: active. The next branch should refresh the snapshot audit and
then duplicate this design script into the first executable source-factor
isolation run.
