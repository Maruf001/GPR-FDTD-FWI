# 448 - 2026-07-05 - GSSI 51600S Depth-Slope Gate Checkpoint

## Purpose

Test whether a y-dependent cover-depth slope can explain the current GSSI 51600S shallow/deep profile-subset ambiguity and promote a single tilted 3D finite-length rebar interpretation.

## What Changed

- Added optional bounded crossline depth-slope optimization to `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`.
  - Default behavior is unchanged: slope is zero unless `--optimize-depth-slope` is enabled.
  - New reported fields include best/final depth slope, depth-slope gradient, and slope prior settings.
- Added `run_gssi51600s_depth_slope_candidate_card.py`.
  - Compares fixed-depth vs depth-slope GSSI runs for profiles 0-2 and profiles 1-3.
  - Packages the result as a release gate rather than a hidden diagnostic.
- Integrated the depth-slope gate into:
  - `run_gssi51600s_current_prediction_bundle.py`
  - `run_field_prediction_current_query.py`

## Field Runs

- Profiles 1-3 slope branch:
  - Artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/514_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_prior_depth_slope_windows50_54_58_62_66_iter24`
  - Best field L1: `0.9437721371650696`
  - Best objective: `0.9512885212898254`
  - Best x: `0.49859556555747986` m
  - Best cover depth: `0.12993820011615753` m
  - Best diameter: `17.26720854640007` mm
  - Best length: `0.1835247129201889` m
  - Best background epsr: `2.246645927429199`
  - Best conductivity: `0.0026639688294380903` S/m
  - Best depth slope: `-0.0010108649730682373` m/m
- Profiles 0-2 slope branch:
  - Artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/515_gssi51600s_finite_length_3d_profiles0_2_uniform_y022_domainz070_adamw_prior_depth_slope_windows50_54_58_62_66_iter24`
  - Best field L1: `0.9227229356765747`
  - Best objective: `0.9283937215805054`
  - Best x: `0.4787594676017761` m
  - Best cover depth: `0.15202726423740387` m
  - Best diameter: `17.271336168050766` mm
  - Best length: `0.18352967500686646` m
  - Best background epsr: `2.2292699813842773`
  - Best conductivity: `0.0026332673151046038` S/m
  - Best depth slope: `0.00047791004180908203` m/m

## Interpretation

- The depth-slope parameter did not identify a meaningful tilted-bar geometry:
  - Maximum absolute fitted slope was only `0.0010108649730682373` m/m.
  - Profiles 1-3 improved field L1 versus the fixed-depth reference by about `-0.01454`.
  - Profiles 0-2 worsened field L1 versus the fixed-depth reference by about `+0.01575`.
- The objective improved in both slope runs, but the field waveform fit did not improve consistently.
- The current product action is therefore to keep the two conditioned depth candidates and not promote a tilted single-bar 3D interpretation from the slope test.

## Product Artifacts

- Depth-slope card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/176_gssi51600s_depth_slope_candidate_card_current`
  - Decision: `depth_slope_does_not_resolve_branch_ambiguity`
- Updated current bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/177_gssi51600s_current_prediction_bundle_with_depth_slope_gate`
  - Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Current query now reports:
  - `two_branch_depth_candidate_decision: two_depth_branch_candidate_report_conditioned`
  - `depth_slope_candidate_decision: depth_slope_does_not_resolve_branch_ambiguity`

## Validation

- `python -m py_compile run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py run_gssi51600s_depth_slope_candidate_card.py run_gssi51600s_current_prediction_bundle.py run_field_prediction_current_query.py`
- `python -m pytest ... -q`
- Result: `67 passed`.
- `git diff --check` passed on the touched files.
- Depth-slope figure sanity: size `(1719, 1192)`, nonblank RGBA.

## Next Defensible Task

Continue on the trusted GSSI 51600S predictor by testing a y-dependent multi-event or per-profile target model, or by bringing in measured crossline profile coordinates if available. The two-depth candidate should remain conditioned until that evidence selects a branch.
