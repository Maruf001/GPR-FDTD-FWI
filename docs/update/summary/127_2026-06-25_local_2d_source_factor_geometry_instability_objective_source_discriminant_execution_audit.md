# Local 2D Source-Factor Geometry-Instability Objective/Source Discriminant Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records run `226`, the bounded CPU execution audit for the
geometry-instability objective/source discriminants designed in run `224`.

This did not launch broad source-factor batch execution, GPU work, field
transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/226_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit
```

Tracked note:

```text
docs/experiments/907_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.md
```

## Result

```text
commands in design:                 3
complete optimizer outputs:         2
usable evidence rows:               2
nonzero exits:                      1
required artifacts present:         12 / 18
candidate CSV count:                2
figure file count:                  8
truth x selected count:             0
truth xyz selected count:           0
matched nominal best x:             188.0
time-grid best x:                   188.0
time-grid best source time ps:      -50.0
geometry discriminant evidence ready: false
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

## Decision

The two completed discriminants still select `x=188`, so source timing alone
does not explain the lower-x geometry-instability preference.

The highband command failed because the optimizer requires `base` as the first
diagnostic objective variant. The next useful local 2D task is a corrected
highband-plus-base design. Full batch, GPU work, field transfer, and claims
remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
sha256: cbb9be1a87112710516cb76316bd96296dac19657896e9814df99edf03722778

test_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
sha256: f245dd04a2fd6a82949ec44e04af4b31a0699a0553dc62fd81fccbe37a3a9f4b
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_execution_audit.py
pass
```

Figure check:

```text
2032x770, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then a corrected highband/base
command design.
