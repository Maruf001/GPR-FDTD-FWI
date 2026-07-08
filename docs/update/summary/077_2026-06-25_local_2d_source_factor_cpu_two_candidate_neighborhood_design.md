# Local 2D Source-Factor CPU Two-Candidate Neighborhood Design

Date: 2026-06-25

## Scope

This checkpoint records output `182`, the design for a two-candidate CPU smoke
after the corrected one-candidate source-factor micro-smoke completed.

## Output

```text
outputs/summary_tables/182_local_2d_source_factor_cpu_two_candidate_neighborhood_design
```

Tracked note:

```text
docs/experiments/892_local_2d_source_factor_cpu_two_candidate_neighborhood_design.md
```

## Result

```text
source micro usable:                     true
predicted runner experiment ID:          1361
requested run name:                      local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1361_local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       2
design validation pass:                  true
recommended cap seconds:                 900
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
single z offset:                         true
single radius offset:                    true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands executed:                       false
two-candidate execution ready:           true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The next bounded execution is justified, but only for this one two-candidate
CPU command. The full source-factor batch, GPU work, and field transfer remain
blocked.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
sha256: 762e4c1ea111cb9533d34072413b04fafa0a9d67ae10f76b7284ebafc30d0851

test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
sha256: 1d99def154d7ef4fdbb38c323f18349457f54c13994d06a3da9b98f38545f12e
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py: pass
tests/test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_two_candidate_neighborhood_design.png
1420x738, dynamic range=255
```

Marathon status: active. The next branch is the capped two-candidate execution
audit.
