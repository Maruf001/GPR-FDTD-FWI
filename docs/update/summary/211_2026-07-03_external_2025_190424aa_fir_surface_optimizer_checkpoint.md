# External 2025 190424AA FIR+Surface Optimizer Checkpoint

## What Changed

- Added the completed `right_shift_fir_lowpass_surface_prune_w030` runs (`230/231`) to the 190424AA/LID10002 GGAE optimizer synthesis.
- Refreshed the optimizer synthesis as artifact `232_external_2025_190424aa_lid10002_ggae_optimizer_variant_synthesis`.
- Refreshed the 190424AA evidence pack as `233_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_fir_surface`.
- Refreshed the field-method leaderboard so the optimizer row points to evidence pack `233`.
- Updated the evidence-pack generator to resolve the latest optimizer synthesis rather than staying pinned to the old `195` synthesis.

## Key Numbers

- Best optimizer variant remains `right_shift_surface_prune_w030`.
- Best holdout mean: `0.6064098179340363`.
- Combined Fast-GPR-FWI-style FIR low-pass plus surface-prune holdout mean: `0.8541119694709778`.
- FIR+surface delta versus best surface-prune-only branch: `+0.24770215153694153`.
- Central FIR low-pass holdout mean: `0.6891225874423981`.
- Central FFT-box holdout mean: `0.6834719777107239`.
- Central FIR minus FFT-box delta: `+0.005650609731674194`.

## Current Decision

Decision string:

`external_2025_190424aa_lid10002_surface_prune_weight_ladder_w030_best_fir_validated_not_superior_right_fir_surface_not_superior`

Interpretation: the Fast-GPR-FWI-style FIR low-pass branch is implemented and validated as a field-data run, but on this 190424AA/LID10002 event crop it does not improve the best surface-prune-only optimizer. This remains provisional location/cover evidence only; diameter, concrete permittivity, and global profile transfer are not claimed from this branch.

## What Remains Blocked

- Diameter/material inference remains non-unique for this field crop.
- FIR acceleration/low-pass filtering is not yet a quality improvement on 190424AA, though it is methodologically wired and measured.
- Profile transfer is mixed: the surface-prune optimizer transfers to two profiles but fails LDH1 and slightly worsens LS1/LID10002.

## Validation

- `python -m py_compile run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py run_ggae2025_external_2025_190424aa_evidence_pack.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `16 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py run_ggae2025_external_2025_190424aa_evidence_pack.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py`
- Figure checks:
  - Optimizer figure: `2093x801`, nonwhite fraction `0.20635099579896843`, RGB std `60.68942603141598`.
  - Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/232_external_2025_190424aa_lid10002_ggae_optimizer_variant_synthesis`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/233_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_fir_surface`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue on real field data by testing the GGAE/Fast-GPR-FWI optimizer family on a new external profile from `data/2025-01-13_GPR_Dataset`, using the current best settings as the starting branch and keeping hyperbola-derived initialization as an initializer/sanity check rather than the final claim engine.

## Marathon Status

The requested real-field-data marathon is still active.
