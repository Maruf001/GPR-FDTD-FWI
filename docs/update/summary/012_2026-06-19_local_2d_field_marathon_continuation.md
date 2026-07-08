# Local 2D And Field Marathon Continuation

Date: 2026-06-19

## Scope

This update records the local DGX-side continuation after the June 18
manuscript-positioning work. No FDTD/FWI run, neural-network training, field
FWI, 3D/HPC job, or broad GPU sweep was launched.

## Field Packet Validation

Run `152` corrected the controlled-field packet validator for typed reference
rows and reran validation on the recovered session scaffold from run `151`.
The old validation counted time-zero fields on amplitude-reference rows and
amplitude fields on time-zero-reference rows. The corrected validator keeps
blank/unknown reference rows strict, but makes typed `metal_plate_t0` and
`amplitude_reflector` rows require only their relevant measurement fields.

Key result:

```text
output:                         outputs/field_experiments/local_gssi_51600s_2026_06_09/152_gssi51600s_recovered_scaffold_type_aware_validation
missing required values:         44
previous over-strict count:      56
dtype failures:                  0
cross-table failures:            0
ready for packet acceptance:     false
ready for field FWI/heavy work:  false
ready for field 3D/HPC:          false
gpu priority:                    none
```

Run `153` refreshed the controlled-collection action plan from that corrected
validation. The 44 blockers collapse into seven action groups:

```text
target-truth geometry:       9 fields
time-zero references:        6 fields
amplitude references:        6 fields
profile-target geometry:     6 fields
acquisition-control links:   9 fields
session metadata:            2 fields
reference file registry:     6 fields
```

The reference gate remains three timing references with uncertainty
`<=0.02 ns`, about `1.9986 mm` two-way depth equivalent at the archive
dielectric setting. This is ready as a future controlled 2D collection plan,
not as current-archive field inversion evidence.

## Field QC To Collection Bridge

Run `154` connects the current field-QC evidence to the corrected controlled
2D collection action plan.

Key result:

```text
output:                                      outputs/field_experiments/local_gssi_51600s_2026_06_09/154_gssi51600s_field_qc_to_controlled_collection_bridge
evidence axes:                               9
current archive supported axes:              5
inversion blocker axes:                      4
unresolved inversion blocker axes:           4
action groups:                               7
critical new-data action groups:             5
packet blocking findings:                    44
failed acceptance gates:                     7
ready for current archive QC supplement:     true
ready for absolute time-zero:                false
ready for calibrated depth/radius:           false
ready for current archive field FWI:         false
ready for current archive heavy field work:  false
ready for field 3D/HPC:                      false
gpu priority:                                none
```

Supported current-archive uses are scoped 2D field-QC/manuscript supplement
uses: independent 2D line-profile context, short relative timing, waveform
morphology, content-only timing margin, and broad-window signal contrast.

Blocked inversion uses remain absolute time-zero, amplitude calibration,
target truth/profile geometry, controlled packet acceptance, field FWI, heavy
local GPU field work, and field 3D/HPC. The next field-facing work is a
controlled 2D collection packet with target truth, time-zero references,
amplitude references, surveyed profile geometry, and controlled acquisition
links.

## Field Collection Handoff

Run `155` packages the field next step into a collection-facing handoff built
from runs `151-154`.

Key result:

```text
output:                                outputs/field_experiments/local_gssi_51600s_2026_06_09/155_gssi51600s_controlled_collection_handoff
handoff actions:                       7
critical new-data actions:             5
packet rows:                           12
packet rows needing entry:             12
missing required values:               44
blocking findings:                     44
acceptance gates:                      7
failed acceptance gates:               7
reference repeat gate:                 3
reference uncertainty gate:            0.02 ns
field geometry type:                   independent_2d_line_profiles
ready for collection day:              true
ready for packet acceptance:           false
ready for current archive field FWI:   false
ready for heavy field work:            false
ready for field 3D/HPC:                false
gpu priority:                          none
```

The run writes `data/field_controlled_collection_run_sheet.md`, an action CSV,
a packet fill map, a gate handoff table, and a summary figure. The run-sheet
names the planned scaffold IDs (`T_CONTROL_001`, `P_CONTROL_001`,
`T0_REF_001-003`, and `AMP_REF_001-003`) and keeps the hard stop rule: no field
FWI, heavy local GPU field work, field 3D/HPC, or neural-network training from
this archive until a filled controlled packet passes validation and all gates
pass.

## Field Critical-Path Checkpoint

Run `156` audits the critical path from the controlled-collection handoff to
packet acceptance.

Key result:

```text
output:                                  outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path
actions:                                 7
new controlled-data actions:             6
critical new-data actions:               5
field-inversion prerequisite actions:    3
acceptance gates:                        7
ready gates:                             0
current-archive unblockable gates:       0
packet rows needing entry:               12
missing required values:                 44
ready for collection execution:          true
ready for packet acceptance:             false
ready for current archive field FWI:     false
ready for heavy field work:              false
ready for field 3D/HPC:                  false
gpu priority:                            none
```

The field-FWI/heavy-work critical path is
`target_truth_geometry -> time_zero_reference -> amplitude_reference`. The
packet-acceptance metadata path remains profile geometry, acquisition links,
session metadata, and reference registry. The current field endpoint is
therefore a controlled 2D collection checklist, not an inversion, GPU, 3D/HPC,
or neural-network launch.

## Controlled-Prior Detector Refinement Table Pack

Summary table `124` refreshes the combined local 2D and field manuscript table
pack after adding the detector radius/material prior-scope audit (`089`) and
controlled-prior refinement budget (`090`).

Key result:

```text
output:                                      outputs/summary_tables/124_local_2d_field_manuscript_table_pack_post_controlled_prior_budget
metric rows:                                 290
auxiliary evidence metrics:                  274
controlled synthetic radius/material prior:  ready
detector-inferred radius/material prior:     false
fixed-radius fine budget points:             29936602
fixed-radius coarse budget points:           156250
known-radius permutation multiplier:         6.0
independent-radius multiplier:               27.0
refinement launch ready:                     false
detector-seeded FWI ready:                   false
gpu priority:                                none
ready for manuscript table use:              true
```

Interpretation: stable saved detector cases now have a controlled synthetic
radius/material prior budget for design sizing, but this remains distinct from
a detector-inferred radius/material seed. It does not authorize refinement,
FWI, GPU work, field transfer, 3D/HPC, or neural-network training.

## Cross-Domain Scope Boundary

Summary table `125` refreshes the cross-domain local 2D/field scope map against
the current manuscript table pack (`124`).

Key result:

```text
output:                                 outputs/summary_tables/125_local_2d_field_cross_domain_scope_map_post_controlled_prior_budget
scope rows:                             8
field min same-time spacing:            96.657 mm
synthetic close-spacing context max:    50.0 mm
field/synthetic spacing ratio:          1.93314
field resolution benchmark ready:       false
field absolute time-zero ready:         false
field FWI ready:                        false
detector controlled prior ready:        true
detector-inferred radius/material:      false
controlled-prior fixed fine points:     29936602
controlled-prior permutation factor:    6.0
refinement launch ready:                false
detector-seeded FWI ready:              false
gpu priority:                           none
ready for manuscript scope table:       true
```

Interpretation: the field archive is measured 2D QC/context, not a known-truth
validation benchmark for the synthetic close-spacing threshold. Synthetic
resolution evidence, measured-field timing/spacing QC, and controlled-prior
detector-refinement design sizing should remain separate manuscript claims.

## Fixed-Radius Detector Second Pass

Run `1357` executed the one selected guarded GPU pilot from the repaired
`target2_close14|seed21|nominal` fixed-radius detector seed state. The command
used the resource guard with RAM capped at 80% and GPU utilization capped at
90%.

Key result:

```text
output:                    outputs/experiments/1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu
initial state:             [191,252,266] / [90,89,91] mm
final state:               [190,251,265] / [90,89,91] mm
truth:                     [190,250,264] / [90,90,90] mm
initial L-infinity error:  2 mm
final L-infinity error:    1 mm
guard aborted:             false
max GPU utilization:       88%
max RAM used:              14.996%
```

Summary table `127` refreshes the fixed-radius pilot selector after this run:

```text
output:                       outputs/summary_tables/127_local_2d_detector_fixed_radius_pilot_outcome_synthesis_post_second_pass
pilot runs included:          3
best final residual:          1 mm
within-1-mm residual pilots:  1
immediate second pass ready:  false
broad GPU queue ready:        false
detector-seeded FWI ready:    false
gpu priority:                 none
```

Summary table `128` audits the residual cause from the `1357` candidate tables:

```text
output:                                      outputs/summary_tables/128_local_2d_detector_fixed_radius_residual_ambiguity_audit_post_second_pass
selected truth coordinate count:             1
truth selected but ambiguous count:          1
truth present but objective-neighbor count:  1
truth absent after non-overlap filter count: 1
immediate GPU iteration ready:               false
broad GPU queue ready:                       false
detector-seeded FWI ready:                   false
```

Interpretation: the residual is not a simple missing-local-samples problem.
Target 0 selects truth but has a near tie, target 1 has the exact coordinate
present but slightly worse than a neighbor, and target 2's exact coordinate is
absent after non-overlap filtering because the sequential state still contains
the target1 residual. The next step is CPU-side update-order/coordinate-locking
design before any additional detector-refinement GPU work.

Summary table `129` folds this into the manuscript table pack:

```text
output:                              outputs/summary_tables/129_local_2d_field_manuscript_table_pack_post_fixed_radius_residual_audit
metric rows:                         301
auxiliary evidence metrics:          285
fixed-radius pilot runs:             3
best fixed-radius residual:          1 mm
objective-neighbor residual count:   1
non-overlap-absent residual count:   1
gpu priority:                        none
ready for manuscript table use:      true
```

## Fixed-Radius Locking Mechanism Validation

Summary table `130` converts the residual audit into a CPU-side
coordinate-locking hypothesis: lock target 1 at `[250,90]` instead of the
greedy `[251,89]`, then run one guarded target-2 unlock probe. The selected
lock has a 3.4146% objective penalty but improves downstream target-2 truth
clearance from `-0.961595 mm` to `0 mm`.

Run `1358` executed exactly that one guarded validation probe:

```text
output:                    outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu
initial state:             [190,250,266] / [90,90,91] mm
final state:               [190,250,264] / [90,90,90] mm
final L-infinity error:    0 mm
guard aborted:             false
max GPU utilization:       88%
max RAM used:              14.688%
```

Summary table `131` synthesizes the result:

```text
output:                              outputs/summary_tables/131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe
exact geometry recovered:            true
truth selected but ambiguous count:  1
locking mechanism claim ready:       true
general detector policy ready:       false
broad GPU queue ready:               false
detector-seeded FWI ready:           false
gpu priority:                        none
```

Summary table `132` folds this into the manuscript table pack:

```text
output:                              outputs/summary_tables/132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation
metric rows:                         308
auxiliary evidence metrics:          292
locking validation exact:            true
locking broad GPU ready:             false
gpu priority:                        none
ready for manuscript table use:      true
```

Interpretation: this validates a fixed-radius near-tie
downstream-clearance mechanism on one repaired branch. It is not a broad
detector-policy result, not a detector-seeded FWI trigger, and not field
transfer evidence.

## Source-Density Claim Boundary

Summary table `111` audits the confounds in the close50/close14 source-density
comparison after summary table `110`.

Key result:

```text
output:                                 outputs/summary_tables/111_close_spacing_source_density_confound_audit
matched control factors:                 5
intended spacing axes:                   1
acquisition confounds:                   1
geometry confounds:                      1
metadata gaps:                           1
context-only factors:                    1
close50 within-family transition ready:  true
guarded cross-spacing contrast ready:    true
spacing-only causal claim ready:         false
ready for broad GPU queue:               false
gpu priority:                            none
```

Safe wording:

```text
Close50 Tx/Rx40 shows a within-family source-density transition, and close14
Tx/Rx45 source3 is a strong near-exact three-seed context.
```

Blocked wording:

```text
Target spacing alone controls source3 success/failure across close14 and
close50.
```

Reason: close50 and close14 also differ in Tx/Rx offset and absolute target2
x-position, and the source5 cross-family evidence mixes nominal close50 context
with close14 noise-boundary context. A spacing-only causal claim would require
a deliberately matched narrow probe, not a broad GPU queue.

Summary table `112` turns that matched-probe option into a concrete
skip-existing queue without launching it.

Key result:

```text
output:                                outputs/summary_tables/112_close_spacing_matched_source3_probe_queue
probe families:                        2
seed probe count:                      6
existing seed probes:                  0
missing seed probes:                   6
estimated missing GPU runtime:         128.88 min
ready for matched narrow queue:        true
ready for spacing-only claim now:      false
ready for broad GPU queue:             false
maximum parallel GPU jobs:             1
autonomous GPU launch ready:           false
gpu priority:                          narrow_conditional_not_launched
```

The two queued families are:

```text
close14 source3 Tx/Rx40 seeds 13/21/34
close50 source3 Tx/Rx45 seeds 13/21/34
```

These are the only synthetic GPU extensions currently justified by the source
density/confound chain. They should be run only if the manuscript needs a
spacing-only causal claim, one seed at a time, under the hard GPU/RAM caps.

Run `1348` executes the first priority-1 matched seed under
`run_resource_guarded_command.py`:

```text
output:                                  outputs/experiments/1348_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives
probe:                                   close14 source3 Tx/Rx40 seed13
target2 truth:                           x=264 mm, z=90 mm, r=8 mm
target2 final:                           x=264 mm, z=90 mm, r=8 mm
confidence labels:                       strong, strong
minimum radius margin abs:               0.003136
maximum ambiguity x width:               2.0 mm
guard max observed GPU utilization:      83%
guard max observed RAM use:              14.85%
guard aborted:                           false
```

Summary table `115` is the current matched-source3 queue endpoint after that
run:

```text
queue status:                            partially_complete_ready_skip_existing
existing seed probes:                    1
missing seed probes:                     5
estimated remaining GPU runtime:         109.78 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

The completed seed is useful because it does not reproduce the close50 Tx/Rx40
source3 failure under matched Tx/Rx. It is still only one seed; the archive
does not yet support a spacing-only causal statement.

Run `1349` executes the second priority-1 matched seed under the same resource
guard:

```text
output:                                  outputs/experiments/1349_coordinate_optimizer_close14_seed21_sources3_txrx40_objectives
probe:                                   close14 source3 Tx/Rx40 seed21
target2 truth:                           x=264 mm, z=90 mm, r=8 mm
target2 final:                           x=264 mm, z=90 mm, r=8 mm
confidence labels:                       strong, strong
minimum radius margin abs:               0.003490
maximum ambiguity x width:               2.0 mm
guard max observed GPU utilization:      84%
guard max observed RAM use:              14.68%
guard aborted:                           false
```

Summary table `116` is the current matched-source3 queue endpoint after the
second close14 matched seed:

```text
queue status:                            partially_complete_ready_skip_existing
existing seed probes:                    2
missing seed probes:                     4
missing probes:                          close14 Tx/Rx40 seed34;
                                         close50 Tx/Rx45 seeds 13/21/34
estimated remaining GPU runtime:         90.67 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

The close14 Tx/Rx40 matched family is now two-thirds complete and both completed
seeds select the exact target2 branch with strong confidence. The remaining
close14 seed `34` is needed before aggregating that family, and the reciprocal
close50 Tx/Rx45 family is still missing.

Run `1350` completes the close14 Tx/Rx40 matched family with seed `34`, again
under the resource guard:

```text
output:                                  outputs/experiments/1350_coordinate_optimizer_close14_seed34_sources3_txrx40_objectives
probe:                                   close14 source3 Tx/Rx40 seed34
target2 truth:                           x=264 mm, z=90 mm, r=8 mm
target2 final:                           x=264 mm, z=90 mm, r=8 mm
confidence labels:                       strong, strong
minimum radius margin abs:               0.003307
maximum ambiguity x width:               2.0 mm
guard max observed GPU utilization:      84%
guard max observed RAM use:              14.80%
guard aborted:                           false
```

Run `1351` aggregates the three close14 matched seeds:

```text
output:                                  outputs/experiments/1351_coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
confidence rows:                         6
truth geometry rows:                     6
confidence labels:                       strong=6
fallback warnings:                       0
minimum radius margin abs:               0.003136
mean radius margin abs:                  0.003478
maximum radius margin abs:               0.003864
maximum ambiguity x width:               2.0 mm
```

Summary table `117` is the current matched-source3 queue endpoint after the
close14 aggregate:

```text
queue status:                            partially_complete_ready_skip_existing
existing seed probes:                    3
missing seed probes:                     3
missing probes:                          close50 Tx/Rx45 seeds 13/21/34
estimated remaining GPU runtime:         71.57 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

The close14 matched family now supports a strong, replicated matched-control
result at Tx/Rx `40 mm`, but not a spacing-only causal statement. The reciprocal
close50 Tx/Rx45 matched family remains the missing half of that causal test.

Run `1352` executes the first reciprocal close50 Tx/Rx45 matched seed:

```text
output:                                  outputs/experiments/1352_coordinate_optimizer_close50_seed13_sources3_txrx45_objectives
probe:                                   close50 source3 Tx/Rx45 seed13
target2 truth:                           x=300 mm, z=90 mm, r=8 mm
target2 final:                           x=299 mm, z=90 mm, r=7.5 mm
confidence labels:                       moderate, strong
minimum radius margin abs:               0.000774
truth selected all cases:                false
guard max observed GPU utilization:      84%
guard max observed RAM use:              14.61%
guard aborted:                           false
```

Summary table `118` is the current matched-source3 queue endpoint after that
first close50 reciprocal seed:

```text
queue status:                            partially_complete_ready_skip_existing
existing seed probes:                    4
missing seed probes:                     2
missing probes:                          close50 Tx/Rx45 seeds 21/34
estimated remaining GPU runtime:         47.72 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

This first reciprocal seed is near-truth but not exact. It strengthens the
matched-control contrast with the completed close14 family, but close50 Tx/Rx45
seeds `21` and `34` are still required before aggregating that reciprocal
family.

Run `1353` executes the second reciprocal close50 Tx/Rx45 matched seed:

```text
output:                                  outputs/experiments/1353_coordinate_optimizer_close50_seed21_sources3_txrx45_objectives
probe:                                   close50 source3 Tx/Rx45 seed21
target2 truth:                           x=300 mm, z=90 mm, r=8 mm
target2 final:                           x=299 mm, z=90 mm, r=7.5 mm
confidence labels:                       moderate, strong
minimum radius margin abs:               0.000733
truth selected all cases:                false
guard max observed GPU utilization:      84%
guard max observed RAM use:              14.77%
guard aborted:                           false
```

Summary table `119` is the current matched-source3 queue endpoint:

```text
queue status:                            partially_complete_ready_skip_existing
existing seed probes:                    5
missing seed probes:                     1
missing probes:                          close50 Tx/Rx45 seed34
estimated remaining GPU runtime:         23.86 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

Seed `21` repeats seed `13`: both cases select the same near-truth wrong branch
at `x=299 mm`, `r=7.5 mm`. Close50 Tx/Rx45 seed `34` is still required before
aggregating the reciprocal family.

Run `1354` completes the reciprocal close50 Tx/Rx45 matched family with seed
`34`:

```text
output:                                  outputs/experiments/1354_coordinate_optimizer_close50_seed34_sources3_txrx45_objectives
probe:                                   close50 source3 Tx/Rx45 seed34
target2 truth:                           x=300 mm, z=90 mm, r=8 mm
target2 final:                           x=299 mm, z=90 mm, r=7.5 mm
confidence labels:                       moderate, moderate
minimum radius margin abs:               0.000741
truth selected all cases:                false
guard max observed GPU utilization:      84%
guard max observed RAM use:              14.55%
guard aborted:                           false
```

Run `1355` aggregates the three close50 reciprocal matched seeds:

```text
output:                                  outputs/experiments/1355_coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
confidence rows:                         6
truth geometry rows:                     0
confidence labels:                       moderate=4, strong=2
fallback warnings:                       0
minimum radius margin abs:               0.000733
mean radius margin abs:                  0.000906
maximum radius margin abs:               0.001110
maximum ambiguity x width:               0.0 mm
selected branch in all rows:             x=299 mm, z=90 mm, r=7.5 mm
```

Summary table `120` completes the matched-source3 queue:

```text
queue status:                            complete_ready_for_aggregation
existing seed probes:                    6
missing seed probes:                     0
estimated remaining GPU runtime:         0.00 min
ready for spacing-only claim now:        false
ready for broad GPU queue:               false
```

The completed matched-source3 evidence is now:

```text
close14 source3 Tx/Rx40:                 6/6 truth rows, strong=6
close50 source3 Tx/Rx45:                 0/6 truth rows, moderate=4, strong=2
```

This is stronger than the earlier confounded source-density comparison, but it
still should be framed as an acquisition/geometry-aware contrast rather than a
spacing-only causal proof. The close50 reciprocal family repeatedly selects a
near-truth wrong branch, so the next synthetic step should be synthesis and
manuscript policy, not another broad GPU branch.

Summary table `121` turns the completed matched-source3 results into a compact
paper-facing policy table:

```text
output:                                      outputs/summary_tables/121_close_spacing_matched_source3_policy_synthesis
queue complete:                              true
close14 truth-geometry fraction:             1.0
close50 truth-geometry fraction:             0.0
close14 all truth and strong:                true
close50 replicated wrong branch:             true
guarded acquisition/geometry contrast ready: true
spacing-only causal generalization ready:    false
ready for broad GPU queue:                   false
ready for field FWI:                         false
ready for 3D/HPC handoff:                    false
ready for neural-network training:           false
gpu priority:                                none
```

This is the current source-density manuscript boundary: report the matched
source3 contrast with explicit acquisition/geometry caveats; do not claim
spacing-only causality, and do not launch another broad local GPU branch from
this result.

Summary table `122` refreshes the local manuscript contribution matrix with
that matched-source3 policy row:

```text
output:                                  outputs/summary_tables/122_local_2d_manuscript_contribution_matrix_post_matched_source3_policy
contribution rows:                       11
ready rows:                              10
deferred rows:                           1
review rows:                             0
synthetic immediate GPU candidates:      0
synthetic conditional GPU candidates:    0
field ready for 2D QC:                   true
field ready for FWI:                     false
field ready for 3D/HPC:                  false
gpu priority:                            none
ready for manuscript positioning:        true
```

The new contribution row is
`matched_source3_acquisition_geometry_contrast`. It records the close14
truth fraction `1.0`, close50 truth fraction `0.0`, close50 replicated wrong
branch `true`, and spacing-only claim `false`. This moves the result into the
main paper-planning artifact without changing the no-broad-GPU policy.

Run `1356` refreshes the synthetic next-question matrix after the
matched-source3 policy:

```text
output:                                  outputs/experiments/1356_synthetic_2d_next_question_matrix_post_matched_source3_policy
candidate count:                         11
cpu-first count:                         0
immediate GPU-priority candidates:       0
conditional GPU candidates:              0
target1 acquisition surface included:    true
target1 exception map included:          true
matched-source3 policy included:         true
top question:                            synthetic_publication_bundle_current
top readiness:                           no_gpu_required
gpu priority:                            none_now
```

This closes the current synthetic compute queue under the already-posed 2D
hypotheses. The old close50 270/280 branch remains a target2-only claim caveat,
target1 source-density remains closed under the current hypothesis, and the
matched-source3 result is manuscript evidence for guarded acquisition/geometry
contrast, not spacing-only proof or a broad GPU queue.

Summary table `123` refreshes the combined local 2D/field manuscript table pack
using the current synthetic no-GPU endpoint and the field collection handoff:

```text
output:                                  outputs/summary_tables/123_local_2d_field_manuscript_table_pack_post_current_handoff
claim table rows:                        32
figure inventory rows:                   31
metric rows:                             270
synthetic claims:                        11
field claims:                            21
synthetic figures:                       9
field figures:                           22
field collection handoff included:       true
field handoff ready collection day:      true
field handoff ready packet acceptance:   false
field handoff ready field FWI:           false
field handoff ready 3D/HPC:              false
gpu priority:                            none
ready for manuscript table use:          true
```

This table pack keeps the field handoff as a guardrail rather than a validation
claim: it makes the controlled-collection next step visible in the manuscript
metrics while preserving the blocked packet-acceptance, field-FWI, heavy-field,
and 3D/HPC gates.

## Current Decision

The local 2D/field work remains publishable as a controlled synthetic 2D
identifiability and ambiguity-margin study with measured field data used as
scoped 2D timing/morphology and collection-planning evidence. Current field
data remain 2D profile QC only, but run `155` now gives the next controlled
field collection run sheet. The synthetic side has no immediate or conditional
GPU candidate under run `1356`; any new GPU work should start from a new
objective, geometry, or acquisition hypothesis. 3D/HPC work stays separate.
Resource-guarded GPU work stayed within the requested ceilings; the latest
close50 seed reached 84% GPU utilization and 14.55% RAM use.
