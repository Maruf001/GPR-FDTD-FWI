# Local 2D And Field Report Checkpoint

Date: 2026-06-19

## Scope

This checkpoint pauses the current local DGX-side campaign at a clean,
reportable milestone. It preserves the current local 2D synthetic/refinement
state, the measured-field GSSI state, and the policy boundaries needed for a
later report.

No new experiment block should be inferred from this file. It records the
state after the fixed-radius detector mechanism validation and the field
controlled-collection critical-path audit.

## Preserved Outputs

```text
local synthetic experiment root:    outputs/experiments
latest synthetic experiment:        1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu
experiment directories observed:    1359 including _by_category_symlinks
experiment run manifests observed:  1352

summary table root:                 outputs/summary_tables
latest summary table:               132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation
summary-table dirs observed:        138
summary-table run manifests:        132

field experiment root:              outputs/field_experiments/local_gssi_51600s_2026_06_09
latest field run:                   156_gssi51600s_controlled_collection_critical_path
field run dirs observed:            156
field run manifests observed:       156
```

The current report window for synthetic local 2D should start around the
post-`1200` detector/close-spacing sequence, with earlier `700-1259`
archive evaluations used as context rather than the main narrative. The most
reportable local endpoint is the sequence:

```text
1357 guarded fixed-radius second pass
130  CPU locking-policy design
1358 guarded target2 unlock validation
131  locking-policy validation synthesis
132  local 2D/field manuscript table pack refresh
```

The measured-field report window should cover the full dataset-local chain
`001-156`, with the field endpoint being run `156`.

## Local 2D Synthetic Checkpoint

The fixed-radius detector branch reached its natural checkpoint.

Run `1357` was the selected guarded second pass from the repaired exact-radius
seed state:

```text
output:                    outputs/experiments/1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu
initial state:             [191,252,266] / [90,89,91] mm
final state:               [190,251,265] / [90,89,91] mm
truth:                     [190,250,264] / [90,90,90] mm
final L-infinity error:    1 mm
max GPU utilization:       88%
max RAM used:              14.996%
```

Run `128` showed the residual cause was not a missing-local-samples problem:

```text
truth selected but ambiguous count:          1
truth present but objective-neighbor count:  1
truth absent after non-overlap filter count: 1
immediate GPU iteration ready:               false
```

Run `130` produced one falsifiable CPU-side locking hypothesis:

```text
lock target:                         1
lock coordinate:                     [250,90] mm
objective penalty relative to greedy: 3.4146%
downstream truth clearance before:   -0.961595 mm
downstream truth clearance after:    0 mm
single guarded unlock probe ready:   true
```

Run `1358` executed only that guarded unlock probe:

```text
output:                    outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu
initial state:             [190,250,266] / [90,90,91] mm
final state:               [190,250,264] / [90,90,90] mm
final L-infinity error:    0 mm
target updated:            2 only
max GPU utilization:       88%
max RAM used:              14.688%
```

Run `131` validates the mechanism but keeps the claim narrow:

```text
exact geometry recovered:                true
truth selected but ambiguous count:      1
locking mechanism claim ready:           true
general detector policy claim ready:     false
broad GPU queue ready:                   false
detector-seeded FWI ready:               false
field transfer ready:                    false
gpu priority:                            none
```

Run `132` folds this into the manuscript table pack:

```text
claim rows:                         32
figure rows:                        31
metric rows:                        308
synthetic figures:                  9
field figures:                      22
locking validation exact:           true
locking broad GPU ready:            false
ready for manuscript table use:     true
gpu priority:                       none
```

### Local 2D Interpretation

This is a useful mechanism result: a truth-free near-tie/downstream-clearance
lock can recover the exact geometry on the repaired `target2_close14|seed21`
fixed-radius branch.

It is not a general detector-policy result. The exact target remains
objective-ambiguous, radii are controlled priors, and the validation covers one
branch. No broad GPU queue, detector-seeded FWI, field transfer, 3D/HPC, or
neural-network training is justified by this block.

## Field Checkpoint

The measured-field GSSI chain reached a clean controlled-collection endpoint.
The field archive is independent 2D line profiles, not a 3D survey.

Current field endpoint:

```text
output:                                  outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path
source handoff:                          155_gssi51600s_controlled_collection_handoff
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

The field-FWI/heavy-work critical path is:

```text
target_truth_geometry -> time_zero_reference -> amplitude_reference
```

The packet-acceptance metadata path is:

```text
profile_target_geometry -> acquisition_control_links -> session_metadata -> reference_registry
```

### Field Interpretation

The current archive remains reportable as scoped measured-field 2D QC and
manuscript-supplement context: independent line-profile scope, relative
short-profile timing, waveform morphology, content-only timing margin, and
broad-window signal contrast.

It is not ready for absolute time-zero, amplitude calibration, calibrated
cover-depth/radius recovery, field FWI, heavy local GPU work, 3D/HPC, or
neural-network training. Run `156` makes that boundary operational: the current
archive cannot unblock any acceptance gate without new controlled measurements.

### Why This Is A Natural Field Checkpoint

The field campaign was not stopped at an intermediate packet or partial QC
state. Runs `137-156` close a full field-side logic block:

```text
137  controlled acquisition design from field blockers
138  existing-data/control manifest
139  time-zero control-gap manifest
140  controlled 2D acquisition protocol
141  executable packet templates
142  blank packet validation
143  current-archive packet prefill
144  prefilled-packet validation
145  external time-zero reference requirement
146  blocker prioritization
147  controlled collection scaffold
148  scaffold validation
149  scaffold-vs-current validation delta
150  current-archive metadata recovery
151  recovered-session collection scaffold
152  type-aware scaffold validation
153  type-aware blocker prioritization
154  field-QC-to-collection bridge
155  collection run sheet and handoff
156  gate-by-gate critical-path audit
```

Run `156` is the natural checkpoint because it answers the next field-side
decision question completely: the current archive has no remaining CPU-side
metadata recovery or QC synthesis that can turn it into an accepted inversion
packet. The next transition requires new controlled measurements, not another
current-archive analysis pass.

## Key Failures And Ambiguities

Synthetic local 2D:

```text
target 0: truth selected but has a near objective tie
target 1: exact coordinate present but objective prefers [251,89]
target 2: exact coordinate can be excluded by non-overlap when target 1 remains wrong
fixed-radius mechanism: validated on one branch only
general detector policy: not validated
detector-inferred radius/material: not available
detector-seeded FWI: still blocked
```

Measured field:

```text
absolute time-zero: missing external references
amplitude calibration: missing amplitude references
target truth: missing controlled target geometry/material/depth/radius
profile geometry: missing surveyed controlled profile geometry
controlled repeats: missing accepted repeat acquisition links/files/Tx-Rx offsets
packet acceptance: 0 / 7 gates ready
3D/HPC field workload: blocked because archive is independent 2D line profiles
```

## Verification At Checkpoint

Focused tests passed:

```text
tests/test_local_2d_detector_fixed_radius_locking_policy_design.py
tests/test_local_2d_detector_fixed_radius_locking_policy_validation.py
tests/test_local_2d_field_manuscript_table_pack.py
tests/test_gssi_field_controlled_collection_critical_path.py
```

Recent focused result:

```text
12 passed
```

Full repository test result at checkpoint:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
995 passed
```

Figure validation exists for:

```text
outputs/summary_tables/130_local_2d_detector_fixed_radius_locking_policy_design
outputs/summary_tables/131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe
outputs/summary_tables/132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation
outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path
```

Resource cap status at checkpoint:

```text
GPU utilization: 4-5% after runs
system RAM used: about 17 GiB / 119 GiB
guarded GPU validations: max GPU 88%, max RAM below 15%
```

## Recommended Next Steps

For report writing:

```text
1. Use outputs/experiments around the post-1200 detector/close-spacing sequence as context.
2. Treat 1357 -> 130 -> 1358 -> 131 -> 132 as the current local 2D endpoint.
3. Treat outputs/field_experiments/local_gssi_51600s_2026_06_09/001-156 as the current field chain.
4. Keep synthetic identifiability, detector mechanism, and measured-field QC claims separate.
5. Include separate final planning subsections for local 2D synthetic work and field work.
```

For future local 2D synthetic work after the report checkpoint:

```text
1. Do not start broad GPU/FWI from this state.
2. Generalize the fixed-radius locking policy only with CPU-side policy design first.
3. Resume local GPU work only when a specific CPU-side falsifiable hypothesis opens a single guarded probe.
4. Treat fixed radii as controlled priors unless a detector-inferred radius/material policy is separately validated.
```

For future field work after the report checkpoint:

```text
1. Do not run field FWI, heavy local GPU field work, 3D/HPC, or neural-network training from the current archive.
2. Execute the run-155/run-156 controlled 2D collection checklist before any field inversion claim.
3. Fill target truth, time-zero references, amplitude references, surveyed profile geometry, controlled repeats, session metadata, and reference registry rows.
4. Rerun packet validation and blocker prioritization only after the controlled packet has real measurements.
5. Reconsider field FWI or heavier work only after all seven acceptance gates pass.
```
