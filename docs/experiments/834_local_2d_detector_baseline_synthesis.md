# Experiment 834: Local 2D Detector Baseline Synthesis

Date: 2026-06-18

## Purpose

Complete the CPU-first same-case detector-baseline comparison requested by the
local 2D baseline contract. This slice compares the simple hyperbola-energy
detector against the current close14 and close50 target2 manuscript branches:

```text
target2 close14 source5 / Tx/Rx=45 mm / seeds 13,21,34
target2 close50 linear receiver Tx/Rx=29.5 mm / seeds 13,21,34
```

Each branch was run for nominal and source-mismatch cases. This was not a
GPU/FWI sweep and did not launch broad GPU work.

## Outputs

Command plan:

```text
outputs/summary_tables/017_local_2d_detector_baseline_command_plan_post_interface_patch
```

Detector runs:

```text
outputs/experiments/1326_local2d_detector_baseline_target2_close14_seed13_nominal_cpu
outputs/experiments/1327_local2d_detector_baseline_target2_close14_seed13_source_mismatch_cpu
outputs/experiments/1328_local2d_detector_baseline_target2_close14_seed21_nominal_cpu
outputs/experiments/1329_local2d_detector_baseline_target2_close14_seed21_source_mismatch_cpu
outputs/experiments/1330_local2d_detector_baseline_target2_close14_seed34_nominal_cpu
outputs/experiments/1331_local2d_detector_baseline_target2_close14_seed34_source_mismatch_cpu
outputs/experiments/1332_local2d_detector_baseline_target2_close50_linear29p5_seed13_nominal_cpu
outputs/experiments/1333_local2d_detector_baseline_target2_close50_linear29p5_seed13_source_mismatch_cpu
outputs/experiments/1334_local2d_detector_baseline_target2_close50_linear29p5_seed21_nominal_cpu
outputs/experiments/1335_local2d_detector_baseline_target2_close50_linear29p5_seed21_source_mismatch_cpu
outputs/experiments/1336_local2d_detector_baseline_target2_close50_linear29p5_seed34_nominal_cpu
outputs/experiments/1337_local2d_detector_baseline_target2_close50_linear29p5_seed34_source_mismatch_cpu
```

Synthesis:

```text
outputs/summary_tables/018_local_2d_detector_baseline_synthesis_post_cpu_runs
```

Key artifacts:

```text
017/data/local_2d_detector_baseline_command_plan_rows.csv
017/data/local_2d_detector_baseline_commands.sh
018/data/local_2d_detector_baseline_synthesis_rows.csv
018/data/local_2d_detector_baseline_branch_summary.csv
018/data/local_2d_detector_baseline_synthesis_summary.json
018/figures/local_2d_detector_baseline_synthesis.png
```

## Result

Policy label:

```text
local_2d_detector_baseline_synthesis_simple_detector_under_resolves
```

Summary:

```text
cases:                         12
all-truth detector cases:       0 / 12
target0 hits:                   0 / 12
target1 hits:                  12 / 12
target2 hits:                   6 / 12
backend:                        cpu
GPU used:                       false
max parallel processes:         1
mean detector runtime:          72.69 s
max detector runtime:           85.83 s
```

Branch summary:

| Branch | Cases | All-truth | Target0 hits | Target1 hits | Target2 hits | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| close14 | 6 | 0 | 0 | 6 | 6 | close pair detected, left bar missed |
| close50 linear29.5 | 6 | 0 | 0 | 6 | 0 | middle cue only, left and right bars missed |

Runtime/resource envelope:

```text
single pilot wall time:       1:21.75
remaining batch wall time:   13:25.29
batch max RSS:               <292 MB
observed GPU utilization:    about 6%
observed RAM use:            about 15 GiB of 119 GiB
```

## Interpretation

The same-case simple detector is not a positive competitor for the current
FWI/coordinate optimizer. It did not recover all three truth positions in any
of the close14 or close50 cases.

For close14, it repeatedly found the close 250/264 mm pair but missed the
190 mm bar. This supports the view that close14 contains image-level
overlap/ambiguity, but the detector is still weaker than the coordinate
optimizer because the optimizer selected the full truth in all six close14
rows.

For close50 linear 29.5 mm, the detector only recovered the middle 250 mm cue.
It did not track the optimizer's seed13-specific x-ambiguity caveat and should
not be used as evidence about the clean-versus-ambiguous FWI distinction.

The paper-safe use is therefore:

```text
Use this as a weak simple-detector baseline showing that the controlled
FWI/coordinate objective is doing more than naive hyperbola-energy seeding.
Do not frame it as a competitive detector or as a method that tracks the
optimizer's objective-margin ambiguity tiers.
```

## Parameter Sensitivity Follow-Up

The saved-B-scan parameter sensitivity is:

```text
outputs/summary_tables/020_local_2d_detector_parameter_sensitivity_post_rank_depth_metrics
```

This follow-up rescored the 12 saved detector B-scans without rerunning FDTD,
FWI, GPU kernels, field FWI, or 3D/HPC work. It swept 81 detector settings:

```text
background mode:        none, mean, median
top-k candidates:       20, 40, 80
separation profiles:    dense4, moderate12, distinct20
time-offset families:   single667, baseline, wide
case/config rows:       972
backend:                saved-B-scan CPU rescore
GPU used:               false
```

Key result:

```text
policy label:                         local_2d_detector_parameter_sensitivity_saved_bscan_cpu
rescued cases:                         12 / 12
best config:                           median_top40_moderate12_single667
best-config all-truth cases:            12 / 12
best-config mean unique truth hits:       3.0
best-config mean max assigned rank:      23.42
best-config worst max assigned rank:     36.0
```

Interpretation: the original negative detector-baseline result is a default
parameter-setting failure, not a detector-family impossibility. With a
moderate non-maximum-suppression profile and deeper candidate list, all truth
locations are present in the candidate set for every close14 and close50 case.

The caveat is rank depth. Some close50 recoveries require candidate ranks in
the 30s, so this is candidate-list recoverability, not a clean standalone
top-pick detector result. The paper-safe update is:

```text
Use the detector as a weak default baseline and as evidence that an improved
detector-to-FWI or detector-to-assignment stage can provide truth-containing
candidate lists. Do not claim that the tuned detector alone resolves the
ambiguity tiers without a downstream assignment/refinement policy.
```

## Candidate Rank Policy

The candidate-rank policy synthesis is:

```text
outputs/summary_tables/021_local_2d_detector_candidate_rank_policy_post_sensitivity
```

It reads the saved sensitivity rows and asks what top-N detector candidate
budget is required before every case has all three truths available.

Key result:

```text
policy label:                           local_2d_detector_candidate_rank_policy_saved_bscan_cpu
rank caps tested:                        3,5,10,20,40,80
best case count within top3:             0 / 12
best case count within top5:             2 / 12
best case count within top10:            4 / 12
best case count within top20:           10 / 12
best case count within top40:           12 / 12
full-recovery configs at top40:          8
minimal shared rank cap for all cases:  40
best shared config:                      none_top40_moderate12_baseline
best shared mean max assigned rank:      21.33
best shared worst max assigned rank:     32.0
```

Branch-specific top-20 policies exist:

```text
close14 best top20:  6 / 6 with mean_top20_moderate12_baseline
close50 best top20:  6 / 6 with mean_top20_distinct20_baseline
```

Interpretation: a single shared detector policy needs a top-40 candidate
budget to cover all saved close14/close50 cases. Branch-specific policies can
cover each branch at top-20, but that is not yet a blind operational policy.
Any detector-to-FWI pilot should therefore be rank/cost gated and should not
be described as a shallow detector-only solution.

## Blind Assignment Policy

The blind score-based assignment policy synthesis is:

```text
outputs/summary_tables/022_local_2d_detector_blind_assignment_policy_post_rank_sensitivity
outputs/summary_tables/023_local_2d_detector_blind_assignment_policy_with_span_bonus
```

These runs rerun the saved-B-scan detector grid and evaluate blind
three-candidate assignments. Run `022` uses score plus a minimum-x-separation
constraint. Run `023` adds span/diversity bonuses to test whether spatial
coverage can rescue the handoff. Neither run uses truth to choose assigned
candidates, and neither reruns FDTD, FWI, GPU kernels, field FWI, or 3D/HPC
work.

Score-only result:

```text
policy label:                       local_2d_detector_blind_assignment_policy_saved_bscan_cpu
case/policy rows:                   11664
config-assignment policies:           972
full-recovery policies:                 0
best config:                        median_top40_dense4_baseline
best assignment policy:             top40_minx20
best all-truth cases:                   1 / 12
best mean unique truth hits:            1.0
close14 branch-best all-truth:          1 / 6
close50 branch-best all-truth:          1 / 6
```

Span/diversity result:

```text
case/policy rows:                   46656
config-assignment policies:          3888
full-recovery policies:                 0
best config:                        none_top20_moderate12_baseline
best assignment policy:             top20_minx8_span0p5
best all-truth cases:                   2 / 12
best mean unique truth hits:            1.667
close14 branch-best all-truth:          2 / 6
close50 branch-best all-truth:          1 / 6
```

Interpretation: the detector candidate lists can contain all truth locations,
but simple blind score/spread assignment and span/diversity bonuses cannot
extract the correct three-bar geometry. Therefore a detector-to-FWI experiment
should not be framed as a solved blind detector handoff. It should either
introduce a stronger assignment model, remain rank-gated, or be explicitly
labeled as an oracle/upper-bound initialization study.

## Assignment Policy-Oracle Taxonomy

The follow-up taxonomy is:

```text
outputs/summary_tables/025_local_2d_detector_assignment_failure_taxonomy_policy_oracle
```

It reads the saved assignment rows from run `023` and, for each saved
close14/close50 case, chooses the best row across the blind-assignment policy
grid. This is a per-case policy oracle, not a deployable shared policy.

```text
policy label:                         local_2d_detector_assignment_failure_taxonomy_per_case_policy_oracle
selection scope:                      per_case_best_assignment_policy_oracle
cases:                                12
per-case oracle all-truth cases:       7 / 12
best shared-policy all-truth cases:    2 / 12
target0 hits:                          9 / 12
target1 hits:                         12 / 12
target2 hits:                         10 / 12
mean unique truth hits:                2.583
close14 oracle all-truth:              6 / 6
close50 oracle all-truth:              1 / 6
GPU used:                              false
```

Interpretation: the candidate lists contain more recoverable information than
the best shared blind policy can currently exploit. The failure is now better
localized: close14 can be solved by choosing the right assignment policy per
case, while close50 linear 29.5 mm remains mostly limited by missed left/right
assignments. The next meaningful local 2D step is therefore not a broad GPU
sweep. It is a stronger assignment-policy selector or a small downstream
objective-gated handoff that can explain why a policy should be selected
without looking at truth.

## Truth-Free Selector Audit

The first truth-free selector audit is:

```text
outputs/summary_tables/026_local_2d_detector_assignment_selector_truth_free_feature_grid
```

It scores the saved assignment rows using only assignment-row features:
candidate ranks, x-span, center offset, gap balance, z-consistency, and
budget. It does not use truth labels to score a held-out row, and it does not
rerun FDTD, FWI, GPU kernels, field FWI, or 3D/HPC work.

```text
policy label:                         local_2d_detector_assignment_selector_truth_free_feature_grid
assignment rows:                       46656
selector candidates:                     220
best in-sample selector:              span_target70_w1_rank_lite_center0.06_gap0
best in-sample all-truth cases:          1 / 12
leave-one-case all-truth cases:          0 / 12
leave-one-seed all-truth cases:          0 / 12
leave-one-branch all-truth cases:        0 / 12
fixed shared-policy all-truth cases:     2 / 12
per-case policy-oracle all-truth cases:  7 / 12
GPU used:                              false
```

Interpretation: simple truth-free row-feature heuristics are worse than the
fixed shared blind policy, even before held-out validation. This rules out the
easy path of choosing assignment policies from rank/span/center/z-spread
features alone. The policy-oracle gap should now be treated as a need for
richer information, most likely candidate-score geometry, waveform/objective
gating, or an explicitly bounded rank-gated FWI upper-bound study.

## Image-Objective Gate

The saved-B-scan image-objective gate is:

```text
outputs/summary_tables/027_local_2d_detector_image_objective_gate_saved_bscan
```

It scores assigned detector triples against the saved B-scans with Gaussian
hyperbola masks over the detector time-offset families. This is a proxy
image-domain objective, not FDTD/FWI. It does not rerun FDTD, FWI, GPU kernels,
field FWI, or 3D/HPC work.

```text
policy label:                         local_2d_detector_image_objective_gate_saved_bscan_cpu
assignment rows:                       46656
scored rows:                          100656
objective variants:                       3
primary objective:                    row_background_sigma60
primary all-truth cases:                 0 / 12
primary mean unique truth hits:          1.250
fixed shared-policy all-truth cases:     2 / 12
rank/span selector all-truth cases:       0 / 12
per-case policy-oracle all-truth cases:  7 / 12
close14 primary all-truth:               0 / 6
close50 primary all-truth:               0 / 6
GPU used:                              false
```

Interpretation: the simple image-objective gate is worse than the fixed shared
blind policy. It tends to select central/right high-energy hyperbolas and
systematically misses target0. That closes the easy downstream-gate path:
detector-seeded FWI should not be launched on the assumption that a shallow
image objective can pick the right three-bar geometry. The remaining honest
options are a stronger waveform/objective gate, a learned selector with richer
features and more cases, or an explicitly labeled rank-gated/oracle upper-bound
study.

## Detector-to-FWI Handoff Budget

The detector handoff-budget synthesis is:

```text
outputs/summary_tables/029_local_2d_detector_handoff_budget
```

It compares candidate-list upper bounds against deployable single-triple
selectors before any detector-seeded FWI run.

```text
policy label:                         local_2d_detector_handoff_budget_cpu_no_fwi
cases:                                12
strategies compared:                   7
cheapest full candidate strategy:      branch_top20_candidate_list
cheapest full triples per case:     1140
cheapest full total triples:       13680
best deployable strategy:             shared_blind_assignment
best deployable all-truth cases:        2 / 12
per-case oracle all-truth cases:        7 / 12
image-gate all-truth cases:             0 / 12
shared rank cap for full recovery:     40
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: a detector-seeded FWI handoff is not yet narrow. The detector
can produce truth-containing candidate lists, but the cheapest all-case
candidate-list handoff still implies 1,140 candidate triples per case under
branch-specific top-20 settings. The deployable shared assignment is cheap but
only reaches 2/12 all-truth cases, while the 7/12 oracle is not deployable.
The next step should be a stronger CPU waveform/objective gate that shrinks
the candidate-triple set before spending GPU/FWI time.

## All-Top20 Triple Gate Pilot

The branch-specific all-top20 triple gate pilot is:

```text
outputs/summary_tables/030_local_2d_detector_alltriples_gate_pilot
```

It reruns the branch-specific saved-B-scan detector configurations on CPU,
enumerates all candidate triples from the top-20 detector lists, and scores
12,180 triples with simple score/span/min/mask objectives.

```text
policy label:                         local_2d_detector_alltriples_gate_pilot_cpu_no_fwi
cases:                                12
candidate-triple rows:             12180
objective rows:                       72
objectives tested:                     6
best top1 all-truth cases:             0 / 12
best top10 objective:                 span_bonus
best top10 all-truth cases:            2 / 12
best top50 objective:                 span_bonus
best top50 all-truth cases:            8 / 12
best top50 median first-truth rank:   23.5
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: even after enumerating the branch-specific top-20 candidate
triple space, simple score/span/min/mask objectives do not produce a deployable
detector-seeded FWI queue. No objective selects an all-truth triple at rank 1,
and the best top-10 gate reaches only 2/12 cases. This strengthens the no-FWI
decision: a future handoff needs a richer waveform gate, a deliberately labeled
oracle/rank-gated upper-bound, or more training/evaluation cases.

## Rank-Budget Diagnostic

The detector rank-budget diagnostic is:

```text
outputs/summary_tables/034_local_2d_detector_rank_budget_diagnostic_post_alltriples_gate
```

It reads the saved all-top20 triple rows from run `030` and asks how deep each
objective must go before the first all-truth triple appears.

```text
policy label:                         local_2d_detector_rank_budget_diagnostic_cpu_no_fwi
cases:                                12
candidate-triple rows:             12180
all-truth combo available cases:      12 / 12
sparse all-truth cases:                6 / 12
best top20 objective:                 span_bonus
best top20 all-truth cases:            6 / 12
best top50 all-truth cases:            8 / 12
best top100 all-truth cases:          10 / 12
best top200 all-truth cases:          12 / 12
minimal all-case budget:             200 triples/case
objectives at all-case budget:        balanced, span_bonus
max top1 all-truth cases:              0 / 12
max top1 target0-hit cases:            3 / 12
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the detector is not missing the correct geometry from the
candidate space; the problem is ranking and sparsity. All six close50 cases
have only one or two all-truth triples in the enumerated space, and current
objectives usually under-select the left target. A rank-gated upper-bound study
is defensible as a bounded analysis, but detector-seeded FWI is still not a
launch-ready GPU workload.

## Component Waveform-Gate Pilot

The component-wise waveform gate is:

```text
outputs/summary_tables/035_local_2d_detector_component_waveform_gate_post_rank_budget
```

It scores each candidate bar's hyperbola mask separately on the saved B-scans,
then combines the component support with span/gap terms. This is still CPU-only
saved-data scoring, not FDTD/FWI.

```text
policy label:                         local_2d_detector_component_waveform_gate_cpu_no_fwi
cases:                                12
candidate-triple rows:             12180
component candidates scored:         230
objectives tested:                     7
best top1 all-truth cases:             0 / 12
best top10 objective:                 component_balanced
best top10 all-truth cases:            3 / 12
best top50 objective:                 component_balanced
best top50 all-truth cases:           10 / 12
best top100 all-truth cases:          11 / 12
best top200 all-truth cases:          12 / 12
top10 improvement over run 030:        +1 case
top50 improvement over run 030:        +2 cases
minimal all-case budget:             200 triples/case
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: component-wise waveform support is a better CPU gate than the
previous simple all-triples objectives, especially at top-50. It still does
not produce a deployable top-1 selector and still needs a 200-triple/case
budget for full coverage. The next detector-side research path is a stronger
waveform objective or a clearly labeled rank-gated upper-bound, not a GPU/FWI
launch.

## Component Selector Audit

The truth-free component selector audit is:

```text
outputs/summary_tables/037_local_2d_detector_component_selector_audit_post_component_gate
```

It evaluates 975 truth-free selector candidates over the saved component
waveform-gated detector triples from run `035`.

```text
policy label:                         local_2d_detector_component_selector_audit_cpu_no_fwi
selector candidates:                  975
best in-sample selector:              cb0.4_min0.4_span0.25_target70.0_tw0.25_rank0.08
best in-sample all-truth cases:         1 / 12
leave-one-case all-truth cases:         0 / 12
leave-one-seed all-truth cases:         0 / 12
leave-one-branch all-truth cases:       0 / 12
best in-sample target0 hits:            6 / 12
leave-one-case target0 hits:            5 / 12
dominant best-selector failure:        missing_target1
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: selector features over the improved component gate still do
not solve deployable top-1 selection. The best in-sample selector only recovers
one all-truth case, and cross-validation recovers none. This closes the current
truth-free selector route; the detector evidence should be used as rank-gated
upper-bound context unless a materially stronger waveform objective is added.

## Geometry-Family Selector Audit

The branch-family geometry-prior selector audit is:

```text
outputs/summary_tables/041_local_2d_detector_geometry_family_selector_post_upper_bound_policy
```

This run adds controlled geometry-family features to the selector: span target,
signed left/right gap target, center target, and rank penalties. It reads saved
component-gated detector rows only and does not run FDTD, FWI, GPU kernels,
field FWI, 3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_geometry_family_selector_cpu_no_fwi
selector candidates:                  2160
best selector:                        cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1
best in-sample all-truth cases:          3 / 12
leave-one-case all-truth cases:          2 / 12
leave-one-seed all-truth cases:          1 / 12
leave-one-branch all-truth cases:        2 / 12
best in-sample target0/1/2 hits:         7 / 5 / 9
improvement over component selector:    +2 in-sample, +2 leave-one-case
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the old gap-balance selector penalized the close14 right-pair
geometry. A signed-gap branch-family prior repairs part of that pathology, but
validated top-1 recovery remains only 2/12. This is useful detector-analysis
evidence, not a detector-seeded FWI launch trigger.

## Selector-Gap Decomposition

The selector-gap decomposition is:

```text
outputs/summary_tables/045_local_2d_detector_selector_gap_decomposition
```

It reads the saved component-gated detector rows and decomposes the current
geometry-family selector's selected row against the best all-truth competitor
per case. It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or
neural-network training.

```text
policy label:                         local_2d_detector_selector_gap_decomposition_cpu_no_fwi
selected all-truth cases:               3 / 12
failed selector cases:                  9 / 12
best truth available cases:            12 / 12
median required selector gain:          0.18098
max required selector gain:             0.55054
dominant loss feature:                  signed_gap_prior_score
dominant loss feature cases:            7 / 9 failed
selected-truth minimum wrong margin:    0.00667
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the all-truth triple is present for every saved case, but the
truth-free selector still chooses a wrong triple in nine cases. The dominant
loss is the signed-gap prior, not raw component waveform support. The detector
therefore remains useful as a rank-gated upper-bound/failure-analysis baseline,
not as an automatic detector-seeded FWI initializer.

## Selector Counterfactual Sensitivity

The selector counterfactual sensitivity is:

```text
outputs/summary_tables/048_local_2d_detector_selector_counterfactual_sensitivity
```

This run tests simple one-dimensional reweighting around the current
geometry-family selector. It reads saved detector rows only and does not run
FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_selector_counterfactual_sensitivity_cpu_no_fwi
counterfactual variants:                44
counterfactual families:                 8
base all-truth cases:                    3 / 12
best counterfactual:                    signed_gap_sweep_w2
best all-truth cases:                    3 / 12
best improvement over base:              0
signed-gap-zero all-truth cases:         1 / 12
best median required selector gain:      0.15420
ready for detector-seeded FWI:          false
gpu priority:                           none
```

Interpretation: simple scalar reweighting does not rescue the detector
selector. The best variant reduces the median required selector gain, but it
does not improve the top-1 all-truth count beyond 3/12. Removing the signed-gap
prior makes recovery worse. A detector-seeded FWI run would need a materially
stronger downstream waveform objective, not just selector retuning.

## Image-Objective Rank Diagnostic

The saved-B-scan image-objective rank diagnostic is:

```text
outputs/summary_tables/050_local_2d_detector_image_objective_rank_diagnostic
```

This run reads the scored rows from `027` and ranks each case/objective by
image-objective score. It does not recompute masks and does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_image_objective_rank_diagnostic_cpu_no_fwi
objective variants:                    3
scored rows:                           100656
best objective:                        row_background_sigma100
best top50 all-truth cases:             0 / 12
best top200 all-truth cases:            1 / 12
best top1000 all-truth cases:           6 / 12
best median first all-truth rank:     639
best max first all-truth rank:        1980
previous policy-oracle cases:           7 / 12
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the existing image-objective gate is weaker than the component
rank-gated upper-bound route. It does not put any all-truth row inside top-50,
and only half the cases are inside top-1000 under the best variant. This closes
the current saved-B-scan image-objective route as a practical detector-to-FWI
handoff.

## Target-Failure Taxonomy

The detector target-failure taxonomy is:

```text
outputs/summary_tables/053_local_2d_detector_target_failure_taxonomy
```

It reads the selector-gap cases from `045` and asks which true target locations
are dropped by the selected wrong triples. It does not run FDTD, FWI, GPU
kernels, field FWI, 3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_target_failure_taxonomy_cpu_no_fwi
selected all-truth cases:              3 / 12
failed selector cases:                 9 / 12
best truth available cases:           12 / 12
single-target failure cases:           4 / 9
multi-target failure cases:            5 / 9
missing target0 cases:                 5 / 9
missing target1 cases:                 7 / 9
missing target2 cases:                 3 / 9
dominant missing target:               target1
target1-missing median required gain:  0.28615
target1-missing max required gain:     0.55054
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the selector is not merely underweighted or overweighted along
one scalar feature. The selected wrong triples usually drop target1, and more
than half the failures drop multiple targets. A meaningful next detector-side
model would need target-conditioned coverage or waveform evidence; another
simple reweighting or detector-seeded FWI launch is not justified.

## Depth/Slot Prior Probe

The detector depth/slot prior probe is:

```text
outputs/summary_tables/055_local_2d_detector_depth_slot_prior_probe
```

It tests a concrete follow-up to the target-failure taxonomy by adding broad
depth and expected-x-slot priors to the current selector score over saved
component-gate rows. It does not run FDTD, FWI, GPU kernels, field FWI,
3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_depth_slot_prior_probe_cpu_no_fwi
candidate rows:                       12180
prior variants:                       72
base all-truth cases:                  3 / 12
best all-truth cases:                  5 / 12
gain over base:                        2 cases
best mean truth hits:                  2.4167
best depth weight:                    12.0
best slot weight:                      1.0
remaining failed selector cases:       7 / 12
remaining target1 misses:              4
remaining target2 misses:              3
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: a broad depth prior is useful signal: it improves top-1
all-truth selection from 3/12 to 5/12. It is not enough for a detector-seeded
FWI contract. The remaining failures support a stronger target-conditioned
waveform/coverage model rather than another broad GPU run.

## Slot-Component Assembly Probe

The branch-slot component assembly probe is:

```text
outputs/summary_tables/057_local_2d_detector_slot_component_assembly_probe
```

It decomposes saved detector triples into unique components and assembles them
slot-by-slot using the known close14/close50 branch target slots. It does not
run FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or neural-network training.

```text
policy label:                         local_2d_detector_slot_component_assembly_probe_cpu_no_fwi
candidate rows:                       12180
slot-assembly variants:               120
current triple selector all-truth:      3 / 12
depth/slot prior best all-truth:        5 / 12
branch-slot component assembly:        12 / 12
best mean target-slot hits:             3.0
best failed cases:                      0 / 12
minimum component candidates per case: 16
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: component evidence is present for all target slots in every
saved case when known branch slots are allowed. This is a strong upper-bound
and contract result, not a deployable selector. The remaining detector problem
is blind target assignment, not missing component detections.

## Blind Component-Envelope Assembly Probe

The blind component-envelope assembly probe is:

```text
outputs/summary_tables/059_local_2d_detector_blind_component_envelope_assembly
```

It decomposes saved detector triples into unique components, infers support
envelopes from the component cloud, and selects components with a
span-adaptive close-pair/regular-spacing prior. The selector does not use the
known branch slot coordinates at inference; truth slots are used only to score
the policy grid and report recovery.

```text
policy label:                         local_2d_detector_blind_component_envelope_assembly_cpu_no_fwi
candidate rows:                       12180
blind-envelope variants:              288
current triple selector all-truth:      3 / 12
depth/slot prior best all-truth:        5 / 12
known-slot component upper bound:      12 / 12
blind envelope best slot cases:        12 / 12
leave-one-case slot cases:             12 / 12
uses branch slots for selection:       false
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the saved detector evidence can support target-slot assembly
without hard-coding close14/close50 slot locations. This is a meaningful
advance over the known-slot upper-bound probe, but it is still a small
saved-corpus policy synthesis and only validates component-slot coverage, not
full x/z/r inversion. It should inform manuscript claims and the next
CPU-side detector handoff design, not launch broad GPU FWI.

## Blind Envelope Robustness Audit

The blind-envelope robustness audit is:

```text
outputs/summary_tables/061_local_2d_detector_blind_envelope_robustness_audit
```

It reads the saved `059` grid and the saved `035` component rows. It selects
variants under held-out seed, branch-family, and source-condition splits, then
computes the best-variant score margin over the best wrong component triple.

```text
policy label:                         local_2d_detector_blind_envelope_robustness_audit_cpu_no_fwi
full-success variants:                117 / 288
near-success variants:                288 / 288
source best slot cases:                12 / 12
leave-one-case slot cases:             12 / 12
leave-one-seed slot cases:             12 / 12
leave-one-branch slot cases:           11 / 12
leave-one-condition slot cases:        12 / 12
minimum truth-vs-wrong score margin:   0.083628
low-margin cases:                       1
robustness boundary:                   seed_and_condition_robust_but_not_branch_independent
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the blind-envelope rule is not a one-off hyperparameter
accident: many variants recover all saved cases, and held-out seed plus
nominal/source-condition splits remain 12/12. The limit is branch-family
transfer: training only on close14 and evaluating close50 leaves one failure,
and one close50 nominal case has a low truth-versus-wrong margin. This
supports a manuscript detector-handoff claim with an explicit robustness
boundary, not detector-seeded FWI.

## Blind Envelope Policy Stability

The blind-envelope policy-stability audit is:

```text
outputs/summary_tables/063_local_2d_detector_blind_envelope_policy_stability
```

It reads the saved `059` selected-case grid and asks, for each case, how many
of the 288 truth-free blind-envelope variants recover all target slots and how
many distinct successful selected triples appear.

```text
policy label:                         local_2d_detector_blind_envelope_policy_stability_cpu_no_fwi
all-variant success cases:            10 / 12
partial-success cases:                 2 / 12
tuning-sensitive cases:                2 / 12
minimum success fraction:              0.53125
median success fraction:               1.0
single-selection consensus cases:      2 / 12
maximum unique successful selections:  6
tuning-sensitive cases:                target2_close50_linear29p5|seed13|nominal;
                                       target2_close50_linear29p5|seed34|nominal
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: `063` separates robust assignment evidence from policy-tuned
success. All close14 cases and four of six close50 cases are recovered by every
blind-envelope variant. The two policy-sensitive cases are both close50 nominal
cases, so the detector handoff boundary is specifically close50 branch-family
stability under nominal source conditions, not general seed/source-condition
instability.

## Blind Envelope Tuning Sensitivity

The blind-envelope tuning-sensitivity decomposition is:

```text
outputs/summary_tables/066_local_2d_detector_blind_envelope_tuning_sensitivity
```

Key result:

```text
policy label:                         local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi
tuning-sensitive cases:                2
maximum knob effect:                   1.0
top-effect knob:                       structural_weight
top-effect best/worst values:          0.0 / 0.8
structural-weight direction conflict:  true
support-weight direction conflict:     true
span-threshold max effect:             0.0
ready for global tuning fix:           false
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: `066` shows that the close50 nominal fragility is not a simple
global retuning problem. The seed13 nominal case prefers high structural weight
and low support weight, while the seed34 nominal case prefers zero structural
weight and higher support weight. That makes the close50 result an ambiguity
boundary, not a detector-seeded FWI trigger.

## Blind Envelope Reliability Gate

The truth-free blind-envelope reliability gate is:

```text
outputs/summary_tables/069_local_2d_detector_blind_envelope_reliability_gate
```

Key result:

```text
policy label:                         local_2d_detector_blind_envelope_reliability_gate_cpu_no_fwi
stable x-slot drift threshold:        5.0 mm
stable assignment cases:              10 / 12
review assignment cases:               2 / 12
stable assignment all-variant success: 10 / 10
tuning-sensitive cases detected:       2 / 2
tuning-sensitive cases missed:         0
stable min success fraction:           1.0
review max x-slot range:               21.0 mm
ready for reliability claim:           true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Review cases:

```text
target2_close50_linear29p5|seed13|nominal
target2_close50_linear29p5|seed34|nominal
```

Interpretation: `069` turns the close50 policy-stability boundary into a
truth-free confidence diagnostic. Policy-grid x-slot drift at a 5 mm threshold
accepts all close14 cases and four of six close50 cases, while flagging exactly
the two close50 nominal tuning-sensitive cases. This is useful manuscript
evidence for detector reliability and ambiguity labeling, not an FWI trigger.

The threshold-sensitivity follow-up is:

```text
outputs/summary_tables/071_local_2d_detector_blind_envelope_reliability_threshold_sensitivity
```

Key result:

```text
thresholds tested:                    12
clean thresholds:                      5
clean threshold range:                 5.0-19.0 mm
default threshold clean:               true
default tuning-sensitive missed:       0
default false review:                  0
thresholds with false review:          0,1,2,3,4 mm
thresholds with tuning misses:         20,21 mm
ready for reliability claim:           true
ready for detector-seeded FWI:         false
```

Interpretation: the 5 mm gate is not a brittle single cutoff. The clean
threshold interval is wide enough to support confidence/ambiguity wording while
still keeping the detector evidence CPU-side and non-FWI.

## Detector Upper-Bound Policy

The detector upper-bound policy synthesis is:

```text
outputs/summary_tables/039_local_2d_detector_upper_bound_policy_post_selector_audit
```

It consolidates the handoff budget, rank-budget diagnostic, component waveform
gate, and component selector audit into a single paper-facing decision table.

```text
policy label:                         local_2d_detector_upper_bound_policy_cpu_no_fwi
strategies compared:                   6
best rank-gated upper-bound strategy: component_gate_minimal_all_case_upper_bound
best upper-bound objective:            component_balanced
minimal all-case rank-gated budget:   200 triples/case
upper-bound all-truth cases:           12 / 12
component-gate top50 cases:            10 / 12
top50 improvement over simple gate:     2 cases
selector candidates:                  975
selector leave-one-case top1 cases:     0 / 12
ready for rank-gated upper-bound claim: true
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the detector baseline can support a rank-gated upper-bound
claim: the correct triple is recoverable inside a 200-triple/case
component-balanced candidate budget for all 12 saved cases. It cannot support
a deployable detector-seeded FWI queue because validated top-1 selector
recovery is 0/12. This is the current paper-safe detector baseline framing.

## Detector Component Seed Export

The coordinate-only detector component seed export is:

```text
outputs/summary_tables/081_local_2d_detector_component_seed_export
```

It converts the stable case-level launch-contract rows from run `077` into a
component-level x/z seed table for later design work. It does not launch FDTD,
FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

```text
policy label:                         local_2d_detector_component_seed_export_coordinate_only_no_fwi
source cases:                         12
exported seed cases:                  10
exported component rows:              30
excluded review cases:                 2
excluded cases:                       target2_close50_linear29p5|seed13|nominal;target2_close50_linear29p5|seed34|nominal
max exported case seed error:         10.0 mm
median exported case seed error:       3.5 mm
active launch blockers:                6
ready for coordinate seed table:       true
ready for radius/material contract:    false
ready for narrow refinement contract:  false
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: this is a useful engineering artifact, not a launch trigger.
The stable detector rows are now reusable as a coordinate-only seed table, but
the same blockers remain: no radius/material seed, no independent deployable
top-1 selector, branch-transfer gap, review cases, and incomplete per-seed
physics equivalence.

## Detector Lateral-Slot Neighborhood Budget

The lateral x-slot-only neighborhood budget is:

```text
outputs/summary_tables/084_local_2d_detector_lateral_slot_neighborhood_budget
```

It sizes saved-corpus lateral x-slot neighborhoods from the detector seed
errors in run `077` and the coordinate-only seed export in run `081`. It does
not validate detector z-neighborhood coverage and does not launch FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

```text
policy label:                         local_2d_detector_lateral_slot_neighborhood_budget_cpu_no_fwi
source cases:                         12
stable seed cases:                    10
review cases:                          2
max stable lateral x-slot error:      10.0 mm
median stable lateral x-slot error:    3.5 mm
min lateral x half-width all stable:  10.0 mm
branch min lateral x half-widths:     target2_close14:10.0;target2_close50_linear29p5:8.0
stable lateral coverage 5 / 8 / 10:   7 / 9 / 10
h10 step2 lateral-x points/case:      1331
h10 step2 lateral-x stable total:     13310
hypothetical h10 step2 x/z tensor:    1771561
active launch blockers:                6
lateral x-slot design ready:          true
z coverage validated:                 false
x/z neighborhood design ready:        false
radius/material contract ready:       false
narrow refinement contract ready:     false
naive full-tensor refinement ready:   false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Interpretation: a 10 mm lateral x-slot half-width covers all 10 stable exported
detector seed cases in the saved truth evaluation, while 8 mm misses one and
5 mm misses three. The two review cases also fit inside 10 mm by saved lateral
slot error, but remain policy-excluded because they are close50 nominal
drift/review cases. The z dimension is not validated by this artifact: the
1,771,561-point x/z tensor is only a hypothetical warning, while the supported
10 mm / 2 mm lateral-x tensor is 1,331 points per case. This is design-sizing
evidence, not a GPU/FWI launch contract.

## Detector Seed Geometry Error Audit

The matched x/z seed-geometry audit is:

```text
outputs/summary_tables/086_local_2d_detector_seed_geometry_error_audit
```

It joins the detector truth plan in run `017` with the saved launch-contract
rows from run `077`. It computes component-wise matched x/z errors for the
exported detector seeds without running FDTD, FWI, GPU kernels, field FWI,
3D/HPC jobs, or neural-network training.

```text
policy label:                         local_2d_detector_seed_geometry_error_audit_cpu_no_fwi
source cases:                         12
stable seed cases:                    10
review cases:                          2
max stable x error:                   10.0 mm
max stable z error:                   12.0 mm
max stable x/z L-inf error:           12.0 mm
median stable x/z L-inf error:         9.0 mm
stable cases z > lateral error:        7
min x/z half-width all stable:        12.0 mm
source lateral min half-width:        10.0 mm
branch min x/z half-widths:           target2_close14:10.0;target2_close50_linear29p5:12.0
stable x/z coverage 5 / 8 / 10 / 12:  1 / 3 / 8 / 10
h12 step2 x/z points/case:            4826809
x/z seed-neighborhood design ready:   true
narrow refinement contract ready:     false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Interpretation: the earlier 10 mm result was valid only for lateral x-slot
sizing. Direct matched x/z errors need a 12 mm half-width for all 10 stable
exported seed cases, because z errors reach 12 mm and exceed the lateral slot
error in 7/10 stable cases. This closes the coordinate sizing gap for later
seed-neighborhood design, but it still does not provide radius/material seeds
or a refinement/FWI launch contract. A 12 mm / 2 mm x/z tensor is 4,826,809
points per case, so any future refinement must be much narrower or more
structured than a naive full tensor.

## Detector X/Z Seed-Neighborhood Contract

The branch-specific x/z seed-neighborhood contract is:

```text
outputs/summary_tables/088_local_2d_detector_xz_seed_neighborhood_contract
```

It turns the run `086` x/z error audit into a concrete saved-case handoff
contract without running refinement, FWI, GPU kernels, 3D/HPC jobs, or neural
network training.

```text
policy label:                         local_2d_detector_xz_seed_neighborhood_contract_cpu_no_fwi
stable contract cases:                10
review cases excluded:                 2
branch half-widths:                   target2_close14:10;target2_close50_linear29p5:12
global h12 fine x/z points:           48268090
branch-specific fine x/z points:      29936602
fine-grid points saved:               18331488
fine-grid reduction fraction:         0.3797848226436969
branch-specific contract ready:       true
narrow refinement launch ready:       false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Interpretation: a branch-specific contract covers all 10 stable exported seed
cases with 10 mm for `target2_close14` and 12 mm for
`target2_close50_linear29p5`. This is a better design artifact than applying
12 mm globally because it reduces the hypothetical 2 mm x/z coordinate grid by
18.33 million points, about 38%. It remains a coordinate-only saved-case
contract: the two review cases, radius/material seeds, branch-transfer
validation, narrow refinement launch, detector-seeded FWI, and GPU work stay
blocked.

## Detector Radius/Material Prior-Scope Audit

The post-table-pack radius/material prior-scope audit is:

```text
outputs/summary_tables/089_local_2d_detector_radius_material_prior_scope_audit
```

It separates controlled synthetic design priors from detector-inferred
radius/material seeds. It reads the saved detector command plan, the launch
contract, the branch-specific x/z contract, and the fixed synthetic material
constants in `config.py`. It does not run refinement, FWI, GPU kernels,
3D/HPC jobs, field FWI, or neural-network training.

```text
policy label:                         local_2d_detector_radius_material_prior_scope_audit_cpu_no_fwi
source cases:                         12
stable controlled-prior cases:        10
review cases excluded:                 2
radius-prior cases:                   12
radius patterns:                      5,6,8 mm
material prior parameters:             4
detector radius seeds:                 0
detector material seeds:               0
controlled synthetic prior ready:      true
detector-inferred radius/material:     false
field transfer ready:                  false
narrow refinement launch ready:        false
detector-seeded FWI ready:             false
gpu priority:                         none
```

Interpretation: the stable saved synthetic detector cases can use the known
truth radius list and fixed material constants as a controlled synthetic
prior-scope contract. That is a paper-method boundary, not a detector
capability claim. The detector still has no inferred radius/material seed, so
review cases, field transfer, narrow refinement, detector-seeded FWI, and GPU
work remain blocked.

## Controlled-Prior Refinement Budget

The controlled-prior refinement budget sidecar is:

```text
outputs/summary_tables/090_local_2d_detector_controlled_prior_refinement_budget
```

It asks what the branch-specific x/z contract would cost under three
radius-scope assumptions. This is still a CPU-only budget audit, not a
refinement/FWI/GPU launch.

```text
policy label:                         local_2d_detector_controlled_prior_refinement_budget_cpu_no_fwi
stable controlled-prior cases:        10
review cases excluded:                 2
radius pattern:                       5,6,8 mm
fixed-slot radius combinations:        1
known-radius permutations:             6
independent known-radius choices:     27
fixed-slot fine points:               29936602
fixed-slot coarse points:             156250
known-radius permutation fine points: 179619612
independent radius-choice fine points: 808288254
permutation/fixed multiplier:          6.0
independent/fixed multiplier:         27.0
controlled fixed-radius budget ready: true
independent radius search ready:       false
refinement launch ready:               false
detector-seeded FWI ready:             false
gpu priority:                         none
```

Interpretation: exact controlled slot radii keep the stable-case fine grid at
the run `088` branch-specific x/z budget. If radius-to-slot assignment is not
trusted and the known radius set must be permuted, the budget grows by 6x. If
each slot independently searches the known radius set, the budget grows by
27x. This supports a paper-safe fixed-radius synthetic ablation plan only. It
does not justify an independent radius search, field transfer, refinement/FWI
launch, or GPU work.

## Manuscript Table-Pack Integration

The current combined local 2D and field manuscript table pack is:

```text
outputs/summary_tables/087_local_2d_field_manuscript_table_pack
```

Key result:

```text
policy label:                         local_2d_field_manuscript_table_pack_ready_no_gpu
claim rows:                           32
figure rows:                          31
metric rows:                          261
auxiliary policy metrics:             245
detector geometry-selector case CV:   2 / 12
detector selector-gap failed cases:    9 / 12
detector selector-gap dominant loss:   signed_gap_prior_score
detector counterfactual variants:      44
detector counterfactual best cases:    3 / 12
detector counterfactual gain over base: 0
detector image-objective top50 cases:  0 / 12
detector image-objective top1000 cases: 6 / 12
detector target-failure missing target1 cases: 7 / 9
detector target-failure multi-target cases: 5 / 9
detector target-failure dominant missing target: target1
detector depth/slot prior best cases: 5 / 12
detector depth/slot prior gain:       2
detector depth/slot prior ready for FWI: false
detector slot-component assembly cases: 12 / 12
detector slot-component ready for FWI: false
detector blind-envelope slot cases:  12 / 12
detector blind-envelope leave-one cases: 12 / 12
detector blind-envelope uses branch slots: false
detector blind-envelope ready for FWI: false
detector blind-envelope full-success variants: 117 / 288
detector blind-envelope leave-one-branch cases: 11 / 12
detector blind-envelope min margin:   0.083628
detector blind-envelope robustness boundary: seed_and_condition_robust_but_not_branch_independent
detector blind-envelope robustness ready for FWI: false
detector blind-envelope all-variant cases: 10 / 12
detector blind-envelope tuning-sensitive cases: 2 / 12
detector blind-envelope min success fraction: 0.53125
detector blind-envelope stability ready for FWI: false
detector blind-envelope tuning max knob effect: 1.0
detector blind-envelope tuning structural conflict: true
detector blind-envelope tuning support conflict: true
detector blind-envelope tuning ready for FWI: false
detector blind-envelope reliability stable cases: 10 / 12
detector blind-envelope reliability review cases: 2 / 12
detector blind-envelope reliability tuning missed: 0
detector blind-envelope reliability ready for claim: true
detector blind-envelope reliability ready for FWI: false
detector blind-envelope reliability clean thresholds: 5
detector blind-envelope reliability clean threshold range: 5.0-19.0 mm
detector blind-envelope reliability default threshold clean: true
detector blind-envelope reliability threshold ready for FWI: false
detector physics-link review cases:   2 / 12
detector physics-link near-boundary nominal reviews: 2 / 2
detector physics-link close50 nominal review fraction: 2 / 3
detector physics-link review x-ambiguous cases: 1 / 2
detector physics-link per-seed equivalence: false
detector physics-link ready for FWI:  false
detector refinement-contract seed-table cases: 10 / 12
detector refinement-contract review cases: 2 / 12
detector refinement-contract active blockers: 6
detector refinement-contract radius/material seeds: false / false
detector refinement-contract narrow refinement: false
detector refinement-contract ready for FWI: false
detector component seed exported cases: 10 / 12
detector component seed exported rows: 30
detector component seed ready for FWI: false
detector lateral-slot min half-width: 10.0 mm
detector lateral-slot coverage 5/8/10 mm: 7 / 9 / 10
detector lateral-slot h10 step2 points/case: 1331
detector hypothetical x/z tensor points/case: 1771561
detector lateral-slot z coverage validated: false
detector lateral-slot x/z design ready: false
detector lateral-slot ready for FWI: false
detector seed-geometry x/z half-width: 12.0 mm
detector seed-geometry max z error:   12.0 mm
detector seed-geometry z>lateral cases: 7 / 10
detector seed-geometry h12 step2 points/case: 4826809
detector seed-geometry ready for FWI: false
detector sampling-boundary claim ready: true
detector sampling-boundary review cases: 2 / 12
detector sampling-boundary reviews below clean: 2 / 2
detector sampling-boundary close50 nominal reviews: 2 / 3
detector sampling-boundary close50 source-mismatch reviews: 0 / 3
detector sampling-boundary per-seed equivalence: false
detector sampling-boundary ready for FWI: false
field spatial transfer long covered:  1 / 8
field anchor interval short inside:   3 / 3
field dimensionality is 3D survey:    false
field dimensionality short QC ready:  true
field dimensionality long transfer:   false
field time-zero ladder short QC:      true
field time-zero ladder content-only QC: true
field time-zero ladder leave-one content: false
field time-zero ladder content half-range: 0.009823 ns
field time-zero ladder rows:          8
field time-zero ladder absolute t0:   false
field time-zero ladder field FWI:     false
field short-anchor content-only supported: true
field short-anchor leave-one supported cases: 1 / 3
field short-anchor leave-one degraded cases: 2 / 3
field short-anchor spatial residual range: 29.997 mm
field short-anchor spatial residual half-range: 14.9985 mm
field short-anchor spatial single translation: false
field short-anchor spatial calibration: false
field short-anchor spatial field FWI: false
field inversion-readiness supported gates: 2 / 8
field inversion-readiness blocked gates: 6 / 8
field inversion-readiness depth-scale QC: true
field inversion-readiness cover depth: false
field inversion-readiness field FWI: false
field inversion-readiness 3D/HPC: false
field short-anchor radius weak sides: 4 / 4
field short-anchor radius mismatch pairs: 2 / 2
field short-anchor common-radius near-ties: 2 / 2
field short-anchor radius seed: false
field short-anchor radius FWI: false
field short-anchor signed morphology pairs: 2 / 2
field short-anchor min signed corr: 0.939469
field short-anchor signed morphology FWI: false
field signed-morphology supported threshold combos: 36 / 320
field signed-morphology moderate threshold ready: true
field signed-morphology strict claim ready: false
field signed-morphology sensitivity FWI: false
detector upper-bound ready for claim: true
detector upper-bound ready for FWI:   false
gpu priority:                         none
```

Interpretation: the detector selector-gap decomposition, selector
counterfactual sensitivity, image-objective rank diagnostic, target-failure
taxonomy, depth/slot prior probe, slot-component assembly probe, blind
component-envelope assembly probe, blind-envelope robustness audit,
blind-envelope policy-stability audit, blind-envelope tuning-sensitivity
decomposition, blind-envelope reliability gate, reliability-threshold
sensitivity, detector/physics ambiguity-link audit, detector refinement
launch-contract audit, detector component seed export, detector
lateral-slot neighborhood budget, matched x/z seed-geometry audit,
detector/sampling-boundary integration,
geometry-family selector, detector upper-bound policy, field
spatial-transfer guardrail, short-anchor interval reconciliation, field
dimensionality/HPC decision, post-leave-one field time-zero evidence ladder,
short-anchor leave-one/content-only audit, and short-anchor spatial
consistency audit plus field inversion/HPC readiness synthesis and
short-anchor radius-degeneracy, signed-morphology, and signed-morphology
threshold-sensitivity audits are now
integrated into the current cross-domain manuscript table pack as auxiliary
evidence. This keeps the detector role paper-facing and bounded: modest
selector improvement, failure-mode decomposition, failed scalar-retuning
attempt, failed saved-image-objective rank gate, target-level failure
diagnosis, modest depth-prior improvement, rank-gated upper-bound evidence,
a non-slot-coded component-envelope assignment result, and an explicit
seed/condition-vs-branch robustness and close50 policy-stability boundary with
a truth-free reliability gate whose 5 mm cutoff is inside a clean 5-19 mm
threshold interval, plus a physics-link audit showing that the detector review
cases are localized to the close50 29.5 mm nominal branch 0.5 mm below the
paper-safe 30 mm clean threshold. The new sampling-boundary integration keeps
those detector review cases tied to the sub-30 caveat while blocking per-seed
physics equivalence and detector-seeded FWI. That link is branch/variant evidence, not a
per-seed equivalence claim, because only one of the two review cases is
x-ambiguous in the saved coordinate-confidence rows. The launch-contract audit
adds that 10/12 stable detector rows can be exported as a saved x/z component
seed table, but radius/material seeds, independent top-1 validation, branch
transfer, review-case closure, and per-seed equivalence still block narrow
refinement or detector-seeded FWI. The corrected lateral-slot budget audit
shows that a 10 mm lateral x-slot half-width covers all stable exported cases,
while detector z coverage is not validated and a 10 mm / 2 mm x/z tensor would
be 1,771,561 points per case. That is design-sizing evidence, not a launch
trigger. The matched x/z audit then closes the coordinate sizing question:
stable exported seeds need 12 mm x/z half-width because z errors reach 12 mm,
but the 4,826,809-point h12/step2 tensor and unchanged radius/material and
review-case blockers still prevent a refinement/FWI launch. The follow-on
x/z seed-neighborhood contract makes that sizing branch-specific: close14
uses 10 mm and close50-linear29.5 uses 12 mm, saving 18.33 million fine
2 mm coordinate-grid points relative to global h12 while still excluding the
two review cases and blocking refinement/FWI/GPU work. It also keeps
radius/material usage bounded to controlled synthetic priors, not
detector-inferred seeds: post-pack run `089` shows all 12 saved synthetic cases
share the 5,6,8 mm radius design prior and fixed material constants, while
detector radius/material seeds remain 0/12 and refinement/FWI/GPU stays
blocked. Post-pack run `090` then quantifies the cost of using that controlled
radius scope: exact slot radii keep the stable fine grid at 29.94 million
points, known-radius permutations cost 179.62 million points, and independent
known-radius choices cost 808.29 million points. It also keeps measured field
data bounded to short-profile relative timing QC, apparent-depth scale QC,
signed waveform morphology QC, finite threshold-margin evidence, and
post-bundle signal-contrast QC from run `131` (4/4 side windows supported,
minimum event/pre-event RMS ratio 4.13x) with the run `132` sensitivity caveat
that only 13/27 tested contrast-window combinations support all four side
windows. Run `133` packages those contrast figures into the current 29-row
field publication bundle with 25 claim boundaries, and run `134` verifies that
all 29 source figures already have figure notes. Run `135` then shows the
broad event-window contrast regime is robust across all 9 tested aperture/noise
settings, while strict tight/default/broad window invariance remains false.
Run `136` maps those latest field positives against inversion blockers: all
six positive evidence axes support a scoped field morphology supplement, but
all nine blocker axes remain unresolved and six are critical blockers. This is
not absolute time-zero, profile spatial calibration, amplitude calibration,
strict window-invariant contrast, cover-depth/radius recovery, 3D/HPC, or FWI.
Finally, controlled fixed-radius pilot run `1340` improves one non-overlapping
stable detector seed from 9 mm to 5 mm max x/z error but does not fully recover
the right bar in one pass; the failed run `1339` shows exact radii can make
some stable detector seeds geometrically overlapping. The next detector-side
step is therefore seed non-overlap preflight/repair, not a broad GPU queue.
Run `091` performs that preflight: 7/10 stable seeds are direct-ready for
future one-case-at-a-time fixed-radius pilots, while three close14 seeds are
overlap-blocked and need at most 2 mm of repair.
Run `092` designs those truth-free repairs: all three overlap-blocked seeds are
repairable by shifting the middle component 2 mm left, but the repaired seeds
still need waveform validation before any broader claim.
Run `1341` performs that validation for `target2_close14|seed21|nominal`: the
repaired exact-radius seed is runnable and improves from 4 mm to 2 mm max x/z
error, but one pass leaves 2 mm lateral residuals on the middle/right bars.
Run `1342` shows why: when the near-tie middle branch `x=250,z=89` is
preserved, target2 unlocks to `x=264,z=91` and the max error drops to 1 mm.
The detector-refinement path therefore becomes a narrow branch-preserving or
coupled middle-right selection problem, not a broad GPU queue or FWI launch.
Run `093` converts that pair into a CPU policy result: the middle near-tie
branch is within the proposed 0.01 absolute / 10% relative preservation window,
target2 true lateral position is unavailable after the greedy middle branch,
and it unlocks after retaining the near-tie middle branch.
Run `1343` executes the next narrow coupled-search diagnostic: three target1
middle branches fall inside the preservation window, 55 target2 candidates are
evaluated, and the objective-best row is also the oracle-best row with
`target1=(250,91)`, `target2=(264,89)`, and 1 mm final L-infinity error. This
confirms that branch preservation can improve the repaired close14 case from
the run `1341` 2 mm greedy residual to 1 mm without requiring a broad GPU
queue or detector-seeded FWI.
Run `094` then scans the saved coordinate optimizer archive for the same
preservation-window mechanism. It audits 747 candidate surfaces and finds 13
retained-but-not-selected truth-lateral branches, concentrated mostly in
target2 (9/373). This makes branch preservation an archive-backed CPU policy
direction rather than a one-off 1343 artifact, while still blocking broad GPU
queues and detector-seeded FWI.
Run `095` triages those rows by coordinate impact: 7/13 improve full x/z
L-infinity error if the retained truth-lateral branch is selected, 6/13 are
same-error objective near-ties, and 0/13 are worse. Three older close50 target2
rows are possible narrow coupled-probe candidates, but the gate remains closed
without a case-specific coupled-search design and manuscript rationale.
Run `096` then sweeps preservation thresholds. The default 0.01 absolute / 10%
relative rule recovers 13/17 missed-available truth-lateral branches with 4.598
extra retained candidates per step; the tested maximum is 14/17 at 0.01 / 20%,
but that costs 6.317 extra candidates per step. This supports the default rule
as a balanced manuscript threshold, not a max-fanout GPU launch policy.

## Validation

Focused tests:

```text
tests/test_local_2d_detector_seed_geometry_error_audit.py
tests/test_local_2d_detector_xz_seed_neighborhood_contract.py
tests/test_local_2d_detector_radius_material_prior_scope_audit.py
tests/test_local_2d_detector_controlled_prior_refinement_budget.py
tests/test_local_2d_detector_exact_radius_seed_nonoverlap_preflight.py
tests/test_local_2d_detector_exact_radius_seed_repair_design.py
tests/test_local_2d_detector_branch_lock_counterfactual_synthesis.py
tests/test_local_2d_detector_coupled_middle_right_search.py
tests/test_local_2d_branch_preservation_archive_audit.py
tests/test_local_2d_branch_preservation_actionability.py
tests/test_local_2d_branch_preservation_threshold_sensitivity.py
tests/test_local_2d_field_manuscript_table_pack.py
tests/test_local_2d_detector_refinement_neighborhood_budget.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_publication_source_figure_notes_backfill.py
tests/test_gssi_field_short_anchor_signed_morphology_timing_margin.py
tests/test_gssi_field_short_anchor_signal_contrast_audit.py
tests/test_gssi_field_short_anchor_signal_contrast_sensitivity.py
tests/test_gssi_field_short_anchor_signal_contrast_regime_synthesis.py
tests/test_gssi_field_inversion_blocker_map.py
69 passed
```

Full suite:

```text
884 passed
```

Earlier broad focused detector/field regression:

```text
tests/test_local_2d_detector_baseline_synthesis.py
...
tests/test_local_2d_field_manuscript_table_pack.py
116 passed
```

Figure validation:

```text
local_2d_detector_baseline_synthesis.png: 2365x869,
nonwhite=0.4368, dynamic range=255
local_2d_detector_assignment_failure_taxonomy.png: 2484x903,
nonwhite=0.3702, dynamic range=255
local_2d_detector_assignment_selector.png: 2484x903,
nonwhite=0.0872, dynamic range=255
local_2d_detector_image_objective_gate.png: 2484x903,
nonwhite=0.0831, dynamic range=255
local_2d_detector_handoff_budget.png: 2739x988,
nonwhite=0.1999, dynamic range=255
local_2d_detector_alltriples_gate_pilot.png: 2535x937,
nonwhite=0.1713, dynamic range=255
local_2d_detector_rank_budget_diagnostic.png: 2535x937,
nonwhite=0.1480, dynamic range=255
local_2d_detector_component_waveform_gate.png: 2535x937,
nonwhite=0.1497, dynamic range=255
local_2d_detector_component_selector_audit.png: 2467x903,
nonwhite=0.1131, dynamic range=255
local_2d_detector_geometry_family_selector.png: 2467x903,
nonwhite=0.1698, dynamic range=255
local_2d_detector_selector_gap_decomposition.png: 2603x937,
nonwhite=0.1668, dynamic range=255
local_2d_detector_selector_counterfactual_sensitivity.png: 2569x903,
nonwhite=0.1028, dynamic range=255
local_2d_detector_image_objective_rank_diagnostic.png: 2535x903,
nonwhite=0.3235, dynamic range=255
local_2d_detector_target_failure_taxonomy.png: 2365x835,
nonwhite=0.4825, dynamic range=255
local_2d_detector_depth_slot_prior_probe.png: 1977x835,
nonwhite=0.5919, dynamic range=255
local_2d_detector_slot_component_assembly_probe.png: 2190x835,
nonwhite=0.4913, dynamic range=255
local_2d_detector_blind_component_envelope_assembly.png: 2365x835,
nonwhite=0.2388, dynamic range=255
local_2d_detector_blind_envelope_robustness_audit.png: 2365x835,
nonwhite=0.3570, dynamic range=255
local_2d_detector_blind_envelope_policy_stability.png: 2365x835,
nonwhite=0.3306, dynamic range=255
local_2d_detector_blind_envelope_tuning_sensitivity.png: 2535x903,
nonwhite=0.1182, dynamic range=255
local_2d_detector_blind_envelope_reliability_gate.png: 2535x903,
nonwhite=0.3004, dynamic range=255
local_2d_detector_blind_envelope_reliability_threshold_sensitivity.png: 2365x835,
nonwhite=0.0808, dynamic range=255
local_2d_detector_physics_ambiguity_link.png: 2399x920,
nonwhite=0.1011, dynamic range=255
local_2d_detector_refinement_launch_contract_audit.png: 2229x869,
nonwhite=0.2461, dynamic range=255
local_2d_detector_seed_geometry_error_audit.png: 2263x835,
nonwhite=0.1559, dynamic range=255
local_2d_detector_xz_seed_neighborhood_contract.png: 2314x835,
nonwhite=0.3583, dynamic range=255
local_2d_detector_exact_radius_seed_nonoverlap_preflight.png: 2314x1005,
nonwhite=0.2060, dynamic range=255
local_2d_detector_exact_radius_seed_repair_design.png: 1685x869,
nonwhite=0.1833, dynamic range=255
run 1341 coordinate_confidence_margins.png: 1804x665,
nonwhite=0.0452, dynamic range=238
run 1341 coordinate_radius_decision_panel.png: 2127x1583,
nonwhite=0.0981, dynamic range=241
run 1341 system_scene_geometry.png: 1595x1028,
nonwhite=0.7194, dynamic range=255
run 1342 coordinate_confidence_margins.png: 1804x665,
nonwhite=0.0361, dynamic range=238
run 1342 coordinate_radius_decision_panel.png: 2127x1583,
nonwhite=0.0875, dynamic range=241
run 1342 system_scene_geometry.png: 1625x1028,
nonwhite=0.7065, dynamic range=255
local_2d_detector_branch_lock_counterfactual_synthesis.png: 2144x801,
nonwhite=0.4995, dynamic range=255
coupled_middle_right_branch_preserving_search.png: 2127x784,
nonwhite=0.4325, dynamic range=255
local_2d_branch_preservation_archive_audit.png: 2331x835,
nonwhite=0.2243, dynamic range=255
local_2d_branch_preservation_actionability.png: 2263x835,
nonwhite=0.3023, dynamic range=255
local_2d_branch_preservation_threshold_sensitivity.png: 2227x903,
nonwhite=0.6313, dynamic range=255
local_2d_detector_upper_bound_policy.png: 2705x937,
nonwhite=0.3698, dynamic range=255
field_time_zero_evidence_ladder.png: 2535x903,
nonwhite=0.2056, dynamic range=255
field_short_anchor_leave_one_audit.png: 2535x903,
nonwhite=0.1879, dynamic range=255
field_time_zero_ladder_post_leave_one.png: 2535x903,
nonwhite=0.2474, dynamic range=255
field_short_anchor_spatial_consistency_audit.png: 2195x835,
nonwhite=0.3272, dynamic range=255
field_inversion_readiness_synthesis.png: 2263x886,
nonwhite=0.1187, dynamic range=255
field_publication_claim_bundle.png (run 133): 2484x1968,
nonwhite=0.0701, dynamic range=255
field_short_anchor_signal_contrast_regime_synthesis.png: 2433x818,
nonwhite=0.2778, dynamic range=255
field_inversion_blocker_map.png: 2484x1039,
nonwhite=0.2673, dynamic range=255
local_2d_field_manuscript_table_pack.png: 1587x835,
nonwhite=0.3036, dynamic range=255
```
