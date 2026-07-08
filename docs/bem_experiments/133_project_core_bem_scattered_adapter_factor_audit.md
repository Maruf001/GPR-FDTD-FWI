# BEM Experiment 133: Scattered Adapter Factor Audit

Date: 2026-06-27

## Purpose

Decompose the project-core BEM/FDTD scattered-field mismatch into simple adapter
factors.

Run `132` showed that the BEM 2D validation ladder is ready and the
project-core direct/background source-normalization check passes, but the
project-core rebar-scattered transfer still fails. This run asks:

```text
Can a simple sign, scale, receiver-order, time-shift, or observable transform
repair the scattered-field bridge?
```

This is a CPU-only audit of saved run `017` arrays. It does not rerun FDTD or
BEM solvers, compare against field data, launch GPU/HPC work, run 3D validation,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/133_project_core_bem_scattered_adapter_factor_audit
```

Key artifacts:

```text
data/project_core_bem_scattered_adapter_candidate_metrics.csv
data/project_core_bem_scattered_adapter_trace_shift_metrics.csv
data/project_core_bem_scattered_adapter_factor_audit_summary.json
figures/project_core_bem_scattered_adapter_factor_audit.png
docs/PROJECT_CORE_BEM_SCATTERED_ADAPTER_FACTOR_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate count:                         10
trace shift rows:                        14
scattered acceptance gate:               0.1
baseline symmetric L2:                   1.3943651626310445
best candidate:                          per_receiver_circular_shift_plus_scale
best candidate symmetric L2:             0.24094406788990988
best candidate relative L2 vs FDTD:      0.2374971503940242
best candidate passes gate:              false
best improvement factor:                 5.787090650715443
per-receiver circular shift span:        0.976482895414369 ns
per-receiver circular trace L2 mean:      0.23185951630814758
simple adapter fix ready:                false
project-core bridge ready:               false
project-core FDTD comparison ready:      false
real 3D validation ready:                false
field FWI ready:                         false
gpu/hpc ready:                           false
```

Candidate metrics:

| Candidate | Symmetric L2 | Relative L2 vs FDTD | Passes gate |
| --- | ---: | ---: | --- |
| source_normalized_baseline | 1.3943651626310445 | 1.4641925358593955 | false |
| sign_flip_only | 1.4369562087164727 | 1.5089164671824191 | false |
| global_real_scale_only | 1.9404541113579319 | 0.9995433937552558 | false |
| receiver_reverse_plus_scale | 1.9404541113579639 | 0.9995433937552562 | false |
| global_circular_shift_plus_scale | 1.4260425819216818 | 0.9454012103483397 | false |
| global_zero_padded_shift_plus_scale | 1.447851770475174 | 0.9499911536296816 | false |
| per_receiver_circular_shift_plus_scale | 0.24094406788990988 | 0.2374971503940242 | false |
| per_receiver_zero_padded_shift_plus_scale | 0.8178213407668117 | 0.7006646504836583 | false |
| time_derivative_plus_scale | 1.9725969048969079 | 0.9999048388750815 | false |
| time_integral_plus_scale | 1.9945307565543837 | 0.999996250683072 | false |

## Interpretation

The scattered-field bridge is not fixed by a simple sign flip, global amplitude
scale, receiver reversal, global time shift, time derivative, or time integral.

The largest improvement comes from allowing each receiver trace to use its own
circular time shift and scale. That reduces symmetric relative L2 from
`1.3943651626310445` to `0.24094406788990988`, a `5.787x` improvement, but it
still misses the `0.1` comparison gate.

The circular shifts range from `1.3246202755186227 ns` to
`2.3011031709329917 ns`, a span of `0.976482895414369 ns`. Because this is a
wrapped shift, it is diagnostic rather than a physically accepted adapter. It
points to frequency-domain phase convention, source time-origin alignment, and
causal reconstruction as the next likely source of mismatch.

## Decision

Keep the project-core BEM/FDTD bridge blocked. The next adapter branch should
focus on phase and time-origin reconstruction before older project archive
comparison, 3D validation, GPU/HPC, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_scattered_adapter_factor_audit.py
6 passed
```

Figure validation:

```text
project_core_bem_scattered_adapter_factor_audit.png
3003x874, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_scattered_adapter_factor_audit.py
sha256=a5799f637e64e2fd0f3ea446dc0cc5d58b06ecf941c2d2ef2a4bd2071b71df4f

tests/test_project_core_bem_scattered_adapter_factor_audit.py
sha256=3562a4d65d3ebc5163add8d29385903dc43d6e9dba0bd74d34325becb1d387fa
```
