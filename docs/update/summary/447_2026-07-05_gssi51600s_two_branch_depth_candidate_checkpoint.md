# 447 2026-07-05 GSSI51600S Two-Branch Depth Candidate Checkpoint

## What changed

- Packaged the shallow and deep GSSI profile-subset results as two conditioned candidate branches.
- Added branch-level x, cover depth, diameter, finite length, relative permittivity, conductivity, and field-fit ranges.
- Wired the two-branch candidate into the latest GSSI prediction bundle and public query output.

## Key numbers

- Decision: `two_depth_branch_candidate_report_conditioned`.
- Mean cover-depth gap between branches: `0.05223581939935684 m`.
- Shallow branch:
  - subsets: `profiles0_1`, `profiles0_2`
  - x range: `0.5128870606422424-0.5242039561271667 m`
  - mean x: `0.5185455083847046 m`
  - cover-depth range: `0.096347875893116-0.09768731147050858 m`
  - mean cover depth: `0.09701759368181229 m`
  - diameter range: `17.518799751996994-17.556559294462204 mm`
  - length range: `0.1856800615787506-0.18713364005088806 m`
  - relative permittivity range: `1.9923940896987915-2.0307161808013916`
  - conductivity range: `0.002558577572926879-0.0025631326716393232 S/m`
- Deep branch:
  - subsets: `profiles1_3`, `profiles2_3`
  - x range: `0.4724560081958771-0.5013077855110168 m`
  - mean x: `0.48688189685344696 m`
  - cover-depth range: `0.138297438621521-0.16020938754081726 m`
  - mean cover depth: `0.14925341308116913 m`
  - diameter range: `17.418239265680313-17.55896955728531 mm`
  - length range: `0.18566444516181946-0.18643775582313538 m`
  - relative permittivity range: `2.0178639888763428-2.0728392601013184`
  - conductivity range: `0.002558391308411956-0.0025782580487430096 S/m`

## Current decision

The current product should report shallow and deep profile-subset candidates separately. The diameter and finite-length estimates are reasonably consistent across branches, while x and cover depth differ enough that a single x/y/z claim would hide real 3D ambiguity.

## What remains blocked

- The two-branch interpretation still needs either measured crossline profile coordinates, a y-dependent target model, or a multi-event model to select or merge branches.
- The current straight finite-length target model cannot yet represent a sloped/curved rebar trajectory.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_two_branch_depth_candidate_card.py`
- `python -m pytest tests/test_gssi51600s_two_branch_depth_candidate_card.py -q`
- Result: `2 passed`.
- Bundle/query focused validation passed before regeneration: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the two-branch card and bundled copy: both PNGs are nonblank RGBA images with size `1515 x 1141`.

## Artifact paths

- Two-branch card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/174_gssi51600s_two_branch_depth_candidate_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/175_gssi51600s_current_prediction_bundle_with_two_branch_depth_candidate`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Prototype a y-dependent target or two-event forward objective so the optimizer can test whether the two branches are one sloped/curved target or two nearby events.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
