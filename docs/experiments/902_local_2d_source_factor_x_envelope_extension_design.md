# Experiment 902: Local 2D Source-Factor X-Envelope Extension Design

Date: 2026-06-25

## Purpose

Define the smallest defensible next local 2D source-factor CPU branch after run
`194` showed that target-0 truth x was outside the tested envelope.

This is a design contract. It does not run FDTD, GPU work, field transfer,
field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/216_local_2d_source_factor_x_envelope_extension_design
```

Key artifacts:

```text
data/local_2d_source_factor_x_envelope_extension_design_rows.csv
data/local_2d_source_factor_x_envelope_extension_design_gates.csv
data/local_2d_source_factor_x_envelope_extension_design_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_X_ENVELOPE_EXTENSION_DESIGN.md
figures/local_2d_source_factor_x_envelope_extension_design.png
scripts/run_local_2d_source_factor_x_envelope_extension_design.py
scripts/test_local_2d_source_factor_x_envelope_extension_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                         194
source truth x in candidate set:    false
source update z/r support:          2 / 2
design rows:                        2
candidate evaluations:              5
all designs include truth x:        true
all designs fix truth z/radius:     true
small CPU execution ready:          true
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

Designed rows:

| Family | Case | X candidates mm | Z mm | Radius mm | Candidate evals |
| --- | --- | --- | --- | --- | ---: |
| `max_amplitude_stress` | `ff_max_amplitude_stress_time_shift_only` | `189.0;190.0` | `90.0` | `5.0` | 2 |
| `max_geometry_instability` | `ff_max_geometry_instability_time_shift_only` | `188.0;189.0;190.0` | `90.0` | `5.0` | 3 |

## Interpretation

Run `194` blocked broad promotion because the current x/z/radius evidence is
case-label-dependent and truth x was outside the tested envelope. This design
does not reopen a broad GPU or full-batch path. It only defines a smaller
CPU-side question:

```text
If truth x is included while the update-case-supported truth z/radius are
fixed, do the two update cases select truth x?
```

## Decision

If another local 2D source-factor run is desired, run this small CPU
x-envelope extension. Do not promote to full batch, GPU work, or field transfer
from the current evidence.

## Milestone Snapshot

This is a result-driven local 2D design milestone. It froze:

```text
run_local_2d_source_factor_x_envelope_extension_design.py
sha256: 9387562e81126cd80f16aae8ef5e7d4260534a1b1ed2b7cc667a3533a9ed5ae4

test_local_2d_source_factor_x_envelope_extension_design.py
sha256: b6805a804c87e93b695858ad9283c76a8bf002d645ad391ce0a61599a76554fc
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_x_envelope_extension_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_x_envelope_extension_design.png
1852x732, dynamic range=255
```
