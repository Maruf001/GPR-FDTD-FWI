# Field Experiment 022: GSSI 51600S Long-Profile Stack Policy

Date: 2026-06-17

## Purpose

CPU-only repeat-aligned stack analysis for the two long local GSSI profiles:

```text
PROJECT001C__015.DZT
PROJECT001C__013.DZT
```

Experiment 020 found this pair as a moderate direct repeat candidate
(`corr=0.7244`). Experiment 021 stacked the stronger short pair 014/016; this
run checks whether the long pair also supports a repeatable shallow-response
pattern. It does not run FDTD, FWI, or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/022_gssi51600s_long_profile_stack_policy
```

Artifacts:

```text
data/long_profile_stack_lag_scan.csv
data/long_profile_stack_signal.csv
data/long_profile_stack_anchor_candidates.csv
data/long_profile_stack_policy_summary.json
data/figure_validation.csv
figures/long_profile_stack_policy.png
run_manifest.json
```

## Result

Alignment:

```text
best orientation:             direct
best lag:                     +413.292 mm
normalized correlation:        0.7244
alignment label:               moderate_direct_scan_preferred
```

Stack anchors:

```text
anchor candidates:             8
stable stack anchors:          6
policy label:                  long_repeat_stack_pattern_only_qc
```

Stable anchor x positions:

```text
746.6 mm
1043.2 mm
1293.2 mm
1496.5 mm
1693.2 mm
2096.5 mm
```

## Interpretation

The long profiles contain a repeatable shallow-pattern structure, but the
field evidence remains pattern-only. Experiment 016 skipped profile 013 because
it had no usable phase-anchor picks:

```text
reason: no_phase_anchor_picks
candidate_count_before_time_filter: 4
candidate_count_after_time_filter: 0
```

Therefore the long-pair stack cannot support event pairing, phase-time
anchoring, radius, cover-depth, survey-geometry, 3D, or FWI claims. The useful
field conclusion is narrower:

```text
Use 013/015 as long-profile shallow-pattern repeatability/QC evidence.
Use 014/016 as stronger short-profile timing/repeatability QC evidence.
Do not treat the four DZT files as a recovered 3D survey grid.
Do not report field radius, cover depth, field FWI recovery, or 3D inversion
from this dataset without external survey and target metadata.
```

## Validation

Focused field tests:

```text
tests/test_gssi_field_long_profile_stack_policy.py: included in 7 passed
tests/test_gssi_field_short_profile_stack_policy.py: included in 7 passed
```

The stack-policy figure was validated as nonblank:

```text
long_profile_stack_policy.png nonwhite=0.1122, dynamic range=255
```
