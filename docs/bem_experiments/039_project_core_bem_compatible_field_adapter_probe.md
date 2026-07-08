# BEM Experiment 039: BEM-Compatible Field Adapter Probe

Date: 2026-06-25

## Purpose

Replace the project-core generated target-cell fields in the run `038` adapter
harness with BEM-compatible continuous analytic Green fields sampled at the
same project-grid target cells.

This is a CPU-only adapter probe. It uses the colleague-provided `scarep`
Green-function implementation as an analytic 2D TMz reference. It does not run
FDTD time stepping, field data, GPU work, FWI, 3D/HPC, neural networks, or the
historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/039_project_core_bem_compatible_field_adapter_probe
```

Key artifacts:

```text
data/project_core_bem_compatible_field_adapter_probe.csv
data/project_core_bem_compatible_field_adapter_probe_summary.json
figures/project_core_bem_compatible_field_adapter_probe.png
docs/PROJECT_CORE_BEM_COMPATIBLE_FIELD_ADAPTER_PROBE.md
```

## Result

```text
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
cases checked:                      3
best analytic variant:              analytic_receiver_conjugate_div_source
worst best-analytic L2:             0.8309901396143111
analytic field adapter ready:       false
project-grid best worst L2:         0.44601690298659386
uses colleague scarep Green:        true
gpu required:                       false
```

Best analytic metrics:

| epsr | Best analytic L2 |
| ---: | ---: |
| 1.25 | 0.8309901396143111 |
| 2.0 | 0.8309901396143111 |
| 4.0 | 0.8309901396143111 |

Comparison to the project-grid adapter:

| epsr | Project-grid best L2 | Best analytic/BEM-compatible L2 |
| ---: | ---: | ---: |
| 1.25 | 0.0989465314024021 | 0.8309901396143111 |
| 2.0 | 0.23018542478328735 | 0.8309901396143111 |
| 4.0 | 0.44601690298659386 | 0.8309901396143111 |

## Interpretation

Continuous analytic Green fields sampled at the project target cells improve
over the older analytic-cylinder transfer, but they still do not reproduce the
project-grid Born adapter across the contrast ladder.

The remaining adapter gap is not gross target geometry and not direct-wave
calibration. The active issue is the field-convention or finite-domain mapping
from BEM-compatible fields into the project-grid discrete scattering operator.

## Decision

Do not promote continuous analytic/BEM-compatible fields into the project-core
adapter yet. Continue with a bounded field-map calibration probe that tests
whether a low-dimensional analytic-field mixture can close the adapter gap
under held-out scan-position validation.

## Validation

```text
python -m py_compile run_project_core_bem_compatible_field_adapter_probe.py
python run_project_core_bem_compatible_field_adapter_probe.py
```

Figure check:

```text
project_core_bem_compatible_field_adapter_probe.png: 1852x805, dynamic range=255
```
