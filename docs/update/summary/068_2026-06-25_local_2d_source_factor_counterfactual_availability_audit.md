# Local 2D Source-Factor Counterfactual Availability Audit

Date: 2026-06-25

## Scope

This checkpoint records output `172`, an availability audit for the nine
required full-factorial source-factor counterfactual rows from run `170`.

## Output

```text
outputs/summary_tables/172_local_2d_source_factor_counterfactual_availability_audit
```

Tracked note:

```text
docs/experiments/884_local_2d_source_factor_counterfactual_availability_audit.md
```

## Result

```text
required counterfactual rows:            9
controlled counterfactuals in cache:     0
candidate profile proxy rows:            9
existing runner controls ready:          true
cache reconstruction ready:              false
bounded CPU executor wrapper needed:     true
runner code extension needed:            false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The missing source-factor rows cannot be promoted from cache because no
controlled counterfactual replication cases exist. A bounded CPU wrapper around
the existing coordinate optimizer is the next executable path; it should use
fixed per-variant source frequency/time settings and `--no-fit-amplitude` for
amplitude-isolation rows.

Do not launch new FDTD, GPU work, field transfer, broad source robustness, or
time-zero-only explanation from the current cache.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_counterfactual_availability_audit.py
sha256: 287440fddbc083ba9d32bab10359278f3d1307b8e9f593d5dc5c7a97bcc416ff

test_local_2d_source_factor_counterfactual_availability_audit.py
sha256: d13020d6238bec2d385b10e1667f09a8f1cbee3f3434580bf3151b9211b73096
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_counterfactual_availability_audit.py
4 passed
```

Python compile check:

```text
run_local_2d_source_factor_counterfactual_availability_audit.py: pass
tests/test_local_2d_source_factor_counterfactual_availability_audit.py: pass
```

Figure check:

```text
local_2d_source_factor_counterfactual_availability_audit.png
1420x772, dynamic range=255
```

Marathon status: active. The next branch should design the bounded CPU wrapper
commands without running broad GPU or new FDTD.
