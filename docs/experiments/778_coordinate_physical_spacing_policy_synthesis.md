# Experiment 778: Coordinate Physical-Spacing Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only guardrail synthesis after the close10 Tx/Rx50 result. Experiments 776
and 777 showed clean close12 and close10 recovery in the current target2 branch,
but the target1/target2 radii are 6 mm and 8 mm. Therefore center spacings
below 14 mm overlap the cylinders.

This run separates physically non-overlapping/tangent spacing evidence from
overlapping-cylinder algorithmic stress tests. It uses existing aggregate CSVs
only; no FDTD, FWI, or GPU command was run.

## Output

```text
outputs/experiments/1256_coordinate_physical_spacing_policy_synthesis_after_close10
```

Artifacts:

```text
data/coordinate_physical_spacing_policy_groups.csv
data/coordinate_physical_spacing_policy_by_txrx.csv
data/coordinate_physical_spacing_policy_summary.json
data/figure_validation.csv
figures/coordinate_physical_spacing_policy.png
run_manifest.json
```

## Inputs

The synthesis uses the default close-spacing aggregate policy set plus the
existing close14 Tx/Rx50 high-noise replicated aggregate:

```text
outputs/experiments/360_coordinate_confidence_close14_sources4_txrx50_noise15p361328125_seed_replicates
```

## Result

Summary:

```text
groups:                         18
clean non-overlap groups:        13
clean overlap-stress groups:      2
target1/target2 radius sum:      14 mm
```

By Tx/Rx:

| Tx/Rx | Closest clean physical spacing | Clean physical spacings | Clean overlap-stress spacings |
| ---: | ---: | --- | --- |
| 35 mm | 30 mm | 30, 35, 40, 45, 50 | none |
| 45 mm | 14 mm | 14, 15, 20, 25, 28 | none |
| 50 mm | 14 mm | 14 | 10, 12 |

Decision:

```text
For physical rebar-spacing claims with the current target1/target2 6 mm and
8 mm radius pair, close14 is the tangent non-overlap limit. The archive
supports clean non-overlap/tangent recovery at close14 for the tested Tx/Rx45
and Tx/Rx50 branches; close10 and close12 should be reported only as
overlapping-cylinder algorithmic stress tests.
```

## Interpretation

The close10 result is still useful, but its role is narrower: it demonstrates
that the current optimizer/objective can distinguish a mathematically
overlapping branch. It should not be used as a physical rebar-spacing limit in
the paper.

For publishable physical spacing claims in this branch, the clean boundary is
currently:

```text
close14 tangent case for the 6 mm / 8 mm pair
```

The next physical synthetic work should use non-overlapping geometries or
explicitly redesign the geometry in terms of edge clearance rather than center
spacing.

Follow-up implementation guard:

```text
run_multi_rebar_local_geometry_profile.py
run_multi_rebar_coordinate_optimizer.py
```

Both geometry-search entry points now support the default-off flag:

```text
--enforce-nonoverlap-candidates
```

When enabled, local candidate geometries with overlapping circular rebar
cross-sections are skipped. Tangent candidates are allowed. Existing archived
experiments are unchanged because the flag defaults to off.

## Validation

Focused coordinate policy tests:

```text
tests/test_coordinate_physical_spacing_policy_synthesis.py: included in 8 passed
tests/test_coordinate_resolution_policy_synthesis.py: included in 8 passed
tests/test_multi_rebar_local_geometry_profile.py and
tests/test_multi_rebar_coordinate_optimizer.py: included in 37 passed
```

The guardrail figure was validated as nonblank:

```text
coordinate_physical_spacing_policy.png nonwhite=0.1456, dynamic range=255
```
