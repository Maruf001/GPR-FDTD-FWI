# Experiment 758: Target1 Confidence-Policy Synthesis

Date: 2026-06-16

## Purpose

Continue the CPU-side confidence-policy synthesis at the migration stop point
without launching new GPU experiments. The focus is target1, where recent
source-density escalation preserved exact geometry but did not clear the strict
base-margin confidence cutoff.

No optimizer, FDTD, FWI, figure-generation, or GPU command was run for this
decision note. The synthesis reads existing tracked summary tables and restored
experiment artifacts only.

## Inputs Read

Project and migration context:

```text
README.md
MIGRATION.md
SETUP.md
docs/update/summary/005_2026-06-11_summary_update.md
FIGURE_ANIMATION_TEMPLATE_INVENTORY.md
docs/experiments/756_marathon_stop_point_evaluation_seed2111485081748050_to_seed5527939710754757.md
```

Holistic table inputs:

```text
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/coordinate_run_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/target1_source_density_policy_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/intervention_series_policy_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/objective_variant_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/rank1_candidate_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/txrx_target_policy_700_1218.csv
```

Path note: the June 11 prose summary names
`outputs/summary_tables/experiment_700_1218_holistic_evaluation/`, but the
tracked restored summary-table directory on this machine is the `wk03_...`
path above.

## Archive-Level Confidence Facts

From `coordinate_run_summary_700_1218.csv`:

```text
parseable coordinate-optimizer rows: 425
exact final x/z/r geometry rows:      425
strict accepted rows, margin >=5e-4:  266
weak rows, margin <5e-4:              159

target1 rows:                         127
target1 strict accepted rows:          90
target1 weak rows:                     37
```

All 37 weak target1 rows still have rank-1 exact target1 geometry across all
six objective variants in `rank1_candidate_summary_700_1218.csv`.

Interpretation: target1 weak rows in this archive are radius-confidence
separation problems. They are not localization failures in the tested bounded
synthetic setting.

## Target1 Source-Density Evidence

The target1 source-density policy table contains 17 detected series. Some early
series overlap because the holistic detector groups historical branches from
different intervention contexts, so the counts should be treated as policy
evidence rather than independent trials.

```text
mixed: accepted setting exists    13
all weak                           3
all accepted                       1
```

Recent and decision-critical target1 source-density examples:

| Branch | Runs | Result |
| --- | --- | --- |
| seed139583862445 | 1114 -> 1115 | 5-source weak, 9-source accepted |
| seed17167680207565 | 1159 -> 1160 | 5-source weak, 9-source accepted |
| seed72723460378141 | 1172 -> 1173 | 5-source weak, 9-source accepted |
| seed5527939710754757 | 1216 -> 1217 -> 1218 | 5-source weak, 9-source near-miss, 11-source worse |
| seed2178309 | 982 -> 983 -> 984 | 5/9/11-source all weak at Tx/Rx=60 |
| seed610 | 897 -> 898 -> 899 -> 1224 | 5/8/9-source Tx/Rx=60 all weak; 5-source Tx/Rx=52.5 improved to weak near-miss |

Policy implication: a target1 9-source rescue can work, but source-density is
not monotonic and should not be extended automatically past 9 sources. The
11-source row in run 1218 is a negative control for blind escalation. Seed610
adds a complementary negative control: acquisition-offset bracketing at 52.5 mm
can improve a weak target1 branch to a near-miss without clearing the strict
base-margin rule.

## Target1 Tx/Rx Evidence

The target1 Tx/Rx table shows that 52.5 mm is the most defensible narrow
acquisition-offset probe when a target1 source-density ladder stalls:

```text
target1 Tx/Rx=52.5 mm rows: 12
accepted fraction:          0.75
median base margin:         5.10e-4
```

Relevant target1 Tx/Rx series:

| Branch | Runs | Result |
| --- | --- | --- |
| seed2178309 | 982, 987, 988, 989, 990, 991 | Tx/Rx=52.5 clears after 5/9/11 at Tx/Rx=60 were weak |
| seed9227465 | 1021 -> 1022 | 60 mm weak, 52.5 mm accepted |
| seed24157817 | 1032 -> 1033 | 60 mm weak, 52.5 mm accepted |
| seed63245986 | 1039 -> 1040 | 60 mm weak, 52.5 mm accepted |
| seed102334155 | 1045 -> 1046 | 60 mm weak, 52.5 mm accepted |
| seed267914296 | 1056 -> 1057 | 52.5 mm still weak, but later 9-source at 52.5 accepted in run 1058 |
| seed433494437 | 1061 -> 1062 | 60 mm weak, 52.5 mm accepted |

Policy implication: target1 should not inherit the target0 lower-offset rule
blindly. For target1, 52.5 mm is the first narrow acquisition probe; 45 mm is
not established as a target1 default.

## Current Stop-Point Branch

For seed5527939710754757 target1:

| Run | Sources | Tx/Rx mm | Base margin | Strict label |
| --- | ---: | ---: | ---: | --- |
| 1216 | 5 | 60.0 | 4.516e-4 | weak |
| 1217 | 9 | 60.0 | 4.875e-4 | weak near-miss |
| 1218 | 11 | 60.0 | 3.632e-4 | weak negative escalation |
| 1223 | 5 | 52.5 | 4.432e-4 | weak acquisition-offset probe |

Objective variants for run 1217 all rank exact geometry first. Five of six
variant margins clear the 5.0e-4 cutoff; only the base margin remains just
below cutoff. Run 1218 weakens that evidence, with only `late_high` clearing
cutoff.

Run 1223 executed the narrow acquisition-offset probe recommended below. It
preserved exact rank-1 geometry, but did not clear the strict base-margin
cutoff. Its diagnostic evidence is 4/6 objective variants accepted by margin,
matching the 5-source Tx/Rx=60 evidence class rather than improving on run
1217.

Decision: stop the source-density ladder and stop acquisition-offset probing
for this branch until a new objective-policy hypothesis is defined. The branch
should be carried as exact target1 geometry with unresolved strict radius
confidence.

## Confidence Policy

Strict research acceptance remains:

```text
base radius margin >= 5.0e-4
```

Practical reporting policy for synthetic target1:

1. If the base margin clears 5.0e-4, report target1 as accepted.
2. If the base margin is below 5.0e-4 but final x/z/r and all rank-1 objective
   variants are exact, report the geometry as exact but the radius confidence
   as unresolved. Do not relabel it as accepted.
3. If the first target1 weak row is a 5-source Tx/Rx=60 case and the branch is
   decision-critical, one 9-source Tx/Rx=60 rescue is justified.
4. If 9 sources remains weak or near-miss, do not escalate automatically to
   11+ sources.
5. After a failed 9-source target1 rescue, the next allowed synthetic probe is
   one narrow Tx/Rx=52.5 run, preferably at the 5-source control setting unless
   a stronger reason is documented.
6. If the Tx/Rx=52.5 probe also remains weak while exact geometry is preserved,
   carry the branch as exact but unresolved and stop further GPU work until a
   new objective-policy hypothesis is defined.

## Narrow Probe Result

Do not start a broad GPU marathon.

The approved narrow probe was run on 2026-06-17:

```text
seed:     5527939710754757
target:   target1
sources:  5
Tx/Rx:    52.5 mm
ringdown: 0.50
purpose:  test whether the target1 acquisition-offset pattern rescues the
          exact-but-weak branch after source-density escalation failed
run:      1223_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources5_txrx52p5_ringdown050_objectives
result:   exact x/z/r rank-1 geometry, weak base margin 4.432e-4
```

This result supports carrying run 1217 as the best exact target1 row for the
branch, with strict radius confidence unresolved. Additional target1 GPU work
should wait for a new hypothesis rather than repeating source-count or Tx/Rx
variants.

Field-data work remains separate from this synthetic policy synthesis.
