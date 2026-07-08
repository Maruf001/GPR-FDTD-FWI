# Experiment 836: Local 2D Blind-Envelope Reliability Gate

Date: 2026-06-18

## Purpose

Build a truth-free reliability gate for the saved blind-envelope detector
assignment policy. This run reads the existing 288-variant detector policy grid
from run `059` and asks whether policy-grid x-slot drift can flag the close50
nominal ambiguity cases without using truth at inference.

This was a CPU saved-data analysis. It did not run FDTD, FWI, GPU kernels,
field FWI, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/summary_tables/069_local_2d_detector_blind_envelope_reliability_gate
```

Key artifacts:

```text
data/local_2d_detector_blind_envelope_reliability_gate_cases.csv
data/local_2d_detector_blind_envelope_reliability_gate_branches.csv
data/local_2d_detector_blind_envelope_reliability_gate_summary.json
figures/local_2d_detector_blind_envelope_reliability_gate.png
```

## Result

```text
policy label:                         local_2d_detector_blind_envelope_reliability_gate_cpu_no_fwi
cases:                                12
policy variants per case:             288
stable x-slot drift threshold:        5.0 mm
stable assignment cases:              10 / 12
review assignment cases:               2 / 12
stable assignment all-variant success: 10 / 10
tuning-sensitive cases:                2
tuning-sensitive cases detected:       2
tuning-sensitive cases missed:         0
false review all-variant success:      0
stable min success fraction:           1.0
review max x-slot range:               21.0 mm
stable max x-slot range:                5.0 mm
ready for reliability claim:           true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Review cases:

```text
target2_close50_linear29p5|seed13|nominal
target2_close50_linear29p5|seed34|nominal
```

Interpretation: policy-grid x-slot drift is a useful truth-free confidence
diagnostic. It accepts all six close14 cases and four of six close50 cases,
while flagging exactly the two close50 nominal cases already identified as
tuning-sensitive. This supports a detector reliability/ambiguity-boundary
claim, not detector-seeded FWI.

## Validation

```text
tests/test_local_2d_detector_blind_envelope_reliability_gate.py
3 passed
```

Figure validation:

```text
local_2d_detector_blind_envelope_reliability_gate.png: 2535x903,
nonwhite=0.3004, dynamic range=255
```

## Threshold Sensitivity

The follow-up threshold-sensitivity audit is:

```text
outputs/summary_tables/071_local_2d_detector_blind_envelope_reliability_threshold_sensitivity
```

Key result:

```text
policy label:                         local_2d_detector_blind_envelope_reliability_threshold_sensitivity_cpu_no_fwi
thresholds tested:                    12
clean thresholds:                      5
clean threshold range:                 5.0-19.0 mm
default threshold:                     5.0 mm
default threshold clean:               true
default stable/review cases:           10 / 2
default tuning-sensitive missed:       0
default false review:                  0
thresholds with false review:          0,1,2,3,4 mm
thresholds with tuning misses:         20,21 mm
ready for reliability claim:           true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Interpretation: the 5 mm gate is not a single-point artifact. In the audited
threshold grid, 5-19 mm is a clean interval that accepts the 10 stable cases
and flags the two close50 nominal tuning-sensitive cases. Thresholds below
5 mm over-review stable cases; thresholds at 20 mm and above begin accepting
known tuning-sensitive cases.

Validation:

```text
tests/test_local_2d_detector_blind_envelope_reliability_threshold_sensitivity.py
2 passed
```

Figure validation:

```text
local_2d_detector_blind_envelope_reliability_threshold_sensitivity.png: 2365x835,
nonwhite=0.0808, dynamic range=255
```

## Detector/Physics Ambiguity Link

The follow-up detector/physics ambiguity-link audit is:

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
linear 29.5 offset below clean:       0.5 mm
review cases with synthetic x ambiguity: 1 / 2
review cases with synthetic strict-clean rows: 1 / 2
branch-localization claim ready:      true
per-seed physics-equivalence ready:   false
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Interpretation: the detector review cases are localized to the close50
linear-29.5 nominal family just below the 30 mm clean threshold. This supports
a branch/variant ambiguity-boundary explanation, but not the stronger claim
that per-seed coordinate x ambiguity explains every detector review case.

Validation:

```text
tests/test_local_2d_detector_physics_ambiguity_link.py
2 passed
```

Figure validation:

```text
local_2d_detector_physics_ambiguity_link.png: 2399x920,
nonwhite=0.1011, dynamic range=255
```

## Detector Refinement Launch-Contract Audit

The follow-up detector refinement launch-contract audit is:

```text
outputs/summary_tables/077_local_2d_detector_refinement_launch_contract_audit
```

Key result:

```text
policy label:                         local_2d_detector_refinement_launch_contract_audit_cpu_no_fwi
cases:                                12
branches:                              2
best blind-envelope variant:          env2_struct0.4_support0.12_center0.1_span90
truth-free stable cases:              10 / 12
review cases:                          2 / 12
candidate x/z seed-table cases:       10 / 12
max component seed error:             10.0 mm
radius seed available:                false
material seed available:              false
active launch blockers:                6
ready for component seed table:       true
ready for narrow refinement contract: false
ready for detector-seeded FWI:        false
gpu priority:                         none
```

Active blockers:

```text
radius_material_contract_missing
policy_grid_selected_on_saved_corpus
deployable_top1_selector_not_validated
branch_independent_transfer_not_robust
review_cases_present
per_seed_physics_equivalence_not_ready
```

Interpretation: the stable blind-envelope detector assignments can be exported
as a saved-corpus x/z component seed table for later design work, but they do
not yet define a GPU/FWI launch contract. The missing radius/material seeds,
non-independent policy-grid selection, non-deployable top-1 selector, branch
transfer gap, review cases, and incomplete per-seed physics equivalence keep
the detector path in CPU-side evidence mode.

Validation:

```text
tests/test_local_2d_detector_refinement_launch_contract_audit.py
2 passed
```

Figure validation:

```text
local_2d_detector_refinement_launch_contract_audit.png: 2229x869,
nonwhite=0.2461, dynamic range=255
```

## Detector/Sampling Boundary Integration

The follow-up detector/sampling-boundary integration audit is:

```text
outputs/summary_tables/079_local_2d_detector_sampling_boundary_integration
```

Key result:

```text
policy label:                         local_2d_detector_sampling_boundary_integration_cpu_no_fwi
cases:                                12
detector review cases:                 2
review cases below clean threshold:    2 / 2
review nominal cases:                  2 / 2
below-clean cases:                     6
stable below-clean cases:              4
branch-transfer failure cases:         1
branch-transfer failures below clean:  1
close50 nominal review cases:          2 / 3
close50 source-mismatch reviews:       0 / 3
review x-ambiguous cases:              1 / 2
sampling first clean threshold:        30.0 mm
linear 29.5 boundary status:           exact_strong_not_clean
sub-30 clean threshold claim ready:    false
detector boundary claim ready:         true
per-seed physics equivalence ready:    false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Interpretation: the detector review cases and the leave-one-branch transfer
failure are localized to the close50 linear 29.5 mm near-boundary caveat below
the 30 mm clean threshold. This supports a branch-local detector
ambiguity-boundary claim. It does not support the stronger per-seed claim that
every detector review is explained by coordinate x ambiguity, and it does not
open a detector-seeded FWI/GPU queue.

Validation:

```text
tests/test_local_2d_detector_sampling_boundary_integration.py
2 passed
```

Figure validation:

```text
local_2d_detector_sampling_boundary_integration.png: 2433x869,
nonwhite=0.1971, dynamic range=255
```
