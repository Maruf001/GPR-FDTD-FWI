# Local 2D And Field Manuscript Positioning

Date: 2026-06-18

## Scope

This update records the local DGX-side manuscript-positioning work after the
field timing-discriminant scorecard. No FDTD/FWI run, neural-network training,
field FWI, 3D/HPC job, or broad GPU sweep was launched.

## Field Claim Viability

The field claim-viability scorecard is:

```text
outputs/summary_tables/013_local_gssi_field_claim_viability_scorecard_post_timing_discriminant
```

Key result:

```text
policy label:                    local_gssi_field_claim_viability_scorecard_ready_no_field_fwi
claim rows:                      13
supported rows:                   3
scope-limited rows:               5
context-only rows:                1
rejected-control rows:            1
blocked rows:                     3
ready for 2D field QC:            true
ready for absolute time-zero:     false
ready for cover-depth recovery:   false
ready for radius recovery:        false
ready for field FWI:              false
ready for 3D/HPC:                 false
gpu priority:                     none
```

Interpretation: the measured GSSI data support scoped 2D line-profile QC,
short-pair relative timing, and current field-figure claim boundaries. They do
not support absolute time-zero, cover-depth recovery, radius recovery, field
FWI, 3D, HPC, or relabeling of synthetic known-truth resolution claims.

## Manuscript Contribution Matrix

The local 2D manuscript contribution matrix is:

```text
outputs/summary_tables/014_local_2d_manuscript_contribution_matrix_post_field_viability
```

Key result:

```text
policy label:                         local_2d_manuscript_contribution_matrix_ready_no_gpu
contribution rows:                    10
ready rows:                            9
deferred rows:                         1
review rows:                           0
synthetic immediate GPU candidates:    0
synthetic conditional GPU candidates:  0
field ready for 2D QC:                 true
field ready for FWI:                   false
field ready for 3D/HPC:                false
gpu priority:                          none
```

Recommended framing:

```text
Controlled acquisition-aware identifiability and ambiguity-margin study for
closely spaced multi-rebar 2D GPR inversion, with measured field data used only
as scoped 2D QC and timing-boundary evidence.
```

Interpretation: the project is now best positioned as a controlled synthetic
2D identifiability and ambiguity-margin paper, not as a first rebar-FWI paper
or a field-validated cover-depth/radius recovery paper. The neural-network
thread remains deferred as literature/baseline context unless a labeled
benchmark is deliberately designed.

## Baseline Readiness

The current baseline-readiness audit is:

```text
outputs/summary_tables/015_local_2d_baseline_readiness_audit_post_contribution_matrix
```

Key result:

```text
policy label:                         local_2d_baseline_readiness_cpu_first_no_gpu
baseline rows:                        6
ready baseline rows:                  2
partial baseline rows:                1
field-context rows:                   1
blocked or contract-needed rows:      2
single-detector scenarios:            96
single-detector hit rate:             1.000
two-stage rows:                       10
two-stage exact fraction:             1.000
two-stage strong / weak rows:         3 / 7
multi-rebar assignment candidates:    9
immediate GPU candidates:             0
conditional GPU candidates:           0
gpu priority:                         none
```

Interpretation: existing detector outputs are ready as location-seed and
single-rebar detector-to-refinement baseline evidence. Multi-rebar detector
assignment is useful as seed-stage evidence. Field hyperbola overlays remain
context only, and field hyperbola/time-zero degeneracy remains a guardrail.
The main baseline gap is now explicit: same-case detector/database comparisons
for the current close14/close50 manuscript claims need a CPU-first contract
before any GPU escalation.

## Baseline Comparison Contract

The current CPU-first baseline comparison contract is:

```text
outputs/summary_tables/016_local_2d_baseline_comparison_contract_post_readiness_audit
```

Key result:

```text
policy label:                    local_2d_baseline_comparison_contract_cpu_first_not_launched
contract rows:                   5
CPU-first contracts:             3
launch-now contracts:            0
GPU-allowed contracts:           0
highest-priority contract:       target2_close14_same_case_detector_baseline
immediate GPU candidates:        0
conditional GPU candidates:      0
gpu priority:                    none
```

Interpretation: the next baseline work should not be an immediate run. It
should first implement a CPU-first, skip-existing same-case detector/database
baseline runner for the current close14 objective-limit and close50 29.5 mm
seed-frequency claims. The target1 detector baseline is optional and lower
priority. Field hyperbola and neural-network baselines remain guardrail/future
work, not launch targets.

## Detector Interface Support

The detector scripts now expose the acquisition parameters needed by the
baseline contract:

```text
run_rebar_detection_pipeline.py --tx-rx-offset-mm ... --receiver-sampling ...
run_rebar_detection_benchmark.py --tx-rx-offset-mm ... --receiver-sampling ...
```

This is a code-path readiness change only. It does not launch a detector,
FDTD/FWI, GPU, field FWI, 3D/HPC, or neural-network run. Focused detector tests
cover explicit Tx/Rx offsets and linear receiver sampling.

## Detector Baseline Synthesis

The CPU same-case detector-baseline command plan and synthesis are:

```text
outputs/summary_tables/017_local_2d_detector_baseline_command_plan_post_interface_patch
outputs/summary_tables/018_local_2d_detector_baseline_synthesis_post_cpu_runs
```

The detector runs are:

```text
outputs/experiments/1326-1337_local2d_detector_baseline_*
```

Key result:

```text
policy label:                  local_2d_detector_baseline_synthesis_simple_detector_under_resolves
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

Interpretation: this simple hyperbola-energy detector is a weak image-feature
baseline, not a positive competitor. For close14 it detects the close 250/264
mm pair but misses the 190 mm bar. For close50 linear 29.5 mm it detects only
the middle 250 mm cue and does not track the optimizer's seed13-specific
x-ambiguity caveat. The paper-safe use is to say that the controlled
FWI/coordinate objective does more than naive detector seeding, not that this
detector reproduces the FWI ambiguity tiers.

## Detector Parameter Sensitivity

The saved-B-scan detector parameter sensitivity is:

```text
outputs/summary_tables/020_local_2d_detector_parameter_sensitivity_post_rank_depth_metrics
```

Key result:

```text
policy label:                         local_2d_detector_parameter_sensitivity_saved_bscan_cpu
configurations:                        81
case/config rows:                      972
rescued cases:                         12 / 12
best config:                           median_top40_moderate12_single667
best-config all-truth cases:            12 / 12
best-config mean max assigned rank:      23.42
best-config worst max assigned rank:     36.0
backend:                               saved-B-scan CPU rescore
GPU used:                              false
```

Interpretation: the original negative detector-baseline result is a
parameter-setting artifact. A tuned detector configuration can place all three
truth locations in the candidate list for every saved close14/close50 case.
However, the required ranks can be deep, especially in close50, so this is
candidate-list recoverability rather than a clean standalone top-pick detector
claim. The useful next local 2D question is a bounded detector-to-assignment or
detector-to-FWI policy, not a broad GPU sweep.

## Detector Candidate-Rank Policy

The detector candidate-rank policy is:

```text
outputs/summary_tables/021_local_2d_detector_candidate_rank_policy_post_sensitivity
```

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

Interpretation: a single shared tuned detector policy needs top-40 candidates
to cover the current saved close14/close50 cases. Branch-specific top-20
policies exist, but they are not blind deployment rules. This supports a
rank-gated detector-to-FWI or detector-to-assignment pilot, not a claim that a
simple detector alone resolves the close-spacing ambiguity.

## Detector Blind Assignment

The detector blind-assignment policy synthesis is:

```text
outputs/summary_tables/022_local_2d_detector_blind_assignment_policy_post_rank_sensitivity
outputs/summary_tables/023_local_2d_detector_blind_assignment_policy_with_span_bonus
```

Score-only result:

```text
policy label:                       local_2d_detector_blind_assignment_policy_saved_bscan_cpu
case/policy rows:                   11664
config-assignment policies:           972
full-recovery policies:                 0
best config:                        median_top40_dense4_baseline
best assignment policy:             top40_minx20
best all-truth cases:                   1 / 12
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
close14 branch-best all-truth:          2 / 6
close50 branch-best all-truth:          1 / 6
```

Interpretation: the tuned detector has truth-containing candidate lists, but a
simple blind score/spread assignment policy and span/diversity bonuses do not
recover the three-rebar geometry. Detector-to-FWI should therefore be
rank-gated, use a stronger assignment model, or be explicitly described as an
oracle/upper-bound handoff.

## Detector Assignment Taxonomy

The detector assignment failure taxonomy is:

```text
outputs/summary_tables/025_local_2d_detector_assignment_failure_taxonomy_policy_oracle
```

This run reads saved assignment rows from `023` and chooses the best row per
case across the blind-assignment policy grid. It is a per-case policy oracle,
not a deployable shared policy.

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

Interpretation: close14 contains enough candidate-list signal for a per-case
assignment-policy oracle to recover all six saved cases, but the shared blind
assignment policy still reaches only two all-truth cases overall. That is a
useful positive upper bound and a useful negative deployment result. The next
local 2D experiment should learn or justify assignment-policy selection from
case features, or gate candidate triples through a small downstream objective,
before spending GPU time on detector-seeded FWI.

## Detector Assignment Selector

The truth-free detector assignment selector audit is:

```text
outputs/summary_tables/026_local_2d_detector_assignment_selector_truth_free_feature_grid
```

This run scores the saved assignment rows using only rank, x-span, center,
gap-balance, z-spread, and budget features. It compares those selectors against
the fixed shared blind policy and the per-case policy oracle.

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

Interpretation: the easy selector route failed. Rank/span/center/z-spread
features alone do not explain the per-case oracle gain and are weaker than the
fixed shared policy. A detector-seeded FWI pilot should therefore either use a
small downstream objective gate over candidate triples or be presented as an
explicit rank-gated/oracle upper-bound, not as a solved automatic detector
handoff.

## Detector Image-Objective Gate

The saved-B-scan image-objective gate is:

```text
outputs/summary_tables/027_local_2d_detector_image_objective_gate_saved_bscan
```

This run scores assigned detector triples against the saved B-scans with
Gaussian hyperbola masks over detector time-offset families. It is a CPU-only
proxy image objective, not FDTD/FWI.

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
GPU used:                              false
```

Interpretation: a shallow image-objective gate also failed. It mostly chases
central/right high-energy hyperbolas and systematically misses the left target.
The local 2D detector handoff is therefore not ready for broad GPU/FWI work.
The remaining useful path is either a stronger waveform/objective gate, more
case data for a learned selector, or an explicitly labeled rank-gated/oracle
upper-bound experiment.

## Detector-to-FWI Handoff Budget

The detector handoff-budget synthesis is:

```text
outputs/summary_tables/029_local_2d_detector_handoff_budget
```

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
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: detector-seeded FWI is still not a narrow run. The detector can
make truth-containing candidate lists, but the cheapest all-case candidate-list
handoff is still 1,140 candidate triples per case. A stronger CPU
waveform/objective gate should shrink that set before any GPU/FWI spend.

## Detector All-Top20 Triple Gate Pilot

The branch-specific all-top20 triple gate pilot is:

```text
outputs/summary_tables/030_local_2d_detector_alltriples_gate_pilot
```

```text
policy label:                         local_2d_detector_alltriples_gate_pilot_cpu_no_fwi
candidate-triple rows:             12180
objectives tested:                     6
best top1 all-truth cases:             0 / 12
best top10 objective:                 span_bonus
best top10 all-truth cases:            2 / 12
best top50 objective:                 span_bonus
best top50 all-truth cases:            8 / 12
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: enumerating and scoring the branch-specific top-20 triple
space does not rescue the detector handoff. Simple score/span/min/mask gates
still do not select an all-truth triple at rank 1. This keeps the local 2D
path CPU-first and argues against detector-seeded GPU/FWI until a richer
waveform gate or explicitly labeled oracle/rank-gated upper-bound is defined.

## Target1 Probe-Readiness Scorecard

The CPU-only target1 probe-readiness scorecard is:

```text
outputs/summary_tables/028_local_2d_target1_probe_readiness_scorecard
```

This run consolidates the target1 weak-exact audit, acquisition-confidence
surface, source-density exception map, and next-question matrix into explicit
GPU-probe gates.

```text
policy label:                         local_2d_target1_probe_readiness_requires_new_hypothesis
scorecard rows:                       10
triggered gates:                       0
GPU action count:                      0
ready for target1 GPU probe:           false
target1 canonical rows:              133
target1 exact-geometry rows:         133
target1 weak-exact base rows:         43
target1 late_high accepted rows:     132
modern exception series:               0
legacy exception series:               1
terminal 11-source worse count:        2
gpu priority:                          none
```

Interpretation: target1 is closed under the current archived hypothesis. The
problem is not x/z/r localization because all canonical target1 rows are exact;
the open point is confidence-policy wording. Modern ringdown050 weak-exact
rows are secondary-confirmed, source-density escalation is nonmonotonic, and
the 11-source endpoints are worse. A future target1 GPU probe should require a
new objective, geometry, or acquisition hypothesis before launch.

## Field Dimensionality And HPC Decision

The current field dimensionality/HPC decision card is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/106_gssi51600s_field_hpc_dimensionality_decision_card
```

Key result:

```text
policy label:                  gssi51600s_field_hpc_dimensionality_decision_2d_only_no_hpc
field geometry type:            independent_2d_line_profiles
is 3D survey:                   false
ready for 2D QC:                true
ready for 3D HPC:               false
ready for field FWI:            false
ready for absolute time-zero:   false
ready for cover-depth recovery: false
ready for radius recovery:      false
field HPC priority:             none
```

Interpretation: the local GSSI 51600S data are four independent dense 2D line
profiles. They are useful for local field timing, repeatability, and
supported-interval visual QC. They are not currently a 3D survey, field-FWI
benchmark, radius-recovery dataset, cover-depth-recovery dataset, or HPC
workload. Field-side HPC should wait for external survey layout metadata,
calibrated target geometry, and absolute timing/depth controls, or for a new
controlled field acquisition.

## Field Support/Publication/Policy Refresh

The current field publication and policy endpoints are:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/110_gssi51600s_field_event_support_tiers_post_timing_discriminant_hpc
outputs/field_experiments/local_gssi_51600s_2026_06_09/112_gssi51600s_field_dataset_policy_synthesis_post_event_support_timing_discriminant_hpc_bundle
outputs/field_experiments/local_gssi_51600s_2026_06_09/130_gssi51600s_field_publication_claim_bundle_post_signed_morphology_timing_margin
```

Key result:

```text
event-support tier rows:            11
publication bundle rows:             27 figures / 24 claim boundaries
timing discriminant included:        true
timing score rows:                   4
short non-raw timing supported:      18
long short-transfer rejections:       3
short morphology chain included:     true
short timing-margin included:        true
short timing-margin content QC:      true
short timing-margin conservative:    false
HPC dimensionality included:         true
HPC geometry type:                   independent_2d_line_profiles
HPC ready for 2D QC:                 true
HPC ready for 3D:                    false
HPC ready for field FWI:             false
field HPC priority:                  none
```

Interpretation: the latest field evidence chain now explicitly includes the
refreshed event-support table, timing-discriminant scorecard, 2D-only/no-HPC
dimensionality decision, and curated short-anchor signed-morphology/timing-margin
figures. The field side remains suitable for scoped 2D QC and manuscript
boundary figures only. Run `109` was superseded by run `110` for a cleaner
support-tier figure, run `130` superseded run `111` with the signed-morphology
chain, and run `133` supersedes run `130` as the current curated publication
bundle after the run `131` signal-contrast guardrail and run `132` sensitivity
caveat. Run `134` verifies current source-figure note coverage. Use runs
`110`, `112`, `131`, `132`, `133`, `134`, and `135` as the current field
endpoints.

## Field Cue/Support Catalog

The current measured-field cue/support traceability catalog is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/113_gssi51600s_field_cue_support_catalog
```

This run separates raw measured reflector cues from derived support anchors so
the manuscript can cite field cue evidence without implying known-truth field
labels.

```text
policy label:                     gssi51600s_field_cue_support_catalog_2d_qc_not_inversion
raw cues:                         19 across 4 profiles
support anchors:                  11
short content-backed anchors:      2
short timing-only cue pairs:       1
long stable pattern anchors:       6
long repeat-limited anchors:       2
timing discriminant rows:          4
event-support tier rows:          11
ready for 2D QC:                  true
ready for absolute time-zero:     false
ready for cover-depth recovery:   false
ready for radius recovery:        false
ready for field FWI / 3D HPC:     false / false
gpu priority:                     none
```

Interpretation: this is the preferred field cue traceability export. Raw
reflector cues remain measured-profile context unless linked to short
content-backed timing anchors or long pattern-only support anchors. The catalog
is useful for supplement tables and QA, but it does not create calibrated field
rebar labels, absolute time-zero, cover-depth, radius, field FWI, 3D, or HPC
readiness.

## Current Manuscript Evidence Pack

The current field source-note coverage, cross-domain evidence audit, and
manuscript table pack are:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/130_gssi51600s_field_publication_claim_bundle_post_signed_morphology_timing_margin
outputs/summary_tables/032_local_2d_field_manuscript_evidence_audit_post_event_support_timing_discriminant_hpc
outputs/summary_tables/087_local_2d_field_manuscript_table_pack
```

Key result:

```text
field source figures with notes:    27 / 27
cross-domain validated figures:     31 / 31
cross-domain claim boundaries:      32
table-pack claim rows:              32
table-pack figure rows:             31
table-pack metric rows:             261
auxiliary policy metrics:           245
target1 ready for GPU probe:        false
detector all-triples top-1 cases:    0 / 12
detector all-triples top-50 cases:   8 / 12
detector component-gate top-50 cases: 10 / 12
detector component-selector leave-one-case cases: 0 / 12
detector geometry-selector leave-one-case cases: 2 / 12
detector geometry-selector ready for FWI: false
detector selector-gap failed cases:  9 / 12
detector selector-gap dominant loss: signed_gap_prior_score
detector counterfactual variants:    44
detector counterfactual best cases:  3 / 12
detector counterfactual gain over base: 0
detector image-objective top50 cases: 0 / 12
detector image-objective top1000 cases: 6 / 12
detector target-failure missing target1 cases: 7 / 9
detector target-failure multi-target cases: 5 / 9
detector target-failure dominant missing target: target1
detector depth/slot prior best all-truth cases: 5 / 12
detector depth/slot prior gain over base: 2
detector depth/slot prior ready for FWI: false
detector slot-component assembly cases: 12 / 12
detector slot-component ready for FWI: false
detector blind-envelope slot cases: 12 / 12
detector blind-envelope leave-one cases: 12 / 12
detector blind-envelope uses branch slots: false
detector blind-envelope ready for FWI: false
detector blind-envelope full-success variants: 117 / 288
detector blind-envelope leave-one-branch cases: 11 / 12
detector blind-envelope min margin:  0.083628
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
detector physics-link review cases: 2 / 12
detector physics-link near-boundary nominal reviews: 2 / 2
detector physics-link close50 nominal review fraction: 2 / 3
detector physics-link review x-ambiguous cases: 1 / 2
detector physics-link per-seed equivalence ready: false
detector physics-link ready for FWI: false
detector refinement-contract seed-table cases: 10 / 12
detector refinement-contract review cases: 2 / 12
detector refinement-contract active blockers: 6
detector refinement-contract radius/material seeds: false / false
detector refinement-contract narrow refinement ready: false
detector refinement-contract FWI ready: false
detector component seed exported cases: 10 / 12
detector component seed exported rows: 30
detector component seed FWI ready: false
detector lateral-slot min half-width: 10.0 mm
detector lateral-slot coverage 5/8/10 mm: 7 / 9 / 10
detector lateral-slot h10 step2 points/case: 1331
detector hypothetical x/z tensor points/case: 1771561
detector lateral-slot z coverage validated: false
detector lateral-slot x/z design ready: false
detector lateral-slot FWI ready: false
detector seed-geometry x/z half-width: 12.0 mm
detector seed-geometry max z error: 12.0 mm
detector seed-geometry z>lateral cases: 7 / 10
detector seed-geometry h12 step2 points/case: 4826809
detector seed-geometry FWI ready: false
detector sampling-boundary claim ready: true
detector sampling-boundary review cases: 2 / 12
detector sampling-boundary reviews below clean: 2 / 2
detector sampling-boundary close50 nominal reviews: 2 / 3
detector sampling-boundary close50 source-mismatch reviews: 0 / 3
detector sampling-boundary per-seed equivalence ready: false
detector sampling-boundary FWI ready: false
detector upper-bound all-truth cases: 12 / 12
detector upper-bound ready for claim: true
detector upper-bound ready for FWI:  false
detector rank-budget all-case triples: 200/case
field cue support anchors:          11
field cue timing long short-transfer rejections: 8 / 8
field spatial transfer long covered: 1 / 8
field spatial transfer ready:       false
field anchor interval short inside: 3 / 3
field anchor interval content inside: 2 / 2
field anchor interval ready for short QC: true
field dimensionality is 3D survey:  false
field dimensionality short QC ready: true
field dimensionality long transfer: false
field time-zero ladder short QC ready: true
field time-zero ladder content-only QC ready: true
field time-zero ladder leave-one-content ready: false
field time-zero ladder content half-range: 0.009823 ns
field time-zero ladder rows: 8
field time-zero ladder absolute t0 ready: false
field time-zero ladder field FWI ready: false
field short-anchor content-only supported: true
field short-anchor leave-one supported cases: 1 / 3
field short-anchor leave-one degraded cases: 2 / 3
field short-anchor content half-range: 0.009823 ns
field short-anchor spatial residual range: 29.997 mm
field short-anchor spatial residual half-range: 14.9985 mm
field short-anchor spatial single translation: false
field short-anchor spatial calibration ready: false
field short-anchor spatial field FWI ready: false
field inversion-readiness supported gates: 2 / 8
field inversion-readiness blocked gates: 6 / 8
field inversion-readiness depth-scale QC: true
field inversion-readiness cover depth ready: false
field inversion-readiness field FWI ready: false
field inversion-readiness 3D/HPC ready: false
field short-anchor radius weak sides: 4 / 4
field short-anchor radius mismatch pairs: 2 / 2
field short-anchor common-radius near-ties: 2 / 2
field short-anchor radius seed ready: false
field short-anchor radius FWI ready: false
field short-anchor signed morphology pairs: 2 / 2
field short-anchor min signed corr: 0.939469
field short-anchor signed morphology FWI ready: false
field signed-morphology supported threshold combos: 36 / 320
field signed-morphology moderate threshold ready: true
field signed-morphology strict claim ready: false
field signed-morphology sensitivity FWI ready: false
field signed-morphology timing content-only ready: true
field signed-morphology conservative timing ready: false
field signed-morphology min default timing slack: 0.030354 ns
field signed-morphology conservative half-width: 0.058939 ns
field signed-morphology timing-margin FWI ready: false
field cue ready for FWI / 3D HPC:   false / false
gpu priority:                       none
```

Interpretation: run `087` is the current combined table pack. It supersedes run
`080` by adding the coordinate-only detector seed export (`081`), detector
corrected lateral-slot neighborhood budget (`084`), matched x/z seed-geometry
audit (`086`), short-anchor signed-morphology audit
(`126`), and signed-morphology threshold sensitivity (`127`) as paper-facing
guardrails. The detector side now has a 10 mm lateral x-slot sizing result,
plus a corrected 12 mm matched x/z seed-neighborhood sizing result, but
radius/material seeding and refinement/FWI launch remain blocked; the field
side now has signed morphology plus finite threshold-margin evidence, but no
amplitude calibration, radius/geometry recovery, field FWI, 3D/HPC, or heavy
field work.
Run `080` had superseded run
`078` by adding the detector/sampling-boundary integration (`079`) and
short-anchor radius-degeneracy audit (`125`) as paper-facing guardrails:
detector review cases are tied to the close50 sub-30 sampling caveat, while
field waveform morphology remains QC-only because radius choices are weak and
near-tied. Run `078` had superseded run
`076` by adding the detector refinement launch-contract audit (`077`) as a
seed-table guardrail: 10/12 stable x/z component rows are exportable for later
design work, but six active blockers keep detector-seeded refinement/FWI
closed. Run `076` had superseded run
`075` by adding the field inversion/HPC readiness synthesis (`123`) to the
cross-domain metrics. Run `075` had superseded run
`073` by adding the detector/physics ambiguity-link audit (`074`) after the
blind-envelope reliability gate (`069`), reliability-threshold sensitivity
(`071`), and close50 29.5 mm coordinate-confidence evidence (`1303`). Run
`073` had superseded run
`072` by adding the short-anchor spatial-consistency audit (`122`) after the
post-leave-one time-zero evidence ladder (`121`) and short-anchor leave-one
audit (`120`). Run `072` had already added the reliability-threshold sensitivity (`071`) after the
truth-free blind-envelope reliability gate (`069`). It keeps the
post-leave-one field time-zero ladder (`121`) and the field short-anchor
leave-one audit (`120`). It also includes the blind-envelope
policy-stability audit (`063`) after the
blind-envelope robustness audit (`061`) and the
blind component-envelope assembly probe (`059`), which itself was added to the
detector slot-component assembly probe (`057`), detector depth/slot prior probe (`055`),
target-failure taxonomy (`053`), field
time-zero evidence ladder (`121`),
detector image-objective rank diagnostic (`050`), detector selector
counterfactual sensitivity (`048`), refreshed field dimensionality decision
card (`118`),
detector selector-gap decomposition (`045`), field anchor-interval
reconciliation (`117`), field spatial-transfer audit (`116`), geometry-family
selector audit (`041`), detector upper-bound policy (`039`), component selector
audit (`037`), rank-budget/component-gate results (`034-035`), and field
timing-envelope integration (`115`). The current pack
uses the latest field bundle/policy (`111-112`), latest field source notes
(`114`), the fresh cross-domain audit (`032`), and CPU-only policy summaries
from runs `028-030`, `034-035`, `037`, `039`, `041`, `045`, `048`, `050`,
`053`, `055`, `057`, `069`, `071`, `074`, `077`, `079`, `113`, `115`, `116`, `117`, `118`, `120`, `121`, `122`, `123`, and `125`. It is a
manuscript-planning package, not a new physics experiment or a GPU launch
trigger.

## Detector Physics Ambiguity Link

The detector/physics ambiguity-link audit is:

```text
outputs/summary_tables/074_local_2d_detector_physics_ambiguity_link
```

Key result:

```text
policy label:                         local_2d_detector_physics_ambiguity_link_cpu_no_fwi
detector review cases:                2 / 12
review near-boundary nominal cases:   2 / 2
close50 29.5 nominal review fraction: 2 / 3
close50 29.5 source-mismatch reviews: 0 / 3
first clean close50 threshold:        30.0 mm
linear 29.5 offset below clean:       0.5 mm
review cases with synthetic x ambiguity: 1 / 2
review cases with synthetic strict-clean rows: 1 / 2
branch-localization claim ready:      true
per-seed physics-equivalence ready:   false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Interpretation: the detector reliability review cases are not scattered
randomly across the detector corpus; they are localized to the close50 linear
29.5 mm nominal family, which sits just below the paper-safe 30 mm clean
threshold. The claim must stay narrower than "coordinate ambiguity explains
every detector review," because only one of the two review cases is
x-ambiguous in the saved coordinate-confidence rows. This is useful
branch/variant ambiguity evidence for the manuscript, not a global retuning
fix or detector-seeded FWI trigger.

## Detector Refinement Launch-Contract Audit

The detector refinement launch-contract audit is:

```text
outputs/summary_tables/077_local_2d_detector_refinement_launch_contract_audit
```

Key result:

```text
policy label:                         local_2d_detector_refinement_launch_contract_audit_cpu_no_fwi
stable detector seed-table cases:     10 / 12
review cases:                          2 / 12
max component seed error:             10.0 mm
radius seed available:                false
material seed available:              false
active launch blockers:                6
ready for component seed table:       true
ready for narrow refinement contract: false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Interpretation: this audit turns the blind-envelope detector result into a
more precise handoff decision. The stable cases can be written down as a saved
x/z component seed table, but that is not enough for a narrow refinement or
FWI launch. The blockers are radius/material seeding, independent deployable
top-1 validation, branch-independent transfer, the two review cases, and the
incomplete per-seed physics-equivalence explanation.

## Detector Rank-Budget Diagnostic

The detector rank-budget diagnostic is:

```text
outputs/summary_tables/034_local_2d_detector_rank_budget_diagnostic_post_alltriples_gate
```

Key result:

```text
all-truth combo available cases:      12 / 12
sparse all-truth cases:                6 / 12
best top20 all-truth cases:            6 / 12
best top50 all-truth cases:            8 / 12
best top100 all-truth cases:          10 / 12
best top200 all-truth cases:          12 / 12
minimal all-case budget:             200 triples/case
max top1 all-truth cases:              0 / 12
max top1 target0-hit cases:            3 / 12
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the detector handoff is not failing because the correct triples
are absent; all cases contain an all-truth triple in the branch-specific
top-20 candidate space. The failure is ranking and sparse geometry support,
especially in close50, where all-truth triples are rare. A rank-gated
upper-bound study is now a defensible CPU-side analysis direction, but it is
not a detector-seeded FWI launch trigger.

## Component Waveform-Gate Pilot

The component-wise waveform gate is:

```text
outputs/summary_tables/035_local_2d_detector_component_waveform_gate_post_rank_budget
```

Key result:

```text
component candidates scored:         230
objectives tested:                     7
best top1 all-truth cases:             0 / 12
best top10 all-truth cases:            3 / 12
best top50 all-truth cases:           10 / 12
best top100 all-truth cases:          11 / 12
best top200 all-truth cases:          12 / 12
top10 improvement over run 030:        +1 case
top50 improvement over run 030:        +2 cases
minimal all-case budget:             200 triples/case
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: component-wise hyperbola support is a real improvement over
the earlier simple all-triples objectives, but it still fails the deployable
top-1 test. The detector handoff remains CPU-side: useful for a rank-gated
upper-bound or stronger waveform-objective development, not for launching
detector-seeded FWI.

## Detector Component Selector Audit

The truth-free component selector audit is:

```text
outputs/summary_tables/037_local_2d_detector_component_selector_audit_post_component_gate
```

Key result:

```text
selector candidates:                  975
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

Interpretation: the improved component gate does not become a deployable
detector initializer after adding truth-free selector features. The selector
audit strengthens the rank-gated/upper-bound framing and argues against a
detector-seeded GPU/FWI queue under the current saved cases.

## Detector Geometry-Family Selector Audit

The branch-family geometry-prior selector audit is:

```text
outputs/summary_tables/041_local_2d_detector_geometry_family_selector_post_upper_bound_policy
```

Key result:

```text
selector candidates:                  2160
best in-sample all-truth cases:          3 / 12
leave-one-case all-truth cases:          2 / 12
leave-one-seed all-truth cases:          1 / 12
leave-one-branch all-truth cases:        2 / 12
best in-sample target0/1/2 hits:         7 / 5 / 9
leave-one-case improvement over component selector: +2 cases
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: adding branch-family span and signed-gap priors fixes part of
the previous selector pathology, especially the close14 gap-balance penalty,
but it still does not produce a deployable detector initializer. This is useful
negative evidence for the paper: modest, explainable selector improvement does
not close the gap to FWI-ready top-1 recovery.

## Detector Selector-Gap Decomposition

The detector selector-gap decomposition is:

```text
outputs/summary_tables/045_local_2d_detector_selector_gap_decomposition
```

Key result:

```text
selector:                            cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1
selected all-truth cases:              3 / 12
failed selector cases:                 9 / 12
best truth available cases:           12 / 12
median required selector gain:         0.18098
max required selector gain:            0.55054
dominant loss feature:                 signed_gap_prior_score
dominant loss feature cases:           7 / 9 failed
selected-truth minimum wrong margin:   0.00667
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the rank-gated candidate space contains an all-truth triple in
every saved case, but the truth-free selector still chooses the wrong triple in
nine cases. The dominant deficit is not the raw component waveform score; it is
the signed-gap prior itself, which overfits the branch-family geometry enough
to pull several cases toward nearby wrong branches. This sharpens the detector
claim boundary: the detector supports a rank-gated upper-bound and failure-mode
analysis, not an automatic detector-seeded FWI queue.

## Detector Selector Counterfactual Sensitivity

The detector selector counterfactual sensitivity is:

```text
outputs/summary_tables/048_local_2d_detector_selector_counterfactual_sensitivity
```

Key result:

```text
source selector:                    cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1
counterfactual variants:              44
counterfactual families:               8
base all-truth cases:                  3 / 12
best counterfactual:                  signed_gap_sweep_w2
best all-truth cases:                  3 / 12
best improvement over base:            0
signed-gap-zero all-truth cases:       1 / 12
best median required selector gain:    0.15420
best dominant loss feature:            signed_gap_prior_score
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the `045` selector failure is not fixed by simple scalar
reweighting. Removing the signed-gap prior drops top-1 all-truth recovery to
1/12, while the best signed-gap reweighting still reaches only 3/12. This
supports the current decision boundary: a stronger downstream waveform
objective would be needed before detector-seeded FWI is a justified local run.

## Detector Image-Objective Rank Diagnostic

The detector image-objective rank diagnostic is:

```text
outputs/summary_tables/050_local_2d_detector_image_objective_rank_diagnostic
```

Key result:

```text
objective variants:                  3
scored rows:                         100656
best objective:                      row_background_sigma100
best top1 all-truth cases:             0 / 12
best top10 all-truth cases:            0 / 12
best top50 all-truth cases:            0 / 12
best top200 all-truth cases:           1 / 12
best top1000 all-truth cases:          6 / 12
best median first all-truth rank:    639
best max first all-truth rank:       1980
ready for detector-seeded FWI:       false
gpu priority:                        none
```

Interpretation: the existing saved-B-scan image objective is not a practical
rank-gated detector handoff. Even the best variant fails to put any all-truth
case inside top-50 and reaches only half the cases by top-1000. This closes the
current image-objective route unless a materially different waveform objective
is designed.

## Detector Target-Failure Taxonomy

The detector target-failure taxonomy is:

```text
outputs/summary_tables/053_local_2d_detector_target_failure_taxonomy
```

Key result:

```text
policy label:                         local_2d_detector_target_failure_taxonomy_cpu_no_fwi
cases:                                12
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

Interpretation: the selector failure is not just a scalar scoring-margin
problem. In the failed cases, the selected wrong triple most often drops
target1, and more than half of failures drop multiple targets. This points the
next detector-side work toward target-conditioned coverage or waveform
evidence, not another one-dimensional signed-gap reweighting or a
detector-seeded FWI launch.

## Detector Depth/Slot Prior Probe

The detector depth/slot prior probe is:

```text
outputs/summary_tables/055_local_2d_detector_depth_slot_prior_probe
```

Key result:

```text
policy label:                         local_2d_detector_depth_slot_prior_probe_cpu_no_fwi
selector:                             cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1
saved candidate rows:                 12180
prior variants:                       72
cases:                                12
base all-truth cases:                  3 / 12
best all-truth cases:                  5 / 12
gain over base:                        2 cases
best mean truth hits:                  2.4167
best depth weight:                    12.0
best slot weight:                      1.0
remaining failed cases:                7 / 12
remaining target1 misses:              4
remaining target2 misses:              3
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the target-failure clue leads to a concrete feature probe:
a broad depth prior plus weak slot prior improves top-1 all-truth selection
from 3/12 to 5/12. That is a real improvement, but still far below a
detector-seeded FWI contract. The useful next design direction is a stronger
target-conditioned waveform/coverage model; the current depth/slot heuristic
is only feature-design evidence.

## Detector Slot-Component Assembly Probe

The branch-slot component assembly probe is:

```text
outputs/summary_tables/057_local_2d_detector_slot_component_assembly_probe
```

Key result:

```text
policy label:                         local_2d_detector_slot_component_assembly_probe_cpu_no_fwi
saved candidate rows:                 12180
slot-assembly variants:               120
cases:                                12
current triple selector all-truth:      3 / 12
depth/slot prior best all-truth:        5 / 12
branch-slot component assembly:        12 / 12
best mean target-slot hits:             3.0
best failed cases:                      0 / 12
minimum component candidates per case: 16
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the saved detector component evidence is sufficient to cover
all three expected target slots in every saved close14/close50 case when the
known synthetic branch slots are used during assembly. This is a strong
upper-bound/contract result, not a deployable selector: it proves the remaining
detector handoff problem is target assignment under blind or weakly supervised
conditions, not lack of component evidence.

## Detector Blind Component-Envelope Assembly Probe

The blind component-envelope assembly probe is:

```text
outputs/summary_tables/059_local_2d_detector_blind_component_envelope_assembly
```

Key result:

```text
policy label:                         local_2d_detector_blind_component_envelope_assembly_cpu_no_fwi
saved candidate rows:                 12180
blind-envelope variants:              288
cases:                                12
current triple selector all-truth:      3 / 12
depth/slot prior best all-truth:        5 / 12
known-slot component upper bound:      12 / 12
blind envelope best slot cases:        12 / 12
leave-one-case slot cases:             12 / 12
uses branch slots for selection:       false
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: run `059` closes the saved target-slot assignment gap without
using close14/close50 slot coordinates during inference. It infers component
support envelopes from the candidate cloud and uses a span-adaptive
close-pair/regular-spacing prior. This is a meaningful CPU-side detector
handoff result, but it is still a small saved-corpus policy synthesis and only
validates component-slot coverage. It should not trigger detector-seeded FWI.

## Detector Blind-Envelope Robustness Audit

The blind-envelope robustness audit is:

```text
outputs/summary_tables/061_local_2d_detector_blind_envelope_robustness_audit
```

Key result:

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

Interpretation: run `061` makes the `059` result more publishable by adding a
negative boundary, not just a success count. The assignment rule is stable
across held-out seeds and nominal/source-mismatch conditions, but it is not
fully branch-family independent: training only on close14 and evaluating
close50 leaves one failed case. This supports a careful detector-handoff claim
and argues against using `059` alone as an FWI launch trigger.

## Detector Blind-Envelope Policy Stability

The blind-envelope policy-stability audit is:

```text
outputs/summary_tables/063_local_2d_detector_blind_envelope_policy_stability
```

Key result:

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

Interpretation: run `063` shows that the blind-envelope result is stable for
most cases across the whole saved policy grid, not just the selected best
variant. The instability is concentrated in two close50 nominal cases. This
supports a specific close50 policy-stability boundary and keeps the result in
the CPU-side manuscript-evidence lane.

## Detector Blind-Envelope Tuning Sensitivity

The blind-envelope tuning-sensitivity decomposition is:

```text
outputs/summary_tables/066_local_2d_detector_blind_envelope_tuning_sensitivity
```

Key result:

```text
policy label:                         local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi
tuning-sensitive cases:                2
maximum knob effect:                   1.0
top-effect case:                       target2_close50_linear29p5|seed34|nominal
top-effect knob:                       structural_weight
top-effect best/worst values:          0.0 / 0.8
structural best values:                seed13 nominal=0.8; seed34 nominal=0.0
support best values:                   seed13 nominal=0.0; seed34 nominal=0.12
structural direction conflict:         true
support direction conflict:            true
span-threshold max effect:             0.0
ready for global tuning fix:           false
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: run `066` shows that the close50 nominal fragility is not a
single-knob global tuning issue. The two sensitive seeds prefer conflicting
structural/support-weight directions. That strengthens the close50 ambiguity
boundary and argues against detector-seeded FWI from this policy.

## Detector Blind-Envelope Reliability Gate

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
tuning-sensitive cases detected:       2 / 2
tuning-sensitive cases missed:         0
stable min success fraction:           1.0
review max x-slot range:               21.0 mm
ready for reliability claim:           true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: run `069` makes the detector boundary deployable as a
truth-free reliability label. The 5 mm x-slot drift gate accepts all stable
saved cases and flags exactly the two close50 nominal tuning-sensitive cases.
This supports confidence/ambiguity wording in the detector baseline section,
not a detector-seeded FWI launch.

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

Interpretation: run `071` shows the 5 mm reliability gate is not a single-point
artifact. It lies at the lower edge of a clean threshold interval; tighter
thresholds over-review stable cases, while thresholds at 20 mm and above miss
known close50 nominal tuning-sensitive cases.

## Detector Upper-Bound Policy

The detector upper-bound policy synthesis is:

```text
outputs/summary_tables/039_local_2d_detector_upper_bound_policy_post_selector_audit
```

Key result:

```text
best rank-gated upper-bound strategy: component_gate_minimal_all_case_upper_bound
best upper-bound objective:            component_balanced
minimal all-case rank-gated budget:   200 triples/case
upper-bound all-truth cases:           12 / 12
component-gate top50 cases:            10 / 12
selector leave-one-case top1 cases:     0 / 12
ready for rank-gated upper-bound claim: true
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the detector baseline has a usable paper role as a rank-gated
upper-bound: the correct detector triple is recoverable within a 200-triple
component-balanced budget for all 12 saved cases. It is not a launch-ready FWI
initializer because validated top-1 selector recovery is zero.

## Field Cue Timing Envelope

The field cue timing-envelope integration is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog
```

Key result:

```text
support anchor rows:                 11
timing reference rows:                2
short anchors inside envelope:        3 / 3
short content anchors inside:         2 / 2
long pattern anchors rejecting short transfer: 8 / 8
short content offset:                 0.127701 ns
short content half-width:             0.058939 ns
early common-mode delta:              2.167 half-widths
long pattern delta:                   1.149 half-widths
ready for short relative timing QC:   true
ready for long short-transfer:        false
ready for absolute time-zero:         false
ready for field FWI / 3D HPC:         false / false
gpu priority:                         none
```

Interpretation: the current measured-field timing picture is internally
consistent and scoped. The short 014/016 anchors are inside the conservative
relative timing envelope, while long 015/013 pattern anchors sit outside that
envelope and therefore reject transfer of the short-pair correction. This is a
field supplement/QC result, not an absolute time-zero, cover-depth, radius,
field FWI, 3D, or HPC claim.

## Field Spatial Transfer Audit

The field spatial-transfer audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/116_gssi51600s_field_spatial_transfer_audit_post_timing_envelope
```

Key result:

```text
spatial match threshold:             100 mm
short content anchors:                 2
short anchors near long pattern:        1 / 2
long pattern anchors:                   8
long anchors near short content:        1 / 8
median short-to-long distance:       106.656 mm
median long-to-short distance:       701.5965 mm
max long-to-short distance:          1403.193 mm
ready for short-to-long timing transfer: false
ready for field FWI / 3D HPC:        false / false
gpu priority:                         none
```

Interpretation: the short content-backed anchors do not provide dense spatial
coverage for the long pattern anchors. Combined with the timing-envelope
rejection, this blocks transferring the short-pair timing correction onto the
long profile. The measured field data remain 2D QC and supplement evidence,
not field FWI, calibrated cover-depth/radius recovery, 3D, or HPC input.

## Field Anchor-Interval Reconciliation

The short-anchor interval reconciliation is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer
```

Key result:

```text
short timing anchors inside supported intervals:     3 / 3
content-backed short anchors inside intervals:       2 / 2
timing-only short anchor inside interval:            1 / 1
minimum margin to supported interval edge:          13.332 mm
median margin to supported interval edge:           19.998 mm
supported interval policy:                           supported_interval_visual_qc_ready
ready for short relative timing QC:                  true
ready for absolute time-zero:                        false
ready for field FWI / 3D HPC:                        false / false
gpu priority:                                        none
```

Interpretation: the current short timing anchors are not only inside the
timing envelope; they also lie inside all-window-supported corrected-stack
intervals from the short 014/016 profile. This strengthens the short-profile
relative timing QC claim, while preserving the same scope boundary: no
absolute time-zero, field inversion, cover-depth/radius recovery, 3D, or HPC
claim.

## Field Dimensionality Refresh

The refreshed field dimensionality decision card is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/118_gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval
```

Key result:

```text
field geometry type:                 independent_2d_line_profiles
is 3D survey:                        false
ready for 2D QC:                     true
ready for short relative timing QC:  true
ready for long short-transfer:       false
ready for 3D HPC:                    false
ready for field FWI:                 false
ready for absolute time-zero:        false
ready for cover-depth/radius:        false / false
profiles:                            4
trace-derived total length:          7.215945 m
scan spacing:                        3.333 mm
short anchors inside supported intervals: 3 / 3
long pattern anchors rejecting transfer:  8
long anchors near short content:          1 / 8
field HPC priority:                  none
```

Interpretation: the measured field files should be treated as four independent
2D line profiles. The short profiles support relative timing and
supported-interval QC, but short-to-long timing transfer is rejected, and the
available DZX metadata do not recover a 3D grid. Do not submit a field-data
3D/HPC/FWI job from this dataset without external survey layout, calibrated
target geometry, and absolute timing/depth controls.

## Field Time-Zero Evidence Ladder

The current consolidated field time-zero evidence ladder is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/121_gssi51600s_field_time_zero_ladder_post_leave_one
```

Key result:

```text
policy label:                         gssi51600s_field_time_zero_evidence_ladder_post_leave_one_short_qc_only
evidence ladder rows:                  8
ready for short relative timing QC:    true
ready for content-only short QC:       true
ready for leave-one content claim:     false
ready for long short-transfer:         false
ready for absolute time-zero:          false
ready for field FWI:                   false
ready for 3D HPC:                      false
short relative offset:                 0.127701 ns
short conservative half-width:         0.058939 ns
content-only half-range:               0.009823 ns
all-short half-range:                  0.034381 ns
leave-one supported cases:             1 / 3
leave-one degraded cases:              2 / 3
short anchors inside envelope:         3
short anchors inside supported intervals: 3
long pattern anchors rejecting transfer: 8
long anchors near short content:       1 / 8
median long-to-short distance:         701.5965 mm
gpu priority:                          none
```

Interpretation: the field timing evidence is now a single claim-boundary
ladder that includes the leave-one/content-only short-anchor audit. The
allowed use is short-profile relative timing QC for the local measured data,
and that short-QC claim survives dropping the timing-only short anchor. It
does not survive leave-one removal of either content-backed anchor, so the
blocked uses remain long-profile timing transfer, absolute time-zero,
calibrated depth/radius recovery, field FWI, and 3D/HPC.

## Field Short-Anchor Spatial Consistency

The field short-anchor spatial-consistency audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/122_gssi51600s_field_short_anchor_spatial_consistency_audit
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_spatial_consistency_timing_qc_only
short anchors:                        3
content-backed anchors:               2
content anchors inside intervals:     2
content residual range:               29.997 mm
content residual half-range:          14.9985 mm
content min supported-interval margin: 13.332 mm
content residual sign consistent:     false
single spatial translation supported: false
ready for short relative timing QC:   true
ready for profile spatial calibration: false
ready for absolute time-zero:         false
ready for field FWI / 3D HPC:         false / false
gpu priority:                         none
```

Interpretation: the two content-backed short anchors continue to support
short-profile relative timing QC, but their signed spatial residuals do not
support one calibrated profile-to-profile translation. This blocks profile
spatial calibration, cover-depth/radius recovery, field FWI, and 3D/HPC use
from the measured field dataset without external survey/target controls.

## Field Inversion/HPC Readiness Synthesis

The field inversion/HPC readiness synthesis is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/123_gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency
```

Key result:

```text
policy label:                       gssi51600s_field_inversion_readiness_synthesis_short_qc_only
readiness gates:                    8
supported gates:                    2
blocked gates:                      6
supported gates:                    short_relative_timing_qc;apparent_depth_scale_qc
blocked gates:                      long_profile_transfer;profile_spatial_calibration;cover_depth_recovery;radius_recovery;field_fwi;field_3d_hpc
ready for short relative timing QC: true
ready for apparent-depth scale QC:  true
ready for long-profile transfer:    false
ready for profile spatial calibration: false
ready for cover-depth recovery:     false
ready for radius recovery:          false
ready for field FWI / 3D HPC:       false / false
apparent-depth max span:            149.916 mm
apparent-depth sensitivity factor:  2.18x
spatial residual range:             29.997 mm
field geometry type:                independent_2d_line_profiles
gpu priority:                       none
```

Interpretation: this is the current field-side decision card for heavy work.
The local GSSI archive remains useful for short-profile timing/visual QC and
apparent-depth scale checks, but not for calibrated cover-depth/radius
recovery, field FWI, neural inversion labels, or 3D/HPC submission without
external survey layout, absolute timing/depth controls, calibrated dielectric,
and known target geometry.

## Field Short-Anchor Waveform-Coherence Audit

The field short-anchor waveform-coherence audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/124_gssi51600s_field_short_anchor_waveform_coherence_audit
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_waveform_coherence_qc_only
content-backed pairs:                 2
waveform-coherent pairs:              2 / 2
min corrected field-trace correlation: 0.939469
min event-local field-trace correlation: 0.988138
min correlation improvement:          0.585637
max corrected timing residual:        0.019646 ns
min panel absolute correlation:       0.819494
radius-match pairs:                   0 / 2
single spatial translation supported: false
leave-one content-anchor claim ready: false
ready for waveform morphology QC:     true
ready for geometry/radius recovery:   false / false
ready for field FWI / 3D HPC:         false / false
gpu priority:                         none
```

Interpretation: run `124` adds positive measured-field morphology evidence:
the two content-backed short anchors are coherent after relative timing
correction. The result is still a QC-only result because radius choices differ,
one profile-to-profile spatial translation is unsupported, and the
content-anchor evidence is not leave-one-content redundant.

## Field Short-Anchor Leave-One Audit

The short-anchor leave-one audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/120_gssi51600s_field_short_anchor_leave_one_audit
```

Key result:

```text
policy label:                       gssi51600s_field_short_anchor_leave_one_content_redundancy_qc_only
short anchors:                      3
content-backed short anchors:       2
timing-only short anchors:          1
content-only supported:             true
content-only half-range:            0.009823 ns
all-short half-range:               0.034381 ns
leave-one supported cases:          1 / 3
leave-one degraded cases:           2 / 3
ready for short relative timing QC: true
ready for absolute time-zero:       false
ready for field FWI:                false
ready for 3D HPC:                   false
gpu priority:                       none
```

Interpretation: run `120` sharpens the field timing claim. The timing-only
short anchor can be removed, and the two content-backed short anchors still
support a narrower relative timing interval. The result is not
leave-one-content redundant, however: removing either content-backed anchor
leaves only one content-backed anchor. This supports short-profile relative
timing QC, not absolute time-zero, depth/radius recovery, field FWI, 3D, or
HPC.

## Close50 Sampling Boundary

The close50 sampling-boundary synthesis is:

```text
outputs/experiments/1338_close50_sampling_boundary_synthesis
```

Key result:

```text
policy label:                         close50_sampling_boundary_synthesis_cpu_no_gpu
nearest first clean replicated Tx/Rx:  30.0 mm
nearest nonclean offsets:              25,27.5,28.75 mm
nearest clean offsets:                 30,35,40 mm
linear exact-strong-not-clean offsets: 29.5,29.75 mm
linear 29.5 ambiguous seeds:           1 / 3
legacy run270 truth fraction:          1.0
legacy run280 Tx/Rx40 truth fraction:  1.0
paper sampling boundary ready:         true
sub-30 clean threshold claim ready:    false
GPU probe ready:                       false
gpu priority:                          none
```

Interpretation: run `1338` closes the 270/280 close50 concern without a new
GPU run. The old evidence is useful, but the clean publication boundary should
stay at nearest-sampled Tx/Rx 30 mm. The sub-30 nearest 28.75 mm and linear
29.5 mm/29.75 mm evidence belongs in the caveat text: truth can be selected
below 30 mm, but the replicated margin is not clean enough to claim a sub-30
clean threshold.

## Field Short-Anchor Radius Degeneracy

The short-anchor radius-degeneracy audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/125_gssi51600s_field_short_anchor_radius_degeneracy_audit
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_radius_degeneracy_audit_qc_only
content-backed pairs:                 2
selected best-radius sides:           4 / 4
weak radius sides:                    4 / 4
min best-second radius corr gap:      0.006066
max best-second radius corr gap:      0.018674
selected radius mismatch pairs:       2 / 2
common-radius near-tie pairs:         2 / 2
waveform morphology QC ready:         true
radius seed ready:                    false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `125` explains why the positive waveform-coherence result
from run `124` still cannot be promoted into radius seeding or field inversion.
The selected side-wise radii are locally best, but the correlation gaps are too
small, the repeat-profile radius choices disagree, and forced common-radius
alternatives are near-tied at the pair level.

## Field Short-Anchor Signed Morphology

The short-anchor signed-morphology audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/126_gssi51600s_field_short_anchor_signed_morphology_audit
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_qc_only
content-backed pairs:                 2
signed morphology supported pairs:    2 / 2
corrected same-polarity pairs:        2 / 2
min corrected signed correlation:     0.939469
mean corrected signed correlation:    0.963803
min event-local abs correlation:      0.988138
min abs correlation improvement:      0.585637
max corrected timing residual:        0.019646 ns
weak radius sides:                    4
selected radius mismatch pairs:       2
common-radius near-tie pairs:         2
signed morphology QC ready:           true
amplitude calibration ready:          false
radius seed ready:                    false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `126` strengthens the measured-field supplement claim by
showing that the two content-backed short anchors remain same-polarity after
relative timing correction. This supports signed waveform-morphology QC, not
just absolute-correlation resemblance. The traces are robust-normalized and
the radius/spatial/depth controls remain blocked, so this is not amplitude
calibration, radius/geometry seeding, cover-depth recovery, field FWI, 3D/HPC,
or heavy field-work evidence.

## Field Signed-Morphology Threshold Sensitivity

The short-anchor signed-morphology threshold sensitivity audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/127_gssi51600s_field_short_anchor_signed_morphology_sensitivity
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_threshold_sensitivity_qc_only
content-backed pairs:                 2
threshold combinations:               320
all-pair supported combinations:      36
all-pair supported fraction:          0.1125
default thresholds supported:         true
moderate tightening supported:        true
strict correlation supported:         false
strict all-threshold claim supported: false
corrected signed-correlation limit:   0.939469
event-local abs-correlation limit:    0.988138
correlation-improvement limit:        0.585637
timing-cap limit:                     0.019646 ns
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `127` shows that the positive signed-morphology result is
not a single fixed-threshold artifact: it survives the default gate and a
moderate tightening envelope. The margin is finite, so strict morphology,
amplitude calibration, radius/geometry seeding, cover-depth recovery, field
FWI, 3D/HPC, and heavy field work remain blocked.

## Field Publication-Bundle Freshness

The field publication-bundle freshness audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/128_gssi51600s_field_publication_bundle_freshness_audit
```

Key result:

```text
policy label:                         gssi51600s_field_publication_bundle_freshness_audit_curated_refresh_needed_not_automatic
current bundle figures:               22
candidate latest morphology figures:   4
candidates already in bundle:          0
candidate missing figures:             0
candidate QC-ready figures:            4
primary refresh candidates:            2
guardrail refresh candidates:          2
candidate field-FWI-ready figures:     0
curated refresh decision ready:        true
automatic bundle refresh ready:        false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: run `128` says not to rewrite the field publication bundle
automatically. If the field supplement is deliberately refreshed, the signed
morphology and threshold-sensitivity figures from runs `126-127` are the first
promotion candidates; waveform-coherence and radius-degeneracy figures from
runs `124-125` are guardrail candidates. This does not change the no-field-FWI,
no-3D/HPC, no-radius/geometry/cover-depth boundary.

## Field Short-Anchor Signed-Morphology Timing Margin

The short-anchor signed-morphology timing-margin audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/129_gssi51600s_field_short_anchor_signed_morphology_timing_margin
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_timing_margin_qc_only
content pairs:                         2
signed morphology supported pairs:      2
default timing cap:                    0.05 ns
moderate timing cap:                   0.02 ns
max corrected timing residual:         0.01964636542239684 ns
min default timing slack:              0.030353634577603164 ns
min moderate timing slack:             0.0003536345776031617 ns
content-only time-zero half-range:     0.00982318271119842 ns
conservative short half-width:         0.058939096267190516 ns
default slack covers content pairs:    2 / 2
default slack covers conservative:      0 / 2
moderate slack covers content pairs:    1 / 2
content-only morphology timing QC:     true
conservative timing morphology claim:  false
absolute time-zero ready:              false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: run `129` strengthens the field supplement boundary rather
than opening inversion. The signed morphology result is robust to the
content-only short-profile timing half-range, but not to the conservative
all-short timing half-width. Keep the claim at content-only timing-margin
morphology QC; do not promote it to absolute time-zero, conservative timing,
field FWI, 3D/HPC, or heavy field work.

## Field Publication Claim Bundle Post Signed-Morphology Timing Margin

The curated post-morphology field publication bundle is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/130_gssi51600s_field_publication_claim_bundle_post_signed_morphology_timing_margin
```

Key result:

```text
policy label:                         field_publication_claim_bundle_2d_qc_short_timing_margin_short_morphology_hpc_dimensionality_timing_discriminant_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          27
claim boundaries:                     24
event-support source:                 run 110
event-support rows:                   11
short signed morphology included:     true
short timing-margin included:         true
short timing-margin content QC:       true
short timing-margin conservative:     false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `130` is the deliberate curated refresh that run `128`
deferred to a decision. It packages the latest short-anchor waveform-coherence,
radius-degeneracy, signed-morphology, threshold-sensitivity, and timing-margin
figures into the publication claim bundle while preserving the no-field-FWI,
no-3D/HPC, no-absolute-time-zero, no-conservative-timing, no-radius/geometry,
and no-cover-depth boundary.

## Field Short-Anchor Signal-Contrast Audit

The post-bundle signal-contrast guardrail is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/131_gssi51600s_field_short_anchor_signal_contrast_audit
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_qc_only
content pairs:                         2
side windows:                          4
signal-contrast supported windows:     4 / 4
min event/pre-event RMS ratio:         4.129473194969804
min event/pre-event RMS dB:           12.317893027750134
min peak/pre-event-p95 ratio:         12.398728731716746
signal contrast QC ready:              true
signed morphology QC ready:            true
timing-margin QC ready:                true
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: run `131` adds a direct local signal-contrast guardrail behind
the field morphology chain. The content-backed short-anchor windows are not
low-contrast artifacts, but the calculation uses background-removed DZT
amplitudes and local pre-event baselines. It supports field supplement
morphology QC only, not absolute amplitude calibration, radius/geometry/depth
recovery, field FWI, 3D/HPC, or heavy field work.

## Field Short-Anchor Signal-Contrast Sensitivity

The post-contrast sensitivity audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/132_gssi51600s_field_short_anchor_signal_contrast_sensitivity
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_sensitivity_qc_only
sensitivity combinations:             27
all-supported combinations:           13 / 27
default combination supported:        true
default min event/pre-event RMS:       4.129473194969804
default min peak/pre-event-p95:       12.398728731716746
worst RMS combination:                a10mm_tight_near
worst supported side windows:          2 / 4
worst min event/pre-event RMS:         1.0542762100138983
window-invariant contrast ready:       false
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: run `132` keeps the run `131` result honest. The default
window supports field morphology QC, but tight/near-window variants fail, so
the contrast result is not a strict window-invariant claim and is not amplitude
calibration or field-inversion evidence.

## Field Publication Bundle Post Signal-Contrast Sensitivity

The current curated field publication claim bundle is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/133_gssi51600s_field_publication_claim_bundle_post_signal_contrast_sensitivity
```

Key result:

```text
policy label:                         field_publication_claim_bundle_2d_qc_short_signal_contrast_short_timing_margin_short_morphology_hpc_dimensionality_timing_discriminant_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          29
claim boundaries:                     25
event-support source:                 run 110
short signal contrast included:       true
short signal supported windows:       4 / 4
short signal min RMS ratio:           4.129473194969804
short signal sensitivity combos:      27
all-supported sensitivity combos:     13
window-invariant contrast ready:      false
absolute amplitude calibration ready: false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `133` is the current curated field bundle. It packages the
existing field timing/morphology chain plus the signal-contrast guardrail and
sensitivity caveat. This strengthens the manuscript field supplement path, but
it remains measured-field 2D QC only, not amplitude calibration, strict
window-invariant contrast, absolute time-zero, radius/geometry/cover-depth
recovery, field FWI, 3D/HPC, or synthetic-policy relabeling.

## Field Source-Figure Notes Backfill Post Signal-Contrast Bundle

The current source-note coverage audit is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/134_gssi51600s_field_publication_source_figure_notes_backfill_post_signal_contrast_bundle
```

Key result:

```text
policy label:           field_publication_source_figure_notes_backfill_complete_skip_existing
bundle run:             133_gssi51600s_field_publication_claim_bundle_post_signal_contrast_sensitivity
source figures audited: 29
generated notes:        0
refreshed notes:        0
skipped existing notes: 29
missing figures:        0
notes present after:    29
gpu priority:           none
ready for handoff:      true
```

Interpretation: run `134` confirms the current run `133` field bundle is
source-note complete without rewriting previous notes. It is provenance support
for manuscript handoff, not a new field inversion or 3D/HPC trigger.

## Field Short-Anchor Signal-Contrast Regime Synthesis

The field signal-contrast regime synthesis is:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/135_gssi51600s_field_short_anchor_signal_contrast_regime_synthesis
```

Key result:

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_regime_synthesis_qc_only
sensitivity combos:                   27
all-supported combos:                 13
broad event combos supported:          9 / 9
broad event min RMS ratio:             5.051403727
broad event min peak/p95 ratio:        11.312450857
default event all-supported fraction:  4 / 9
tight event all-supported fraction:    0 / 9
broad event contrast regime ready:     true
strict window-invariant contrast:      false
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: run `135` finds a stronger but still scoped measured-field
claim: broad event-window signal contrast is robust across the tested
aperture/noise settings, while tight/default event windows are not invariant.
This supports field morphology-contrast QC only and keeps absolute amplitude
calibration, field FWI, 3D/HPC, and heavy field work blocked.

## Detector/Sampling Boundary Integration

The detector/sampling-boundary integration audit is:

```text
outputs/summary_tables/079_local_2d_detector_sampling_boundary_integration
```

Key result:

```text
policy label:                         local_2d_detector_sampling_boundary_integration_cpu_no_fwi
detector review cases:                 2
review cases below clean threshold:    2 / 2
review nominal cases:                  2 / 2
below-clean cases:                     6
stable below-clean cases:              4
branch-transfer failures below clean:  1 / 1
close50 nominal review cases:          2 / 3
close50 source-mismatch reviews:       0 / 3
review x-ambiguous cases:              1 / 2
detector boundary claim ready:         true
per-seed physics equivalence ready:    false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Interpretation: run `079` connects the detector handoff limit to the close50
sampling boundary instead of treating it as a generic detector failure. Both
review cases are close50 linear 29.5 mm nominal rows below the 30 mm clean
threshold; source-mismatch rows at the same offset have no reviews. This is a
paper-useful branch-local detector ambiguity-boundary result, not a
detector-seeded FWI trigger.

## Detector Component Seed Export

The coordinate-only detector component seed export is:

```text
outputs/summary_tables/081_local_2d_detector_component_seed_export
```

Key result:

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

Interpretation: run `081` makes the stable detector rows reusable as a
coordinate-only x/z seed table for later design work. It does not close the
launch blockers: radius/material seeding, independent top-1 selection,
branch-independent transfer, review cases, and per-seed physics equivalence
remain unresolved.

## Detector Lateral-Slot Neighborhood Budget

The lateral x-slot-only neighborhood budget is:

```text
outputs/summary_tables/084_local_2d_detector_lateral_slot_neighborhood_budget
```

Key result:

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

Interpretation: run `084` turns the coordinate-only seed export into a concrete
lateral x-slot budget boundary. A 10 mm lateral x-slot half-width covers all 10
stable exported cases in the saved truth evaluation, but the two review cases
remain policy-excluded. Detector z coverage is not validated; the supported
10 mm / 2 mm lateral-x tensor is 1,331 points per case, while a hypothetical
x/z tensor would be 1,771,561 points per case. This supports later design
sizing only, not a narrow refinement, detector-seeded FWI, or GPU launch.

## Detector Seed Geometry Error Audit

The matched x/z seed-geometry audit is:

```text
outputs/summary_tables/086_local_2d_detector_seed_geometry_error_audit
```

Key result:

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

Interpretation: run `086` closes the z-evidence gap left by run `084`.
Stable exported detector seeds need a 12 mm matched x/z half-width, not only
the 10 mm lateral x-slot half-width, because z errors reach 12 mm and exceed
lateral slot error in 7/10 stable cases. This supports future x/z
seed-neighborhood design only. It still blocks narrow refinement, detector FWI,
and any GPU launch because radius/material seeds, review-case closure, and
launch-contract evidence are still missing.

## Detector X/Z Seed-Neighborhood Contract

The branch-specific x/z seed-neighborhood contract is:

```text
outputs/summary_tables/088_local_2d_detector_xz_seed_neighborhood_contract
```

Key result:

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

Interpretation: run `088` converts the run `086` sizing result into a tighter
saved-case design contract: `target2_close14` can stay at 10 mm, while
`target2_close50_linear29p5` needs 12 mm. This reduces the hypothetical 2 mm
x/z coordinate grid by about 38% relative to global h12. It does not include
the two review cases and does not unblock radius/material seeding, narrow
refinement, detector-seeded FWI, GPU work, 3D/HPC, or neural-network work.

## Detector Radius/Material Prior Scope

The post-table-pack controlled-prior audit is:

```text
outputs/summary_tables/089_local_2d_detector_radius_material_prior_scope_audit
```

Key result:

```text
policy label:                         local_2d_detector_radius_material_prior_scope_audit_cpu_no_fwi
source cases:                         12
stable controlled-prior cases:        10
review cases excluded:                 2
radius patterns:                      5,6,8 mm
material prior parameters:             4
detector radius seeds:                 0
detector material seeds:               0
controlled synthetic prior ready:      true
detector-inferred radius/material:     false
field transfer ready:                  false
detector-seeded FWI ready:             false
gpu priority:                         none
```

Interpretation: run `089` closes a wording gap in the detector handoff plan.
The stable saved synthetic cases have a controlled radius/material design
prior from run `017` and `config.py`, but that prior is not a detector-inferred
radius/material estimate. It can support synthetic prior-scoped manuscript
methods, while review-case inclusion, field transfer, narrow refinement,
detector-seeded FWI, and GPU work remain blocked.

## Controlled-Prior Refinement Budget

The post-prior-scope budget audit is:

```text
outputs/summary_tables/090_local_2d_detector_controlled_prior_refinement_budget
```

Key result:

```text
policy label:                         local_2d_detector_controlled_prior_refinement_budget_cpu_no_fwi
stable controlled-prior cases:        10
review cases excluded:                 2
radius pattern:                       5,6,8 mm
fixed-slot fine points:               29936602
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

Interpretation: run `090` converts the radius/material scope boundary into a
budget decision. A fixed-slot controlled-radius ablation remains finite and
paper-safe as a design artifact, but known-radius permutation and independent
radius-choice searches expand the stable fine-grid budget by 6x and 27x. This
does not authorize a refinement, FWI, GPU, field-transfer, or detector-inferred
radius claim.

## Controlled Fixed-Radius Detector-Seed Pilot

The first bounded fixed-radius detector-seed pilot is:

```text
outputs/experiments/1340_local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_source_mismatch_gpu
```

Key result:

```text
branch/case:              target2_close14 seed21 source_mismatch
backend:                  gpu-cpml
fixed radii:              5,6,8 mm
initial x/z:              [190,248,263] / [95,86,81] mm
final x/z:                [190,250,265] / [91,90,85] mm
initial L-inf error:      9 mm
final L-inf error:        5 mm
elapsed:                  364.8 s
gpu utilization observed: about 87%
```

The nominal seed21 attempt in
`outputs/experiments/1339_local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_nominal_gpu`
failed before simulation because the detector seed geometry overlapped under
the exact `5,6,8` mm radii and the non-overlap filter rejected all first-step
candidates.

Interpretation: run `1340` is useful but not a launch success. Exact-radius
local search improves the non-overlapping detector seed and recovers the middle
bar exactly, but one pass leaves the right bar 1 mm laterally high and 5 mm
shallow. The next useful 2D work is a preflight over the ten stable seeds to
separate overlap-blocked, non-overlap-runnable, and repair-required cases
before any further GPU pilots.

## Exact-Radius Seed Non-Overlap Preflight

The exact-radius seed preflight is:

```text
outputs/summary_tables/091_local_2d_detector_exact_radius_seed_nonoverlap_preflight
```

Key result:

```text
stable seed cases:                    10
direct fixed-radius pilot ready:       7
overlap-blocked cases:                 3
repair-within-2mm cases:               3
minimum pair clearance:               -2.0 mm
close14 direct-ready cases:            3 / 6
close50 linear29.5 direct-ready cases: 4 / 4
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Interpretation: run `091` converts the fixed-radius pilot blocker into a
case-level queue boundary. Seven stable seeds are direct-ready for future
one-case-at-a-time pilots, while three close14 seeds need CPU repair/preflight
first. This keeps broad GPU work and detector-seeded FWI blocked.

## Exact-Radius Seed Repair Design

The exact-radius seed repair design is:

```text
outputs/summary_tables/092_local_2d_detector_exact_radius_seed_repair_design
```

Key result:

```text
overlap-blocked cases:                 3
repair found:                          3
all overlap-blocked repairable:        true
maximum component shift:               2.0 mm
minimum clearance after repair:        0.0 mm
repaired pilot subset ready:           true
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Interpretation: run `092` repairs all three overlap-blocked close14 seeds with
a truth-free 2 mm left shift of the middle detector component. This is still a
geometry-only repair contract, so it authorizes at most one repaired-seed
waveform validation pilot before any broader queue.

## Repaired Exact-Radius Seed Waveform Pilot

The repaired-seed waveform pilot is:

```text
outputs/experiments/1341_local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu
```

Key result:

```text
branch/case:              target2_close14 seed21 nominal
backend:                  gpu-cpml
fixed radii:              5,6,8 mm
repaired initial x/z:     [191,252,266] / [86,91,91] mm
final x/z:                [191,252,266] / [90,89,91] mm
initial L-inf error:      4 mm
final L-inf error:        2 mm
accepted candidates:      target0 25/25, target1 15/25, target2 15/25
elapsed:                  321.6 s
gpu utilization observed: 86-87%
```

Interpretation: run `1341` validates that the run `092` repair is waveform
runnable and improves the one-pass coordinate error, but it is not a clean
recovery. The remaining error is lateral: the middle and right bars stay 2 mm
to the right. This keeps broad GPU work and detector-seeded FWI blocked while
making a second-pass/update-order question the next narrow synthetic option.

## Middle-Branch Counterfactual Target2 Unlock

The target2 unlock diagnostic is:

```text
outputs/experiments/1342_local2d_counterfactual_middle_neartie_target2_unlock_close14_seed21_nominal_gpu
```

Key result:

```text
branch/case:              target2_close14 seed21 nominal
backend:                  gpu-cpml
fixed radii:              5,6,8 mm
counterfactual x/z:       [191,250,266] / [90,89,91] mm
final x/z:                [191,250,264] / [90,89,91] mm
initial L-inf error:      2 mm
final L-inf error:        1 mm
accepted candidates:      target2 20/25
best/next target2 misfit: 0.069865725 / 0.072306181
elapsed:                  116.8 s
gpu utilization observed: 87%
```

Interpretation: run `1342` shows that target2 has waveform support at the true
lateral branch once the middle rebar is kept on the near-tie `x=250,z=89`
branch. The run `1341` residual is therefore a greedy branch-lock /
coupled-assignment issue, not simply an absent right-bar signal. The next
algorithmic work should preserve near-tie middle/right branches or test a
small coupled middle-right search rather than repeat a one-path greedy pass.

## Branch-Lock Counterfactual Synthesis

The branch-lock synthesis is:

```text
outputs/summary_tables/093_local_2d_detector_branch_lock_counterfactual_synthesis
```

Key result:

```text
target1 selected branch:               x=252 mm, z=89 mm
target1 near-tie branch:               x=250 mm, z=89 mm
near-tie misfit gap:                   0.006101703
near-tie relative gap:                 0.092164510
near-tie retained by 10% rule:         true
target2 true-x available after greedy: false
target2 true-x unlocked counterfact.:  true
greedy/counterfactual L-inf error:     2 mm / 1 mm
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
```

Interpretation: run `093` turns the `1341`/`1342` pair into a CPU-side
policy result. The appropriate next design is a branch-preserving selector or
small coupled middle-right search sized before launch, not another one-path
greedy pass.

## Decision

Do not launch GPU work simply to keep the GPU busy. Target1 does not currently
justify a Tx/Rx or source-count probe; it needs a new hypothesis before GPU
work. The detector baseline is now two-part: the default detector setting is
weak as a competitive comparator, but tuned saved-B-scan rescoring shows
truth-containing candidate lists across the close14/close50 cases, with a
shared top-40 rank budget. The assignment taxonomy sharpens this into a
research direction: per-case policy-oracle selection reaches 7/12 all-truth
cases, while the best shared blind policy remains at 2/12. A first truth-free
rank/span selector and shallow image-objective gate did not close the gap, and
run `034` shows that all-case coverage requires a 200-triple rank budget rather
than a deployable top-1 gate. Run `035` improves the top-50 rank-gated result
from 8/12 to 10/12 but still leaves top-1 at 0/12, run `037` shows that
generic truth-free selector features do not generalize, run `041` shows that
branch-family geometry priors improve leave-one-case recovery to only 2/12,
and run `045` decomposes the remaining selector failures as mostly signed-gap
prior deficits despite all-truth candidates being available in 12/12 cases.
Run `048` then shows that simple one-dimensional selector reweighting does not
improve beyond the same 3/12 in-sample top-1 all-truth recovery.
Run `050` shows that the existing saved-B-scan image objective is also too deep
for practical rank-gated handoff, with 0/12 top-50 and 6/12 top-1000 all-truth
coverage.
Run `053` shows that the selected wrong detector triples most often drop
target1, with target1 missing in 7/9 failed cases and multi-target failures in
5/9 failed cases.
Run `055` shows that a broad depth/slot prior can improve the selector to 5/12
all-truth cases, but still leaves seven failed cases and does not justify
detector-seeded FWI.
Run `057` shows that branch-slot component assembly covers all target slots in
12/12 cases, which reframes the detector handoff gap as target assignment
rather than component detectability.
Run `059` then shows that a blind component-envelope assembly can recover all
target slots in 12/12 saved cases and 12/12 leave-one-case selections without
using branch slot coordinates at inference. Because it is still a saved-corpus
component-slot policy, not a full inversion or independent detector benchmark,
it remains CPU-side manuscript evidence rather than an FWI launch trigger.
Run `061` stress-tests that result: it remains robust across held-out seed and
source-condition splits, but leave-one-branch transfer drops to 11/12 and one
close50 nominal case has a low truth-versus-wrong score margin. That is the
current detector boundary.
Run `066` then decomposes the two close50 nominal tuning-sensitive cases and
shows conflicting structural/support-weight directions, so a simple global
retuning is not a credible fix.
Run `069` then turns that boundary into a truth-free x-slot drift reliability
gate: 10/12 cases are stable, the two review cases are exactly the close50
nominal tuning-sensitive seeds, and no detector-seeded FWI is justified.
Run `071` verifies that this gate has a clean threshold interval from 5 to
19 mm, so the default 5 mm cutoff is not a brittle single-point artifact.
Run `074` links those two detector review cases back to the close50 29.5 mm
near-threshold physics context: both review cases are near-boundary nominal
rows, but only one is per-seed x-ambiguous in the coordinate-confidence table.
Run `077` keeps narrow refinement and detector-seeded FWI blocked by six
explicit launch-contract blockers, and run `081` exports the 10 stable cases
as a saved coordinate-only x/z component seed table without changing those
blockers.
Run `084` sizes the lateral x-slot part of that seed table: a 10 mm lateral
x-slot half-width covers all stable exported cases, but z coverage is not
validated and unchanged policy blockers keep refinement and detector-seeded FWI
blocked.
Run `086` closes the coordinate sizing gap for the stable exported seeds: a
12 mm matched x/z half-width covers all stable cases, but the h12/step2 x/z
tensor is 4,826,809 points per case and radius/material plus review-case
blockers still keep refinement and detector-seeded FWI blocked.
Run `088` converts that sizing into a branch-specific stable-case contract:
`target2_close14` uses 10 mm and `target2_close50_linear29p5` uses 12 mm,
reducing the 2 mm x/z coordinate-grid budget by about 38% versus global h12
while still excluding the two review cases and keeping refinement/FWI/GPU
blocked.
Run `089` then scopes the remaining radius/material question: the saved
synthetic cases share the controlled 5,6,8 mm radius design prior and fixed
material constants, so those can be used only as controlled synthetic priors,
not as detector-inferred radius/material seeds. This keeps narrow refinement,
field transfer, detector-seeded FWI, and GPU work blocked.
Run `090` sizes that controlled-prior route: exact slot radii keep the stable
fine grid at 29.94 million points, known-radius permutations cost 179.62
million points, and independent known-radius choices cost 808.29 million
points. Run `1340` then shows a single non-overlapping fixed-radius seed can be
improved but not fully recovered in one pass, while the failed run `1339`
shows some stable seeds require non-overlap preflight or repair before launch.
Run `091` performs that preflight: 7/10 stable seeds are direct-ready, and the
three overlap-blocked close14 seeds need at most 2 mm of geometric repair.
Run `092` designs those repairs, and run `1341` validates one repaired seed:
the max error drops from 4 mm to 2 mm, but residual lateral offsets remain.
Run `1342` identifies the mechanism: preserving the near-tie middle branch
lets target2 move to the correct lateral position and drops the max error to
1 mm. The next small-scope synthetic follow-up is therefore a branch-preserving
or coupled middle-right selector. Run `093` records the CPU-side policy
synthesis and keeps that next step scoped before launch, still without a broad
launch contract.
Run `1343` then executes that scoped coupled-search test: three target1
branches are retained, 55 target2 candidates are evaluated, and the
objective-best coupled row is also the oracle-best row with 1 mm final
L-infinity error. This upgrades the 2D path from a counterfactual mechanism to
a directly evaluated branch-preserving selector diagnostic while still keeping
broad GPU queues and detector-seeded FWI blocked.
Run `094` then scans saved coordinate optimizer candidate surfaces and finds
that the effect is uncommon but archive-backed: 13/747 audited candidate
surfaces retain a truth-lateral branch inside the same 0.01 absolute / 10%
relative preservation window while greedy selection chooses a nearby lateral
branch. Target2 is the main hotspot with 9/373 retained-but-not-selected
surfaces. This supports branch preservation as a CPU-side policy direction,
not as a broad GPU queue.
Run `095` triages those 13 rows by full x/z coordinate impact: 7 improve
L-infinity error by selecting the retained truth-lateral branch, 6 are same-error
objective near-ties, and none are worse. Three older close50 target2 rows are
possible narrow coupled-probe candidates, but none are promoted to GPU without
a separate case-specific design and manuscript rationale.
Run `096` sweeps branch-preservation thresholds. The default 0.01 absolute /
10% relative rule recovers 13/17 missed-available truth-lateral branches with
4.598 extra retained candidates per step. The tested maximum is 14/17 at
0.01/20%, but that costs 6.317 extra candidates per step, so the default rule
is a defensible balanced threshold rather than a max-fanout setting.
Run `1338` resolves the close50 270/280 concern into a paper-safe 30 mm clean
threshold with sub-30 caveats rather than a new GPU-probe queue.
Run `079` links the detector review/branch-transfer failures to that same
close50 linear 29.5 mm sub-30 caveat, while keeping per-seed physics
equivalence and detector-seeded FWI blocked.
Run `039` formalizes the paper-safe detector role as a rank-gated upper-bound
rather than an FWI launch queue. The next useful local 2D work is therefore
to test branch-family transfer on additional saved/skip-existing close-spacing
cases or close the radius/material and review-case blockers behind the new
branch-specific x/z contract, not to launch a broad GPU run.
Runs `113-140` now provide field
cue/support traceability, complete source notes, timing-envelope integration,
spatial-transfer rejection, short-anchor interval support, a time-zero
evidence ladder, short-anchor leave-one/content-only redundancy, and a
short-anchor spatial-consistency guardrail plus field inversion/HPC readiness
synthesis, waveform-coherence QC, radius-degeneracy guardrails, signed
morphology QC plus threshold-margin and timing-margin sensitivity for the field
supplement path, a curated publication-bundle refresh, a signal-contrast
guardrail with sensitivity caveat, the post-signal-contrast curated field
bundle, current source-note coverage, and the broad-event signal-contrast
regime synthesis plus the post-contrast inversion blocker map, controlled
acquisition design, existing-data control manifesting, time-zero control-gap
manifesting, and controlled 2D acquisition protocol design. Run `118` is the current field dimensionality/HPC decision
refresh, run `120` is the short-anchor leave-one audit, run `121` is the
current post-leave-one field time-zero evidence ladder, run `122` is the
current short-anchor spatial-consistency audit, run `123` is the current field
inversion/HPC readiness synthesis, run `124` is the current short-anchor
waveform-coherence audit, run `125` is the current short-anchor
radius-degeneracy audit, run `126` is the current short-anchor signed
morphology audit, run `127` is the current signed-morphology threshold
sensitivity audit, run `128` is the current field publication-bundle freshness
audit, run `129` is the current signed-morphology timing-margin audit, run
`131` is the current short-anchor signal-contrast audit, run `132` is the
current signal-contrast sensitivity audit, run `133` is the current curated
field publication-claim bundle, run `134` is the current source-note coverage
endpoint, run `135` is the current signal-contrast regime synthesis, run
`136` is the current field inversion blocker map after contrast evidence, run
`137` is the current controlled-acquisition design, run `138` is the current
existing-data control manifest, run `139` is the current time-zero control-gap
manifest, run `140` is the current controlled 2D acquisition protocol, run `079`
is the current detector/sampling-boundary integration
audit, run `074` is the current detector/physics ambiguity-link audit, run `077` is the current detector
refinement launch-contract audit, run `081` is the current coordinate-only
detector seed export, run `084` is the current detector lateral-slot
neighborhood budget, run `086` is the current matched x/z detector
seed-geometry audit, run `088` is the current branch-specific x/z
seed-neighborhood contract, run `089` is the current detector radius/material
prior-scope audit, run `090` is the current controlled-prior refinement budget,
run `091` is the current exact-radius seed non-overlap preflight, run `092` is
the current exact-radius seed repair design, run `1341` is the current
repaired exact-radius waveform pilot, run `1342` is the current middle-branch
counterfactual target2-unlock diagnostic, run `093` is the current
branch-lock counterfactual synthesis, run `1343` is the current
branch-preserving coupled middle/right search diagnostic, run `094` is the current
branch-preservation archive audit, run `095` is the current
branch-preservation actionability triage, run `096` is the current
branch-preservation threshold sensitivity, and run `087` is the current
combined manuscript table pack.
Run `1338` is the current close50 sampling-boundary synthesis.
Field data remain local CPU-side 2D timing, morphology QC, and manuscript
supplement evidence only.
Run `136` makes that field boundary explicit after the latest contrast work:
all six positive field evidence axes support a scoped morphology supplement,
but all nine blocker axes remain unresolved. Six are critical blockers for
inversion: absolute time-zero, profile spatial calibration, radius/geometry
seeding, absolute amplitude calibration, cover-depth recovery, and field FWI.
The dataset is still independent 2D line profiles, so 3D/HPC field inversion
remains blocked.
Run `097` then turns the branch-preservation close50 actionability rows into a
case-specific GPU readiness gate. It blocks the Tx/Rx25 rows as already-below-
threshold archive caveats and identifies exactly one useful source-count
question: whether the saved source3 Tx/Rx40 seed34 miss is seed-specific.
Runs `1344` and `1345` answer that question with bounded GPU replicates for
seeds 13 and 21. Both reproduce the source3 result, selecting
`x=299 mm, z=90 mm, r=7.5 mm`. Run `099` closes the synthesis: source3 fails
across seeds 13/21/34 with 0/6 truth-geometry rows, while source4 and source5
are clean across the same seeds with 6/6 strong truth-geometry rows each. This
supports a close50 Tx/Rx40 source-density transition claim and closes
additional GPU replication for that local question.
Summary table `100` then maps that source-density evidence against the wider
saved close-spacing archive. It finds 13 grouped evidence rows: close50 is the
only matched three-seed source-count transition, while close14/25/28 mainly
provide source4/source5 exact-recovery context. The close14 source3 row remains
single-seed context only. This blocks broad GPU source-density sweeps and
detector-seeded FWI; any further source3 spacing probe should be deferred until
the manuscript specifically needs cross-spacing generalization.
Runs `1346` and `1347` close the close14 source3 single-seed caveat with two
bounded Tx/Rx45 seed replicates. Summary table `102` now combines them with
the saved run `336` and source4/source5 context: close14 source3 has 3 seeds,
6 rows, 5/6 truth-geometry rows, 6/6 strong-confidence rows, 0 radius error,
and only one 1 mm adjacent x-branch selection from saved seed34
source-mismatch. Source4 is clean across the same nominal-noise seed set, and
source5 is clean in the higher-noise boundary context. This means close14
source3 is a near-exact three-seed context result, not a replicated failure and
not a broad GPU-launch trigger. The close50 source3 failure should therefore
be framed as spacing/acquisition-specific, not as a generic three-source rule.
Summary table `103` refreshes the broader close-spacing archive map with that
close14 result. The map still has 13 grouped evidence rows and still supports
the close50 Tx/Rx40 source-density transition: source3 fails across
seeds 13/21/34 while source4/source5 are exact. The stale non-close50 source3
incomplete-family flag is now empty, and `close14` appears under
near-exact non-close50 source3 families. Broad source-density GPU sweeps,
detector-seeded FWI, and field/3D handoff remain blocked by this map.
Summary table `104` reconciles the local 2D detector-baseline evidence. The
simple top-20 detector baseline remains weak with 0/12 all-truth cases, but
the saved-B-scan CPU sensitivity and rank-policy tables show 12/12 all-truth
candidate-list recovery only at deeper budgets: minimal rank cap 40 and the
current rank-gated upper bound at top-200 candidate triples per case. The
allowed manuscript use is a baseline ladder: naive detector under-resolves,
tuned candidate lists can contain the truth at deeper ranks, but no validated
truth-free top-1 selector or detector-seeded FWI handoff is ready. Broad GPU,
field work, and 3D/HPC remain blocked by this synthesis.
Summary table `101` closes the target1 weak-but-exact confidence-policy
question from saved CPU summaries. Target1 has 43 canonical weak-exact rows;
36/36 modern ringdown050 rows and all 12 seed610/seed552 problem rows are
confirmed by `late_high`, while the only target1 exception is legacy
ringdown025 run `785` with no GPU priority. All 17 target1 source-density
series in the guarded 700-1259 table preserve exact geometry, including the
three all-weak source-density series. The production gate remains base margin;
`late_high` is diagnostic secondary confirmation only. Broad target1 GPU
sweeps and a run `785` exception probe remain blocked.
Run `137` turns the field blocker map into a controlled-acquisition design:
future field inversion would require absolute timing, surveyed profile/target
geometry, known radius/diameter, known cover depth plus dielectric/velocity
calibration, and reference amplitude calibration. The current local GSSI
archive remains a scoped 2D morphology/timing supplement, not a field FWI,
3D/HPC, or heavy-compute workload.
Run `138` maps the existing local GSSI data against those controls. The archive
has four DZT/DZX independent 2D line profiles, 7.215945 m of parsed profile
length, relative short-pair timing, morphology, spatial-residual, and relative
contrast QC evidence, but satisfies 0/5 must-have inversion controls. Field
FWI, heavy field GPU work, and field 3D/HPC remain blocked; the meaningful
field-side next work is controlled 2D acquisition protocol or metadata
collection, not inversion on the current archive.
Run `139` consolidates the current field timing evidence into an absolute
time-zero control-gap manifest. It records 0 absolute time-zero candidates:
short content-backed relative timing remains supported at 0.127701 ns, but the
early/direct component is a 0 ns common-mode negative control and differs from
the content timing by 0.127701 ns, exceeding the 0.058939 ns conservative
half-width. The next useful timing work is an external air/direct-wave or
metal-plate reference in a controlled 2D acquisition, not field FWI on the
current archive.
Run `140` turns the field blockers into a controlled 2D acquisition protocol:
8 protocol steps, 5 metadata tables, 51 required metadata fields, 7 acceptance
gates, and at least 3 short-profile repeats per controlled target. The
field-sheet template covers session metadata, target truth, profile geometry,
acquisition-run references, and timing/amplitude reference measurements. This
is the current practical field-next-step endpoint; it enables future data
collection, while current-archive field FWI, heavy GPU field work, and field
3D/HPC remain blocked.
Run `141` operationalizes that protocol into a controlled-acquisition packet:
five separate CSV templates, 51 required-field validation rules, and a
current-archive prefill-limit table. The old GSSI archive can partially
prefill session, profile-geometry, and acquisition-run provenance, but cannot
fill target-truth or external reference-measurement controls. The next
field-side action is therefore a future filled packet plus validation, not
current-archive FWI or heavy GPU work.
Run `142` adds that validation gate. Validating the generated blank packet
produces 51/51 blocking required-field findings, 0 filled rows, and 0/7
acceptance gates ready. This is the expected current state: the packet
validator is ready, but field inversion and heavy field compute remain blocked
until a future controlled-acquisition packet is filled and passes all gates.
Run `143` then pre-fills a packet copy from the current archive where the
provenance is defensible: one session row, four profile rows, and four
acquisition rows. It deliberately leaves target-truth and reference-measurement
rows blank because the current archive has no known target geometry, target
crossings, Tx/Rx offset confirmation, or external time-zero/amplitude
references. Run `144` validates that partially filled packet: 9/11 rows are
filled and there are no dtype or cross-table failures, but 67 required fields
remain missing and all seven acceptance gates remain false. This quantifies the
remaining field blockers without promoting unsupported current-archive FWI.
Run `145` translates the missing external time-zero reference into a physical
requirement. With the archive dielectric setting `epsr=2.25`, the protocol
gate of `0.02 ns` reference uncertainty is about `2.00 mm` two-way
depth-equivalent error. The current conservative relative half-width is about
`5.89 mm`, and the short-vs-early negative-control conflict is about
`12.76 mm`. The next controlled field pass therefore needs at least three
repeatable air/direct-wave or metal-plate references at or below that
uncertainty; the current archive has zero such references and remains blocked
for absolute time-zero, calibrated depth, field FWI, heavy field compute, and
3D/HPC.
Summary table `105` audits detector feature separability over the saved
component-gate candidate triples. The candidate space contains all-truth
triples, but only 49/12180 rows are all-truth. Across 22 truth-free features,
the best top-1 feature still selects 0/12 all-truth cases. In-sample
rank-gated coverage reaches 10/12 by top 50 and 12/12 by top 200 using
`score_component_balanced`, but leave-one-case feature selection reaches only
7/12 by top 50 and 9/12 by top 200. This reinforces the detector-baseline
boundary: detector evidence is usable as rank-gated upper-bound/context
evidence, not as a detector-seeded FWI or GPU-launch gate.
Run `146` turns the current field packet blockers into an operational
collection plan. The 67 blocking findings from run `144` collapse into seven
action groups: target truth, time-zero reference, amplitude reference,
profile-target geometry, acquisition-control links, session metadata, and
reference registry. Six groups require new controlled data; only session
metadata may be recoverable from notes. The time-zero group inherits the run
`145` requirement of at least three references with `0.02 ns` uncertainty
(`1.9986 mm` depth equivalent at `epsr=2.25`). All seven acceptance gates
remain blocked, so current-archive field FWI, heavy field compute, and field
3D/HPC remain blocked, but a new controlled 2D acquisition is now actionable.
Run `147` makes that acquisition plan concrete as a packet scaffold. It creates
five collection CSVs with stable planned IDs for one controlled session, one
target, one short-repeat profile, three acquisition repeats, three time-zero
references, and three amplitude references. The scaffold deliberately keeps 72
measured/session fields blank and records `validator_expected_to_pass=false`,
so it is a worksheet for future data collection rather than evidence that the
current field archive is inversion-ready.
Summary table `106` triages the detector feature-separability blocker from run
`105`. Per-case feature choice can put all 12 cases inside top 200 and 11/12
inside top 50, so the detector candidate space is not missing truth. The
failure is feature generalization: leave-one-case feature choice has 0/12 top-1
all-truth cases, 7/12 top-50 cases, and 9/12 top-200 cases. The three
deeper-than-top-200 failures are exactly the
`target2_close50_linear29p5` source-mismatch cases for seeds 13, 21, and 34.
This keeps detector evidence as rank-gated upper-bound/context evidence and
blocks detector-seeded FWI or GPU launch from the current selector state.
Summary table `107` then tests whether that selector failure is caused by
allowing span-target features to overfit. Across 20 leave-one-case selector
policies, the best robust policy uses the `component_only` feature family with
the branch strategy. It removes the three deeper-than-top-200 failures:
top-200 coverage improves from 9/12 for the all-feature global selector to
12/12, and top-50 coverage improves from 7/12 to 10/12. Top-1 all-truth
recovery remains 0/12, so the detector baseline is stronger as a rank-gated
candidate-list result but still not a detector-seeded FWI or GPU-launch gate.
Summary table `108` explains that remaining gap by joining the refreshed
selector from run `107` back to the run `105` feature-separability rows. The
robust selector still has 0/12 top-1 all-truth cases, 10/12 top-50 cases, and
12/12 top-200 cases; even the per-case feature oracle has 0/12 top-1 cases.
All 12 selected cases have positive best-false-minus-best-truth score gaps,
and the dominant top-candidate miss is `target0,target1`. The detector result
therefore supports a rank-gated candidate-list/ambiguity claim, not an
automatic detector-seeded FWI launch.
Summary table `109` then characterizes the morphology of those top false
geometries by comparing each selected top x-triple with representative
all-truth x-triples from the saved component-gate rows. All 12 cases have
truth references and positive false-over-truth feature gaps; 12/12 still have
truth inside top 200, but 0/12 are top-1. Only 3/12 top false rows are
compressed below 75% of the truth x-span. The close14 branch accounts for all
three compressed cases, while close50 linear29p5 mostly preserves x-span but
selects the wrong branch/target subset. The dominant false mode is
`single_truth_only_target2`, with dominant missing targets `target0,target1`.
This supports a detector false-geometry/ambiguity morphology claim and still
blocks detector-seeded FWI.
Run `148` validates the run `147` controlled-collection scaffold. The scaffold
has coherent planned IDs and links: all 12 rows are recognized, dtype failures
are 0, and cross-table failures are 0. It still has 60 blocking missing
required values and 0/7 acceptance gates ready because measured target,
survey, reference, Tx/Rx, coupling, and session values are intentionally blank.
Run `149` compares that scaffold validation with the current-archive prefill
validation from run `144`. Filled rows improve from 9 to 12, missing required
values drop from 67 to 60, target-truth evidence changes from 0 to 1 row, and
short-repeat target evidence changes from 0 to 1. Time-zero and amplitude
reference evidence remain 0, so absolute time-zero, calibrated depth, field
FWI, heavy field compute, and field 3D/HPC remain blocked.
Run `150` then audits the raw GSSI DZX sidecars for recoverable
current-archive packet metadata. It recovers antenna serial `3385` and display
gain `0`, both consistent across all four profiles, and writes a recovered
packet copy. Validation improves from 67 to 65 missing required values and
from 3 to 1 missing session fields, with zero dtype or cross-table failures.
Operator, target truth, surveyed geometry, controlled Tx/Rx and coupling, and
external timing/amplitude references remain absent, so the current archive is
better documented but still blocked for field FWI, heavy field compute, and
field 3D/HPC.
Run `151` applies those same-system recovered fields to the future controlled
collection scaffold. The worksheet now pre-fills antenna serial `3385`,
software version `1.4.35`, gain setting `0`, and time range `5.0 ns`, while
explicitly noting that they must be verified or updated during collection.
Scaffold validation improves from 60 to 56 missing required values and from 6
to 2 missing session fields. The substantive gates remain blocked: date/operator
verification, measured target truth, surveyed profile geometry, controlled
Tx/Rx and coupling, measured time-zero references, and amplitude references
are still required before packet acceptance or any field inversion.
Summary table `110` reconciles the completed close50 Tx/Rx40 source-count
synthesis with the close14 Tx/Rx45 source3 synthesis. It produces six source
rows and six comparison rows over matched seeds `13,21,34`. The result supports
a close50 source-density transition: source3 is a replicated failure, while
source4 and source5 are exact three-seed recoveries. It also blocks a universal
source3-failure claim because close14 source3 is a strong, radius-exact
near-exact context with truth fraction 5/6 and only one 1 mm adjacent-x branch
selection. The manuscript-safe framing is an acquisition/spacing interaction,
not a broad source-count law. The table is ready for manuscript claim-boundary
use and still blocks broad GPU sweeps, detector-seeded FWI, field FWI, and
3D/HPC handoff.
Run `152` corrects the field packet validator for typed reference rows and
reruns validation on the recovered session scaffold from run `151`. The old
validation counted time-zero fields on amplitude-reference rows and amplitude
fields on time-zero-reference rows; the corrected logic keeps blank/unknown
reference rows strict but makes typed `metal_plate_t0` and
`amplitude_reflector` rows require only their relevant measurement fields. The
recovered scaffold now has 44 missing required values instead of 56, with zero
dtype and cross-table failures. The remaining blockers are still real
collection fields: date/operator, target truth, surveyed profile geometry,
file names, Tx/Rx offset, coupling, three time-zero measurements with
uncertainties, and three amplitude measurements with repeatability. Packet
acceptance, field FWI, heavy field compute, and field 3D/HPC remain blocked.
Run `153` refreshes the field collection action plan from that corrected
validation. The 44 blockers collapse into seven action groups: target-truth
geometry (9), time-zero references (6), amplitude references (6),
profile-target geometry (6), acquisition-control links (9), session metadata
(2), and reference file registry (6). The reference gate remains three timing
references with uncertainty `<=0.02 ns`, about `1.9986 mm` two-way depth
equivalent at the archive dielectric setting. The plan is useful for the next
controlled 2D collection pass, but current-archive field FWI, heavy field GPU
work, and field 3D/HPC remain blocked.
