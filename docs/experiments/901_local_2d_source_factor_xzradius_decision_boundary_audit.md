# Experiment 901: Local 2D Source-Factor X/Z/Radius Decision Boundary Audit

Date: 2026-06-25

## Purpose

Audit the completed local x/z/radius source-factor executions as a result
boundary, not as another optimizer run.

This run reads outputs from runs `188` and `192` and asks:

```text
Do the bounded local source-factor results support a broad source-factor
robustness claim, or only a case-label-dependent local claim?
```

It does not run FDTD, the full nine-command batch, GPU work, field transfer,
field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/194_local_2d_source_factor_xzradius_decision_boundary_audit
```

Key artifacts:

```text
data/local_2d_source_factor_xzradius_decision_boundary_cases.csv
data/local_2d_source_factor_xzradius_decision_boundary_families.csv
data/local_2d_source_factor_xzradius_decision_boundary_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_XZRADIUS_DECISION_BOUNDARY_AUDIT.md
figures/local_2d_source_factor_xzradius_decision_boundary_audit.png
scripts/run_local_2d_source_factor_xzradius_decision_boundary_audit.py
scripts/test_local_2d_source_factor_xzradius_decision_boundary_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source executions audited:                 2
case rows audited:                         4
families audited:                          2
update cases truth depth/radius supported: 2 / 2
companion cases truth depth/radius support:1 / 2
families with all-case agreement:          1 / 2
families with mixed response:              1
truth x in tested envelope:                false
full batch ready:                          false
new FDTD run ready:                        false
GPU work ready:                            false
field transfer ready:                      false
```

| Family | Case | Update | Best x mm | Best z mm | Best radius mm | Truth z/r match | Margin rel | Confidence | Decision |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| `max_amplitude_stress` | `ff_max_amplitude_stress_nominal` | false | 189.0 | 90.0 | 5.0 | true | 0.101490 | strong | `companion_case_agrees` |
| `max_amplitude_stress` | `ff_max_amplitude_stress_time_shift_only` | true | 189.0 | 90.0 | 5.0 | true | 0.009782 | moderate | `update_case_truth_depth_radius_supported` |
| `max_geometry_instability` | `ff_max_geometry_instability_nominal` | false | 188.0 | 100.0 | 6.0 | false | 0.062022 | strong | `companion_case_disagrees` |
| `max_geometry_instability` | `ff_max_geometry_instability_time_shift_only` | true | 188.0 | 90.0 | 5.0 | true | 0.091388 | strong | `update_case_truth_depth_radius_supported` |

## Interpretation

The source-factor x/z/radius branch has a real but narrow result:

```text
Both update cases selected target-0 truth depth/radius inside the local
candidate envelope.
```

The broader claim fails:

```text
One companion case disagrees, and the target-0 truth x coordinate was outside
the tested x envelope.
```

So this is not full source-factor robustness. It is case-label-dependent local
evidence for depth/radius recovery under the update cases tested.

## Decision

Do not promote this branch to the full nine-command source-factor batch, GPU
work, or field transfer. Use it as bounded local evidence in reporting unless a
new targeted source-factor hypothesis justifies another small CPU
neighborhood.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_xzradius_decision_boundary_audit.py
sha256: 934d30001955a39843b0c9a282fe9b1a01c6dcdd71b05496ca3e9fed299d1809

test_local_2d_source_factor_xzradius_decision_boundary_audit.py
sha256: b9c59d1b5a82589843193b6d490057fb475d1291e7e3a9372049f2a8abff5ab5
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_xzradius_decision_boundary_audit.py
3 passed
```

Figure check:

```text
local_2d_source_factor_xzradius_decision_boundary_audit.png
1847x748, dynamic range=255
```
