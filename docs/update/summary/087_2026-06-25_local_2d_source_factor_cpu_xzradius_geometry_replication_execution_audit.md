# Local 2D Source-Factor CPU X/Z/Radius Geometry-Replication Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records output `192`, the bounded CPU execution audit for the
corrected `max_geometry_instability/time_shift_only` x/z/radius replication
design from run `191`.

## Output

```text
outputs/summary_tables/192_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1364_local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
```

Tracked note:

```text
docs/experiments/900_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.md
```

## Result

```text
audit elapsed seconds:                  748.444
optimizer elapsed seconds:              589.342
exit code:                              0
timed out:                              false
expected candidate count per case:      8
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
full counterfactual execution ready:    false
GPU work ready:                         false
field transfer ready:                   false
```

Optimizer outcome:

| Case | Best x mm | Best z mm | Best radius mm | Best misfit | Radius margin rel | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_geometry_instability_nominal` | 188.0 | 100.0 | 6.0 | 0.479744 | 0.062022 | strong |
| `ff_max_geometry_instability_time_shift_only` | 188.0 | 90.0 | 5.0 | 0.727040 | 0.091388 | strong |

## Decision

This is mixed replication evidence. The time-shift update case reproduces the
truth-depth/truth-radius local candidate, but the nominal companion prefers the
starting depth/radius. Keep the result as bounded, case-label-dependent local
evidence. Do not promote it to full source-factor robustness, full-batch CPU
execution, GPU work, or field transfer.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.py
sha256: f925e20cc6e316591a675e52c98fe5967cb35bc3d2619f991ee2305869425de1

test_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.py
sha256: 5f166b5811d121e6ee2710cd8661d7b6158e3b2d6c12b7efa10e3cfa1faaa3fe
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.py
3 passed
```

Figure checks:

```text
local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.png  1420x738, dynamic range=255
coordinate_confidence_margins.png                                            1804x665, dynamic range=238
coordinate_objective_radius_candidates.png                                    2025x835, dynamic range=238
coordinate_radius_decision_panel.png                                          2129x1583, dynamic range=238
system_scene_geometry.png                                                     1604x1028, dynamic range=255
```

Marathon status: active. The next branch is a result-boundary decision audit
for the source-factor x/z/radius sequence, followed by a refreshed milestone
snapshot audit.
