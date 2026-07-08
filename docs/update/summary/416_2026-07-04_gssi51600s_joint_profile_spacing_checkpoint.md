# 2026-07-04 GSSI 51600S Joint Profile-Spacing Checkpoint

## What changed

- Added a joint profile-spacing estimator for the trusted GSSI 51600S rebar path.
- The estimator combines common spacing rows from both profile subsets after subtracting each subset's own best field loss, so absolute loss differences between subsets do not dominate the spacing estimate.
- Wired the joint spacing result into the live field-prediction query and the current GSSI prediction bundle.

## Key numbers

- Joint spacing card artifact: `114_gssi51600s_joint_profile_spacing_card_current`
- Current bundle with joint spacing context: `115_gssi51600s_current_prediction_bundle_with_joint_spacing_context`
- Common spacings tested across both subsets: `0.16 m`, `0.22 m`, `0.28 m`
- MAP joint spacing: `0.22 m`
- Weighted joint spacing: `0.2393190257 m`
- 90% spacing interval: `0.16-0.28 m`
- Weighted length: `0.1853032158 m`
- 90% mean-length interval: `0.1833631247-0.1996676922 m`
- Weighted diameter: `17.30561034 mm`
- 90% diameter interval: `17.30550267-17.30563678 mm`
- Weighted relative permittivity: `2.041882165`
- Weighted conductivity: `0.0026601072 S/m`
- Short-only branch weight: `0.8822427552`
- Contains-long branch weight: `0.1177572448`
- Max posterior weight: `0.4425017495`
- Effective sample size: `2.481101948`

## Current decision

The joint estimator is stronger than the single-subset spacing posterior: common spacings of `0.22 m` and `0.28 m` keep both subsets on the short-length branch, while `0.16 m` is the only common spacing that still contains the long branch. This supports a short finite-length interpretation under the joint normalized evidence, but the spacing interval still includes `0.16 m`, so the product state remains geometry-conditioned.

## What remains blocked

- The actual crossline profile coordinates are still not present in the local GSSI metadata.
- The current result is an optimizer-based geometry estimate, not measured survey geometry.
- A release-style single finite-length claim still needs measured crossline spacing or an explicit profile-position optimizer that can be validated against acquisition metadata.

## Next defensible task

Use the joint profile-spacing card as the current strongest geometry-conditioned product estimate, then work on a bounded profile-position optimizer or measured-geometry intake path to turn the spacing estimate into a release-ready geometry field.

## Validation/resource checks

- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_current_prediction_bundle.py run_gssi51600s_profile_spacing_posterior_card.py run_gssi51600s_joint_profile_spacing_card.py`
- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_profile_spacing_posterior_card.py tests/test_gssi51600s_joint_profile_spacing_card.py -q`
- Broader focused validation is pending after this checkpoint.
- The local marathon request remains active.
