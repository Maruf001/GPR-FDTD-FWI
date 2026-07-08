# Experiment 897: Local 2D Source-Factor CPU X/Z/Radius Local Execution Audit

Date: 2026-06-25

## Purpose

Execute the x/z/radius local-neighborhood CPU source-factor smoke from run
`187` and audit whether adding a depth competitor moves target `0` toward the
known synthetic truth.

This run executes one bounded CPU command. It does not run the full
nine-command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/188_local_2d_source_factor_cpu_xzradius_local_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1363_local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_cpu_xzradius_local_execution_audit_summary.json
data/local_2d_source_factor_cpu_xzradius_local_execution_required_artifacts.csv
logs/xzradius_local_stdout.txt
logs/xzradius_local_stderr.txt
figures/local_2d_source_factor_cpu_xzradius_local_execution_audit.png
scripts/run_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
scripts/test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested run name:                     local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
expected runner output:                 1363_local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
cap seconds:                            3600
audit elapsed seconds:                  748.947
optimizer elapsed seconds:              597.056
exit code:                              0
timed out:                              false
expected candidate count per case:      8
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

The local neighborhood compared:

```text
x candidates:      188.0, 189.0 mm
z candidates:       85.0,  90.0 mm
radius candidates:   5.0,   6.0 mm
```

Both source cases selected x `189.0` mm, z `90.0` mm, and radius `5.0` mm.

| Case | Candidate count | Best x mm | Best z mm | Best radius mm | Best misfit | Next radius mm | Next radius misfit | Radius margin abs | Radius margin rel | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_amplitude_stress_nominal` | 8 | 189.0 | 90.0 | 5.0 | 0.619105 | 6.0 | 0.681938 | 0.062833 | 0.101490 | strong |
| `ff_max_amplitude_stress_time_shift_only` | 8 | 189.0 | 90.0 | 5.0 | 1.046605 | 6.0 | 1.056842 | 0.010238 | 0.009782 | moderate |

The final target-0 state moved to the local truth candidate:

```text
initial x mm:     188.0, 248.0, 312.0
final x mm:       189.0, 248.0, 312.0
initial z mm:      85.0, 100.0, 95.0
final z mm:        90.0, 100.0, 95.0
initial radii mm:   6.0,   6.0,  6.0
final radii mm:     5.0,   6.0,  6.0
```

## Interpretation

This is a meaningful bounded local result. Adding z made the optimizer choose
the true depth candidate for target `0`, while preserving the x and radius
winner from run `185`. The nominal case has a strong radius margin. The
time-shift-only case still chooses the same local truth candidate, but its
radius confidence drops to moderate, which shows the source perturbation is
affecting the margin even when it does not change the winner.

This is not yet a general robustness claim. It covers one target, one
source-factor family, one objective, and no revisit phase.

## Decision

Do not run the full nine-command source-factor batch, GPU work, or field
transfer. The next defensible source-factor step is bounded replication on
another source-factor row or another target-local neighborhood, starting from a
duplicated run-specific script.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
sha256: 9bfe375d520a2284336c1daa6e53fdc69c642445585cc80088d87f9a09bf8991

test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
sha256: 67222e50f5ecb2c28f1d818e0283072a1d26e3619a65fcc1f329e9308163def1
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_local_execution_audit.py
3 passed
```

Figure checks:

```text
local_2d_source_factor_cpu_xzradius_local_execution_audit.png  1420x738, dynamic range=255
coordinate_confidence_margins.png                             1804x665, dynamic range=238
coordinate_objective_radius_candidates.png                     2025x835, dynamic range=238
coordinate_radius_decision_panel.png                           2129x1583, dynamic range=241
system_scene_geometry.png                                      1586x1028, dynamic range=255
```
