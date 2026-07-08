# 2026-07-04 GSSI 51600S Profile-Spacing Posterior Checkpoint

## What changed

- Added a bounded posterior-style profile-spacing card for the trusted GSSI 51600S rebar path.
- The card treats crossline spacing as a nuisance parameter over the explicit spacing scan rows, using a softmin likelihood over the field-L1 loss.
- Wired the posterior numbers into the live field-prediction query and the current GSSI prediction bundle.

## Key numbers

- Posterior card artifact: `112_gssi51600s_profile_spacing_posterior_card_current`
- Current bundle with posterior context: `113_gssi51600s_current_prediction_bundle_with_spacing_posterior_context`
- MAP spacing: `0.22 m`
- Weighted spacing: `0.2340056283 m`
- 90% spacing interval: `0.16-0.28 m`
- MAP length: `0.1835240722 m`
- Weighted length: `0.1922146363 m`
- 90% length interval: `0.1835240722-0.2173339278 m`
- MAP diameter: `17.31610671 mm`
- Weighted diameter: `17.31603134 mm`
- 90% diameter interval: `17.31560007-17.31611229 mm`
- Weighted relative permittivity for the spacing scan: `2.104939578`
- Weighted conductivity for the spacing scan: `0.0026602904 S/m`
- Short-branch posterior weight: `0.7414716898`
- Long-branch posterior weight: `0.2585283102`
- Max single spacing weight: `0.1867722706`
- Effective sample size: `5.6674535174`

## Current decision

The posterior quantifies the geometry ambiguity instead of hiding it. It supports reporting a MAP spacing and weighted estimates, but the posterior remains broad, so the product-facing state remains geometry-conditioned rather than release-promoted to a single finite length.

## What remains blocked

- A measured crossline spacing or explicit acquisition grid is still needed to collapse the 0.16-0.28 m spacing interval.
- The current field loss is too flat across the tested 0.20-0.28 m region to claim a unique crossline spacing from data alone.

## Next defensible task

Use the posterior output as the product-facing uncertainty layer, then start a bounded geometry-estimation branch that can jointly fit profile positions with the rebar geometry instead of only scoring fixed spacing rows.

## Validation/resource checks

- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_current_prediction_bundle.py run_gssi51600s_profile_spacing_posterior_card.py`
- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_profile_spacing_posterior_card.py -q`
- Broader focused validation is pending after this checkpoint.
- The local marathon request remains active.
