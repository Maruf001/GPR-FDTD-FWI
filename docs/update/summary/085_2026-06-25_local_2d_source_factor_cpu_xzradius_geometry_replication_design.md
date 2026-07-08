# Local 2D Source-Factor CPU X/Z/Radius Geometry-Replication Design

Date: 2026-06-25

## Scope

This checkpoint records output `190`, a no-go design for
`max_geometry_instability/time_shift_only` replication.

## Output

```text
outputs/summary_tables/190_local_2d_source_factor_cpu_xzradius_geometry_replication_design
```

Tracked note:

```text
docs/experiments/898_local_2d_source_factor_cpu_xzradius_geometry_replication_design.md
```

## Result

```text
replication case category:               max_geometry_instability
replication variant:                     time_shift_only
expected candidate count per case:       8
design validation pass:                  false
revisit disabled:                        false
commands executed:                       false
replication execution ready:             false
full counterfactual execution ready:     false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Do not execute the run `190` command. The selected source row carried revisit
flags from the original numbered command table. The next branch is a duplicated
corrected design script that strips revisit flags/options.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
sha256: 950747e98c8041094b03abe33caceeabb22f72017c223b64e879ea9bd65a5ce3

test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
sha256: 0efdac7d532bd30923c946010a75aa9189ffdcefe26710e56e26d1164e10db9c
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py: pass
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_geometry_replication_design.png
1420x738, dynamic range=255
```

Marathon status: active. Continue by correcting the design before execution.
