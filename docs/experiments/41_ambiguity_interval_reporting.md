# Experiment 41: Ambiguity Interval Reporting

## Goal

Turn weak-confidence candidate rankings into reportable ambiguity fields before
any full multi-rebar optimizer is promoted.

Stage 6 showed:

```text
24/24 cases recover the true target x/z/r,
but 22/24 cases are weak-confidence.
```

So a single point estimate is not enough. The report must expose plausible
nearby candidates.

## Code Changes

Updated:

```text
inversion/candidate_confidence.py
tests/test_candidate_confidence.py
```

New report fields:

```text
fallback_warning
ambiguity_candidate_count
ambiguity_misfit_threshold
ambiguity_x_min_mm
ambiguity_x_max_mm
ambiguity_z_min_mm
ambiguity_z_max_mm
ambiguity_radius_min_mm
ambiguity_radius_max_mm
```

Default ambiguity rule:

```text
include candidates within 1.5% of the best objective value.
```

This threshold is intentionally conservative for the Stage 6 synthetic runs:
it captures the recurring deeper/larger-radius branch instead of hiding it.

## Validation

Focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_candidate_confidence.py \
  -q
```

Result:

```text
5 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  inversion/candidate_confidence.py \
  run_candidate_confidence_report.py
```

Result:

```text
passed
```

## 080_multi_rebar_stage7_ambiguity_interval_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/067_multi_rebar_left_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/071_multi_rebar_left_local_geometry_noise10_seed21/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/073_multi_rebar_left_local_geometry_noise10_seeds34_55/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/068_multi_rebar_center_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/075_multi_rebar_center_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/069_multi_rebar_right_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/077_multi_rebar_right_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_stage7_ambiguity_interval_report
```

Output:

```text
outputs/experiments/080_multi_rebar_stage7_ambiguity_interval_report
```

Plot validation:

```text
candidate_confidence_margins.png: 3691x903 px, dynamic range 255, std 62.937
```

## Results

Fallback warnings:

| Warning | Count |
| --- | ---: |
| radius_weak_confidence | 22 |
| none | 2 |

Ambiguity intervals:

| Target | Radius interval covered | z interval covered | Fallback rows |
| --- | --- | --- | ---: |
| left index 0 | 6.0-7.0 mm | 90-91 mm | 7 |
| center index 1 | 5.4-7.0 mm | 89-91 mm | 8 |
| right index 2 | 6.0-7.0 mm | 90-91 mm | 7 |

Across all rows:

```text
ambiguity z max is 91 mm in all 24 rows.
ambiguity radius max is 6.8 mm in 9 rows and 7.0 mm in 15 rows.
```

## Interpretation

The ambiguity report does what the Stage 6 evidence requires:

```text
it preserves the best estimate at the true 6.0 mm radius, while explicitly
showing that nearby deeper/larger candidates are plausible under the weak
objective margins.
```

This is the right product behavior for the current synthetic regime:

```text
report the point estimate,
report the confidence label,
report the ambiguity interval,
report the nearest competing branch.
```

## Decision

Stage 7 passes as a reporting layer.

Next action:

```text
Run full validation. Then use these confidence/ambiguity fields as mandatory
outputs for any full 9-parameter multi-rebar optimizer or coordinate-search
runner.
```
