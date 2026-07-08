# Advisor Optimizer Bundle Integrity Checkpoint

Date: 2026-07-01

## Scope

This checkpoint records an integrity audit for the advisor optimizer script
handoff folder and zip.

## Output

```text
advisor_optimizer_scripts_2026-07-01/
advisor_optimizer_scripts_2026-07-01.zip
outputs/_generated_checkpoints/team_reporting/321_advisor_optimizer_script_bundle_integrity_audit
```

## Result

```text
bundle files:             58
zip files:                58
matched files:            58
missing in zip:            0
extra zip files:           0
mismatched files:          0
root entrypoints:         17
inversion modules:        16
core modules:              9
gpu modules:               4
visualization modules:     5
source bytes:         644722
zip uncompressed bytes: 644722
zip archive bytes:    183205
audit ready:            true
```

## Decision

Use `advisor_optimizer_scripts_2026-07-01/` or
`advisor_optimizer_scripts_2026-07-01.zip` for advisor handoff. The folder and
zip contain the same source files by SHA-256.

## Validation

Focused test:

```text
tests/test_advisor_optimizer_script_bundle_integrity_audit.py
4 passed
```

Compile check:

```text
run_advisor_optimizer_script_bundle_integrity_audit.py: pass
tests/test_advisor_optimizer_script_bundle_integrity_audit.py: pass
```

Figure check:

```text
321 advisor optimizer bundle audit: 2429x808, dynamic range=255
```

## Marathon State

The requested 30-hour autonomous marathon is still active. This handoff audit
is a checkpoint, not a stop condition.
