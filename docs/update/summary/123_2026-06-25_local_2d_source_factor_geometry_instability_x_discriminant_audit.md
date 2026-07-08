# Local 2D Source-Factor Geometry-Instability X Discriminant Audit

Date: 2026-06-25

## Scope

This checkpoint records run `222`, a read-only audit over the run `220`
x-envelope candidate tables.

It did not run new FDTD, optimizer commands, GPU work, field transfer, field
FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/222_local_2d_source_factor_geometry_instability_x_discriminant_audit
```

Tracked note:

```text
docs/experiments/905_local_2d_source_factor_geometry_instability_x_discriminant_audit.md
```

## Result

```text
candidate rows audited:                 10
discriminant rows:                      4
promotion blockers:                     3
amplitude update best x:                190.0
amplitude update truth x selected:      true
geometry update best x:                 188.0
geometry update truth x selected:       false
geometry truth-minus-best abs:          0.018938287611807936
geometry truth-minus-best rel:          0.026048467309042034
geometry misfit increases with x:       true
full batch ready:                       false
GPU work ready:                         false
field transfer ready:                   false
```

## Decision

The x-envelope branch is now explained. Missing truth x was not the whole
problem: the geometry-instability family prefers lower x in both nominal and
time-shift rows. The source-factor branch remains blocked from full batch,
GPU work, field transfer, and claims.

The next defensible local 2D branch is a geometry-instability objective/source
discriminant design.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
sha256: 2458327294b1693c9dbec48d7e0a97fbddf225e548cdba37eb8a32005bcd553f

test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
sha256: 3e44fb4e6b60f34fd134a1782ab07c2485f84696f689249f5d779fd899408d37
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_x_discriminant_audit.py tests/test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
pass
```

Figure check:

```text
1492x808, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then design the next bounded
geometry-instability discriminant branch.
