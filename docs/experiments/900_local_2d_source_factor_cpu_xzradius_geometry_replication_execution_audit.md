# Experiment 900: Local 2D Source-Factor CPU X/Z/Radius Geometry-Replication Execution Audit

Date: 2026-06-25

## Purpose

Execute the corrected geometry-instability replication command from run `191`
and audit whether the bounded x/z/radius local neighborhood from run `188`
replicates on a different source-factor stress family.

This run executes one bounded CPU command. It does not run the full
nine-command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/192_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1364_local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit_summary.json
data/local_2d_source_factor_cpu_xzradius_geometry_replication_execution_required_artifacts.csv
logs/xzradius_geometry_replication_stdout.txt
logs/xzradius_geometry_replication_stderr.txt
figures/local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.png
scripts/run_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.py
scripts/test_local_2d_source_factor_cpu_xzradius_geometry_replication_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested run name:                     local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
expected runner output:                 1364_local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
cap seconds:                            3600
audit elapsed seconds:                  748.444
optimizer elapsed seconds:              589.342
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
z candidates:       90.0, 100.0 mm
radius candidates:   5.0,   6.0 mm
```

The update case was `ff_max_geometry_instability_time_shift_only`. It selected
the truth-depth/truth-radius local candidate:

```text
final x mm:       188.0, 248.0, 312.0
final z mm:        90.0,  90.0, 95.0
final radii mm:     5.0,   6.0,  6.0
```

The nominal companion did not replicate the same geometry. It preferred the
initial-depth/initial-radius candidate.

| Case | Candidate count | Best x mm | Best z mm | Best radius mm | Best misfit | Next radius mm | Next radius misfit | Radius margin abs | Radius margin rel | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_geometry_instability_nominal` | 8 | 188.0 | 100.0 | 6.0 | 0.479744 | 5.0 | 0.509499 | 0.029755 | 0.062022 | strong |
| `ff_max_geometry_instability_time_shift_only` | 8 | 188.0 | 90.0 | 5.0 | 0.727040 | 6.0 | 0.793483 | 0.066443 | 0.091388 | strong |

## Interpretation

This is usable but mixed replication evidence. The time-shift-only
geometry-instability case moves target `0` to the truth-depth/truth-radius
local candidate with a strong radius margin. That supports the bounded
time-shift branch.

It does not support a broad source-factor robustness claim. The nominal
companion in the same geometry-instability family prefers the starting
geometry, so the current x/z/radius local result is stress-family and
case-label dependent.

## Decision

Do not run the full nine-command source-factor batch, GPU work, or field
transfer from this result. The next defensible source-factor step is a decision
audit that separates update-case success from companion-case disagreement and
decides whether a target-0/source-factor branch should be closed, expanded to a
third family, or moved into a report-only claim boundary.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

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
