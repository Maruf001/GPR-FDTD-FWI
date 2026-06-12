# Experiment 88: Report Dependency Archive

## Purpose

Create an explicit archive of the final report dependencies after run 554
showed the dependency set was small.

## 555: Report Dependency Archive

Output:

```text
outputs/experiments/555_report_dependency_archive
```

Command:

```text
tar -czf outputs/experiments/555_report_dependency_archive/report_dependency_archive.tar.gz -T outputs/experiments/555_report_dependency_archive/data/archive_file_list.txt
sha256sum outputs/experiments/555_report_dependency_archive/report_dependency_archive.tar.gz
tar -tzf outputs/experiments/555_report_dependency_archive/report_dependency_archive.tar.gz | wc -l
```

Artifacts:

```text
report_dependency_archive.tar.gz
README.md
data/archive_file_list.txt
data/report_dependency_archive.json
run_manifest.json
```

Result:

```text
input paths: 89
archive entries: 466
archive size: 4.0M
sha256: c5560c13846b501f0c3e67c8dd4b895baa90c2863036cbec27181b15703d5de0
```

## Interpretation

The final report dependency archive is small and reproducible from an explicit
file list. It remains under ignored `outputs/experiments/` and does not change
git tracking.

## Next Decision

Use the archive for external handoff if needed, or continue manuscript editing
and commit preparation.
