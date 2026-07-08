# Local 2D Source-Factor CPU X/Z/Radius Local-Neighborhood Design

Date: 2026-06-25

## Scope

This checkpoint records output `187`, the design for an x/z/radius local CPU
smoke after the x/radius mini source-factor run completed.

## Output

```text
outputs/summary_tables/187_local_2d_source_factor_cpu_xzradius_local_neighborhood_design
```

Tracked note:

```text
docs/experiments/896_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.md
```

## Result

```text
source x/radius usable:                  true
predicted runner experiment ID:          1363
requested run name:                      local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1363_local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       8
design validation pass:                  true
recommended cap seconds:                 3600
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
two z candidates:                        true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands executed:                       false
x/z/radius local execution ready:        true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The next bounded execution is justified for this one x/z/radius local
neighborhood. The full source-factor batch, GPU work, and field transfer remain
blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
sha256: eba4f241f5cc5acfc03fd2b7ce7e2fd9f5dd40f33bc707c58cd21c05728d0d2a

test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
sha256: 74880afbd8985084902bf5692975526251fc7a101233178c01a96887b8b4d598
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py: pass
tests/test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_local_neighborhood_design.png
1420x738, dynamic range=255
```

Marathon status: active. The next branch is the capped x/z/radius local
execution audit.
