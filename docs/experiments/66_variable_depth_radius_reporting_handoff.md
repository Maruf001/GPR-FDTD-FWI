# Experiment 66: Variable-Depth/Radius Reporting Handoff

## Purpose

Package the objective-use decision from experiments 60-65 into a small handoff
artifact. The goal is to prevent future reports from conflating the production
coordinate update rule with the branch-level diagnostic objective.

## 533: Tx/Rx=50 Objective Reporting Handoff

Output:

```text
outputs/experiments/533_variable_depth_radius_txrx50_objective_reporting_handoff
```

Artifacts:

```text
README.md
data/objective_reporting_handoff.json
run_manifest.json
```

Decision:

```text
production coordinate update objective: base
branch-level reporting diagnostic: veryhigh
global objective-rule promotion: rejected
```

Evidence summary:

| Evidence package | Rows | Geometry result | Veryhigh result |
| --- | ---: | --- | --- |
| Run 505 non-ringdown Tx/Rx=50 objective report | 18 | 18/18 truth rows | mean ratio 1.803, weak=5/moderate=11/strong=2, zero ambiguity |
| Run 531 fitted-ringdown all-target report | 9 | 9/9 truth rows | ratio 1.058/1.231/1.403, moderate=6/strong=3, zero ambiguity |
| Run 532 cross-condition report | 27 | 27/27 truth rows | ratio 1.058/1.612/2.563, weak=5/moderate=17/strong=5, zero ambiguity |
| Experiment 62 transfer check | 1 center-target interval | truth geometry preserved | veryhigh worsened the source-shape center-radius margin |

Interpretation:

```text
veryhigh is the default reporting diagnostic for the Tx/Rx=50 variable-depth
and variable-radius branch, but not the default update objective.
```

If base and veryhigh select different geometry in a future stress case, the
reporting rule is to show the conflict and run a targeted guardrail rather
than treating the veryhigh margin as stronger evidence.

## Next Decision

Look for the next missing research guardrail outside this now-packaged
variable-depth/radius objective branch. Prioritize CPU summaries or narrow
single-target GPU checks only if the handoff matrix exposes a concrete gap.
