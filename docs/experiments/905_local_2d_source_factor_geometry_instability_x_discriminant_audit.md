# Experiment 905: Local 2D Source-Factor Geometry-Instability X Discriminant Audit

Date: 2026-06-25

## Purpose

Explain why the run `220` x-envelope execution did not resolve the
geometry-instability update case.

This is a read-only audit over completed candidate tables. It does not run new
FDTD, optimizer commands, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/222_local_2d_source_factor_geometry_instability_x_discriminant_audit
```

Key artifacts:

```text
data/local_2d_source_factor_geometry_instability_x_discriminant_candidates.csv
data/local_2d_source_factor_geometry_instability_x_discriminant_rows.csv
data/local_2d_source_factor_geometry_instability_x_discriminant_gates.csv
data/local_2d_source_factor_geometry_instability_x_discriminant_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_X_DISCRIMINANT_AUDIT.md
figures/local_2d_source_factor_geometry_instability_x_discriminant_audit.png
scripts/run_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
scripts/test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                             220
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

Discriminants:

| Family | Case | Best x | Truth x selected | Truth minus best | Increasing with x |
| --- | --- | ---: | --- | ---: | --- |
| `max_amplitude_stress` | `ff_max_amplitude_stress_nominal` | 190.0 | true | 0.0 | false |
| `max_amplitude_stress` | `ff_max_amplitude_stress_time_shift_only` | 190.0 | true | 0.0 | false |
| `max_geometry_instability` | `ff_max_geometry_instability_nominal` | 188.0 | false | 0.04021999139862342 | true |
| `max_geometry_instability` | `ff_max_geometry_instability_time_shift_only` | 188.0 | false | 0.018938287611807936 | true |

## Interpretation

The geometry-instability failure is not just an x-envelope problem. Truth
`x=190` is present, z/radius are fixed to truth, and the update case still
prefers `x=188`. The nominal geometry-instability row also prefers `x=188`, so
the issue is not isolated to the time shift. Under the current source/noise and
objective settings, this family has a persistent lower-x preference.

## Decision

Do not promote the source-factor branch to full batch execution, GPU work,
field transfer, or source-factor claims.

The next useful local 2D task is a geometry-instability objective/source
discriminant design: test what part of the objective, source/noise profile, or
scene setup causes the lower-x preference.

## Milestone Snapshot

This is a result-driven local 2D discriminant milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
sha256: 2458327294b1693c9dbec48d7e0a97fbddf225e548cdba37eb8a32005bcd553f

test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
sha256: 3e44fb4e6b60f34fd134a1782ab07c2485f84696f689249f5d779fd899408d37
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_x_discriminant_audit.py
3 passed
```

Figure check:

```text
local_2d_source_factor_geometry_instability_x_discriminant_audit.png
1492x808, dynamic range=255
```
