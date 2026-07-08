# Field Experiment 242: Controlled Archive Real Return Populated Synthetic Smoke

Date: 2026-06-28

## Purpose

Run a positive synthetic smoke test against the empty real-return archive
skeleton from runs `239`-`241`. The goal is to prove that the archive paths,
DZT extension checks, minimum-size checks, GSSI header-prefix checks, staged
SHA-256 checks, completed worksheet signoff fields, and provenance table
mechanics can pass when files are present.

This run creates deterministic synthetic DZT-like files only. It does not
contain real measured field files, accept a real archive, promote field
evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/242_gssi51600s_controlled_archive_real_return_populated_synthetic_smoke
```

Key artifacts:

```text
data/field_controlled_archive_real_return_populated_synthetic_files.csv
data/field_controlled_archive_real_return_populated_synthetic_signoff.csv
data/field_controlled_archive_real_return_populated_synthetic_provenance.csv
data/field_controlled_archive_real_return_populated_synthetic_checks.csv
data/field_controlled_archive_real_return_populated_synthetic_smoke_summary.json
figures/field_controlled_archive_real_return_populated_synthetic_smoke.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_POPULATED_SYNTHETIC_SMOKE.md
synthetic_archive_root/
```

## Result

```text
synthetic file count:              9
controlled profile files:          3
time-zero reference files:         3
amplitude reference files:         3
archive checks passed:             45 / 45
completed signoff cells:           27 / 27
synthetic provenance rows ready:   6 / 6
synthetic archive smoke ready:     true
synthetic checksum smoke ready:    true
real files present:                false
real signoff values present:       false
real provenance values present:    false
real archive acceptance ready:     false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The smoke creates nine synthetic DZT-like files under the synthetic archive
root, one for each required real-return slot. Each file passes five checks:
existence, `.DZT` extension, minimum size, `ff07` GSSI header prefix, and
staged SHA-256 agreement with the completed worksheet row.

## Interpretation

The empty archive skeleton is mechanically usable. A populated archive with the
right shape can pass deterministic file, checksum, signoff, and provenance
plumbing. This is not field evidence because the files and values are
synthetic.

The real blocker is unchanged: real measured GSSI files, real operator signoff
values, real provenance values, checksum intake on staged real files, and
controlled-evidence acceptance are still required before any field evidence or
field FWI claim.

## Decision

Use run `242` as the positive-control smoke for future real-return archive
intake. Keep real archive acceptance, controlled field evidence, field FWI,
field 3D/HPC, and GPU escalation blocked until real files pass the same path.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_populated_synthetic_smoke.py
6 passed
```

Figure validation:

```text
3041x840, dynamic range=255
```
