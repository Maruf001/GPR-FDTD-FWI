# Experiment 895: Local 2D Source-Factor CPU X/Radius Mini Execution Audit

Date: 2026-06-25

## Purpose

Execute the x/radius mini-neighborhood CPU source-factor smoke from run `184`
and audit whether it produces complete optimizer artifacts plus a radius-aware
ranking signal.

This run executes one bounded CPU command. It does not run the full
nine-command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/185_local_2d_source_factor_cpu_xradius_mini_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1362_local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_cpu_xradius_mini_execution_audit_summary.json
data/local_2d_source_factor_cpu_xradius_mini_execution_required_artifacts.csv
logs/xradius_mini_stdout.txt
logs/xradius_mini_stderr.txt
figures/local_2d_source_factor_cpu_xradius_mini_execution_audit.png
scripts/run_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
scripts/test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested run name:                     local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
expected runner output:                 1362_local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
cap seconds:                            1800
audit elapsed seconds:                  426.060
optimizer elapsed seconds:              284.008
exit code:                              0
timed out:                              false
expected candidate count per case:      4
candidate CSV count:                    1
figure file count:                      4
required artifacts present:             6 / 6
complete optimizer output:              true
usable evidence ready:                  true
double prefix detected:                 false
full counterfactual execution ready:    false
new FDTD run ready:                     false
GPU work ready:                         false
field transfer ready:                   false
```

## Optimizer Result

The mini-neighborhood compared:

```text
x candidates:      188.0, 189.0 mm
z candidate:        85.0 mm
radius candidates:   5.0, 6.0 mm
```

Both source cases selected x `189.0` mm and radius `5.0` mm.

| Case | Candidate count | Best x mm | Best z mm | Best radius mm | Best misfit | Next radius mm | Next radius misfit | Radius margin abs | Radius margin rel | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_amplitude_stress_nominal` | 4 | 189.0 | 85.0 | 5.0 | 0.849183 | 6.0 | 0.958038 | 0.108855 | 0.128188 | strong |
| `ff_max_amplitude_stress_time_shift_only` | 4 | 189.0 | 85.0 | 5.0 | 1.118763 | 6.0 | 1.194492 | 0.075729 | 0.067690 | strong |

The final target-0 state moved toward the known truth:

```text
initial x mm:     188.0, 248.0, 312.0
final x mm:       189.0, 248.0, 312.0
initial radii mm:   6.0,   6.0,   6.0
final radii mm:     5.0,   6.0,   6.0
```

## Interpretation

The source-factor branch now has a bounded CPU result with a radius-aware
margin. The time-shift-only source perturbation did not overturn the local
selection for this target and case: both nominal and perturbed cases select the
same x/radius candidate, and both radius margins are labeled `strong`.

This is still not a general source-factor robustness result. It covers one
target, one source-factor case family, one z value, one objective, and no
revisit phase. It is evidence that the bounded CPU path is practical and that a
small radius-aware neighborhood can produce useful margins.

## Decision

Do not jump to the full nine-command batch, GPU work, or field transfer. The
next defensible branch is a bounded replication or slightly wider local
neighborhood, using a duplicated run-specific script and preserving the
numeric-free `--run-name` convention.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
sha256: 7add5722dc040e4e27a66a4126e6f382c4dc13fbf0061727c8782b8356a9d8c9

test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
sha256: f18b60a0f625dc71f5670a65c6293cce64be1c22113fd05b7b9ae7dc1b71d27d
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xradius_mini_execution_audit.py
3 passed
```

Figure checks:

```text
local_2d_source_factor_cpu_xradius_mini_execution_audit.png  1420x738, dynamic range=255
coordinate_confidence_margins.png                           1804x665, dynamic range=238
coordinate_objective_radius_candidates.png                   2025x835, dynamic range=238
coordinate_radius_decision_panel.png                         2129x1583, dynamic range=241
system_scene_geometry.png                                    1574x1028, dynamic range=255
```
