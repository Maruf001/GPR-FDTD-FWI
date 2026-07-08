# Discrete Born Scattering Operator Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the continuation after the BEM target-scattering
blocker was narrowed to the discrete scattering/operator level.

No field FWI, heavy GPU queue, field 3D/HPC work, neural-network training, or
historical `outputs/experiments` archive comparison was launched.

## Runs Added

```text
035_project_core_discrete_born_scattering_audit
036_project_core_discrete_born_strength_ladder
037_project_core_bem_scattering_adapter_contract
```

Tracked notes:

```text
docs/bem_experiments/035_project_core_discrete_born_scattering_audit.md
docs/bem_experiments/036_project_core_discrete_born_strength_ladder.md
docs/bem_experiments/037_project_core_bem_scattering_adapter_contract.md
```

## Result

Run `035` built a grid-aware first-order Born-style surrogate from project-core
background fields at the actual rasterized target cells.

```text
cylinder epsr:                     1.25
target cell count:                 533
legacy analytic scattered L2:      1.5472037658996989
best Born variant:                 product_div_source
best Born scattered L2:            0.0989465314024021
discrete Born scattering ready:    true
```

Run `036` extended the surrogate across the same in-range target-strength
ladder that previously failed under the analytic-cylinder bridge.

| epsr | Analytic scattered L2 | Best Born L2 | Best Born variant | Ready |
| ---: | ---: | ---: | --- | --- |
| 1.25 | 1.5472037658996989 | 0.0989465314024021 | product_div_source | true |
| 2.0 | 1.6313894289625301 | 0.23018542478328735 | product_div_source | true |
| 4.0 | 1.5415158197729195 | 0.44601690298659386 | receiver_conjugate_div_source | true |

```text
worst Born scattered L2:           0.44601690298659386
ready epsr count:                  3 / 3
all discrete Born ready:           true
```

## Interpretation

This changes the BEM/project-core bridge diagnosis.

Previous state:

```text
Direct-wave calibration:           solved well enough by empirical surface
Gross target rasterization:        cleared by run 034
Analytic cylinder target transfer: failed around 1.5 scattered L2
```

New state:

```text
Project-grid-aware scattering:     passes through epsr 4.0
```

The project-core FDTD target physics are not the blocker. The blocker is the
continuous analytic-cylinder/BEM representation crossing into the project-core
discrete grid without a grid-aware scattering/operator adapter.

## Decision

Use runs `035`-`036` as the current positive BEM/project-core bridge result.

Run `037` converts that result into the current implementation target:

```text
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
epsr values passed:                 [1.25, 2.0, 4.0]
worst discrete Born L2:             0.44601690298659386
adapter contract ready:             true
```

The adapter contract requires:

```text
project_grid_target_cells
target_cell_weights
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
scattering_formula_variants
per_frequency_complex_scale
```

The next BEM-side work should be:

```text
Implement the BEM-to-project-grid scattering adapter specified by run 037.
```

That means translating continuous BEM target fields/surface quantities into a
project-grid-aware target-cell scattering operator, or using the discrete Born
operator as the adapter layer before returning to continuous BEM claims.

Do not return to direct-wave-only calibration unless new evidence appears. Do
not compare against the historical synthetic 2D archive, field data, or 3D
inversion yet.

## Field And 2D Guardrails

Field state remains unchanged:

```text
current field intake: run 164
field FWI ready:     false
field GPU/HPC ready: false
```

Synthetic 2D state remains unchanged:

```text
fixed-radius result: single-branch mechanism only
new GPU probe ready: false
```

## Validation

```text
python -m py_compile \
  run_project_core_discrete_born_scattering_audit.py \
  run_project_core_discrete_born_strength_ladder.py

python run_project_core_discrete_born_scattering_audit.py
python run_project_core_discrete_born_strength_ladder.py
python run_project_core_bem_scattering_adapter_contract.py
```

Figure checks:

```text
outputs/bem_experiments/035_project_core_discrete_born_scattering_audit/figures/project_core_discrete_born_scattering_audit.png
outputs/bem_experiments/036_project_core_discrete_born_strength_ladder/figures/project_core_discrete_born_strength_ladder.png
outputs/bem_experiments/037_project_core_bem_scattering_adapter_contract/figures/project_core_bem_scattering_adapter_contract.png
```
