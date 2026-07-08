# Local 2D Source-Factor CPU X/Radius Mini-Neighborhood Design

Date: 2026-06-25

## Scope

This checkpoint records output `184`, the design for a tiny x/radius CPU smoke
after the two-candidate x-only source-factor run completed.

## Output

```text
outputs/summary_tables/184_local_2d_source_factor_cpu_xradius_mini_neighborhood_design
```

Tracked note:

```text
docs/experiments/894_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.md
```

## Result

```text
source two-candidate usable:             true
predicted runner experiment ID:          1362
requested run name:                      local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1362_local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       4
design validation pass:                  true
recommended cap seconds:                 1800
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
single z offset:                         true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands executed:                       false
x/radius mini execution ready:           true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The x/radius mini-neighborhood is the next bounded execution. The full
source-factor batch, GPU work, and field transfer remain blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
sha256: de477a726152c3080bc68f0d9dc670acd7e8eff5ba4a47ab2cb9674b60122860

test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
sha256: f610caa33a294957a4a01fdb009a1ddb5b513ac37544d6baba1b2d1670e73fdf
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py: pass
tests/test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_xradius_mini_neighborhood_design.png
1420x738, dynamic range=255
```

Marathon status: active. The next branch is the capped x/radius mini execution
audit.
