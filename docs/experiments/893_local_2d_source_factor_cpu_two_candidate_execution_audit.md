# Experiment 893: Local 2D Source-Factor CPU Two-Candidate Execution Audit

Date: 2026-06-25

## Purpose

Execute the two-candidate CPU source-factor smoke from run `182` and audit
whether it produces complete optimizer artifacts and a meaningful first ranking
signal.

This run executes one bounded CPU command. It does not run the full
nine-command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/183_local_2d_source_factor_cpu_two_candidate_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1361_local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_cpu_two_candidate_execution_audit_summary.json
data/local_2d_source_factor_cpu_two_candidate_execution_required_artifacts.csv
logs/two_candidate_stdout.txt
logs/two_candidate_stderr.txt
figures/local_2d_source_factor_cpu_two_candidate_execution_audit.png
scripts/run_local_2d_source_factor_cpu_two_candidate_execution_audit.py
scripts/test_local_2d_source_factor_cpu_two_candidate_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested run name:                     local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
expected runner output:                 1361_local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
cap seconds:                            900
audit elapsed seconds:                  319.838
optimizer elapsed seconds:              179.415
exit code:                              0
timed out:                              false
expected candidate count per case:      2
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

The two candidate x positions were `188.0` mm and `189.0` mm for target `0`,
with z and radius fixed at `85.0` mm and `6.0` mm.

| Case | Candidate count | Best x mm | Best z mm | Best radius mm | Best misfit | Other x mm | Other misfit | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_amplitude_stress_nominal` | 2 | 189.0 | 85.0 | 6.0 | 0.958038 | 188.0 | 0.968466 | missing |
| `ff_max_amplitude_stress_time_shift_only` | 2 | 189.0 | 85.0 | 6.0 | 1.194492 | 188.0 | 1.230435 | missing |

The final geometry changed only target `0` x:

```text
initial x mm: 188.0, 248.0, 312.0
final x mm:   189.0, 248.0, 312.0
z mm:          85.0, 100.0, 95.0
radii mm:       6.0,   6.0,  6.0
```

## Interpretation

The two-candidate smoke is a useful step beyond the one-candidate micro-smoke.
It proves the corrected command path can run a small candidate neighborhood and
select a better x candidate in both the nominal and time-shift-only cases.

It still cannot support a radius confidence claim because radius was fixed to a
single value, so the confidence labels remain `missing`. This is a controlled
execution/ranking signal, not source-factor robustness evidence.

## Decision

Move to one more bounded CPU smoke with a tiny x/radius neighborhood for the
same target and case. Do not run the full nine-command source-factor batch,
GPU work, or field transfer yet.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_two_candidate_execution_audit.py
sha256: a7c169477d69ccbb2c7a0fcba6bbc08a04b003c4f842adb095b136f30a3cf294

test_local_2d_source_factor_cpu_two_candidate_execution_audit.py
sha256: 6343f28b568ae776ab9ec652f8ad49a016d03777e0f95786f894448e172927d2
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_two_candidate_execution_audit.py
3 passed
```

Figure checks:

```text
local_2d_source_factor_cpu_two_candidate_execution_audit.png  1420x738, dynamic range=255
coordinate_confidence_margins.png                            1804x665, dynamic range=238
coordinate_objective_radius_candidates.png                    2025x835, dynamic range=238
coordinate_radius_decision_panel.png                          2127x1583, dynamic range=241
system_scene_geometry.png                                     1590x1028, dynamic range=255
```
