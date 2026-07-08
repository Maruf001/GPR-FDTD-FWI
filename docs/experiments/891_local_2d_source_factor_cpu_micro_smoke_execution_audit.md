# Experiment 891: Local 2D Source-Factor CPU Micro-Smoke Execution Audit

Date: 2026-06-25

## Purpose

Execute the corrected source-factor CPU micro-smoke from run `180` and audit
whether it produces complete optimizer artifacts before any broader source
factor batch is attempted.

This run executes exactly one reduced CPU command. It does not run the full
nine-command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/181_local_2d_source_factor_cpu_micro_smoke_execution_audit
```

Executed optimizer output:

```text
outputs/experiments/1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_cpu_micro_smoke_execution_audit_summary.json
data/local_2d_source_factor_cpu_micro_smoke_execution_required_artifacts.csv
logs/micro_smoke_stdout.txt
logs/micro_smoke_stderr.txt
figures/local_2d_source_factor_cpu_micro_smoke_execution_audit.png
scripts/run_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
scripts/test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested run name:                     local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
expected runner output:                 1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
cap seconds:                            300
audit elapsed seconds:                  262.859
optimizer elapsed seconds:              85.753
exit code:                              0
timed out:                              false
output directory exists:                true
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

Required optimizer artifacts all exist:

```text
run_manifest.json
data/multi_rebar_coordinate_optimizer_summary.json
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
```

## Optimizer Result

The command used one target, one x offset, one z offset, one radius offset, and
the base objective only. It completed as intended, but this also means it had
only one candidate:

| Case | Candidate count | Best x mm | Best z mm | Best radius mm | Best misfit | Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `ff_max_amplitude_stress_nominal` | 1 | 188.0 | 85.0 | 6.0 | 0.968466 | missing |
| `ff_max_amplitude_stress_time_shift_only` | 1 | 188.0 | 85.0 | 6.0 | 1.230435 | missing |

The final geometry stayed equal to the initial geometry:

```text
x mm:      188.0, 248.0, 312.0
z mm:       85.0, 100.0, 95.0
radii mm:    6.0,   6.0,  6.0
```

## Interpretation

The corrected command path works. The optimizer runner allocated exactly one
numeric prefix, produced a complete artifact set, and did not time out under the
five-minute audit cap.

This is not a source-factor robustness result. The one-point micro grid cannot
rank competing candidates, so the confidence labels are `missing`. It validates
execution plumbing and establishes a practical lower-bound workload for the
source-factor branch.

## Decision

Move from one-point micro-smoke to a slightly wider bounded CPU smoke, not to
the full nine-command batch. The next script should start from a duplicated
run-specific copy and add a minimal candidate neighborhood while preserving the
numeric-free `--run-name` contract.

Keep GPU work, field transfer, and source-robustness claims blocked.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
sha256: d6a08bcc2f5d190eca6f4ac920da13d80988e208a6fae345e92f098500258d02

test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
sha256: 3dd5b0846b8ad818d4667428771f2d46c5c4a6b9552f471147e6f7eef7391151
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_micro_smoke_execution_audit.py
3 passed
```

Figure checks:

```text
local_2d_source_factor_cpu_micro_smoke_execution_audit.png  1420x738, dynamic range=255
coordinate_confidence_margins.png                          1804x665, dynamic range=238
coordinate_objective_radius_candidates.png                  2025x835, dynamic range=238
coordinate_radius_decision_panel.png                        2127x1583, dynamic range=238
system_scene_geometry.png                                   1568x1028, dynamic range=255
```
