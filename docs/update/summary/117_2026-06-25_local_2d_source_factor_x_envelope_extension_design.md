# Local 2D Source-Factor X-Envelope Extension Design

Date: 2026-06-25

## Scope

This checkpoint records summary run `216`, a design contract for the next
bounded local 2D source-factor branch after run `194`.

No FDTD execution, GPU work, field transfer, field FWI, or neural-network
training was started.

## Output

```text
outputs/summary_tables/216_local_2d_source_factor_x_envelope_extension_design
docs/experiments/902_local_2d_source_factor_x_envelope_extension_design.md
```

## Result

```text
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

## Decision

The next defensible local 2D source-factor branch is a small CPU x-envelope
extension over the two update cases. Do not promote this branch to full-batch
source-factor robustness, GPU work, or field transfer from the current
evidence.

## Milestone Snapshot

Frozen scripts:

```text
run_local_2d_source_factor_x_envelope_extension_design.py
sha256: 9387562e81126cd80f16aae8ef5e7d4260534a1b1ed2b7cc667a3533a9ed5ae4

test_local_2d_source_factor_x_envelope_extension_design.py
sha256: b6805a804c87e93b695858ad9283c76a8bf002d645ad391ce0a61599a76554fc
```

## Validation

Focused test:

```text
tests/test_local_2d_source_factor_x_envelope_extension_design.py
3 passed
```

Figure check:

```text
1852x732, dynamic range=255
```
