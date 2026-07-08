"""Archive numbered generated summary checkpoints outside summary_tables.

The project convention is that outputs/summary_tables is for weekly synthesized
report folders. Earlier generated audit/checkpoint folders used the same top
level. This utility preserves those folders, moves them into an explicit
archive, and writes an index that explains what each checkpoint was for.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


SUMMARY_ROOT = Path("outputs/summary_tables")
ARCHIVE_ROOT = Path("outputs/_generated_checkpoints")
NUMBERED_DIR_RE = re.compile(r"^(\d{3})_(.+)$")


@dataclass(frozen=True)
class CheckpointRecord:
    checkpoint_id: str
    name: str
    primary_category: str
    role: str
    related_tracks: str
    source_path: str
    archived_path: str
    tracked_before_move: bool
    file_count: int
    figure_count: int
    data_count: int
    doc_count: int
    summary_label: str
    note: str


def parse_git_tracked_paths() -> set[str]:
    """Return paths tracked by git, if git metadata is available."""
    git_index = Path(".git/index")
    if not git_index.exists():
        return set()
    import subprocess

    try:
        result = subprocess.run(
            ["git", "ls-files"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def classified_tracks(name: str) -> list[str]:
    lower = name.lower()
    tracks: list[str] = []
    if any(token in lower for token in ["local_2d", "synthetic", "detector", "close", "target", "source_factor"]):
        tracks.append("2d_fdtd")
    if any(token in lower for token in ["field", "gssi", "local_gssi"]):
        tracks.append("field")
    if "bem" in lower:
        tracks.append("bem")
    if not tracks:
        tracks.append("other")
    return tracks


def classify_category(name: str) -> str:
    lower = name.lower()
    tracks = classified_tracks(name)
    if "result_milestone_snapshot_audit" in lower:
        return "snapshot_audits"
    if any(token in lower for token in ["team_", "presentation", "storyboard", "delivery_checklist", "meeting_evidence"]):
        return "team_reporting"
    if "local_bem_field_2d" in lower or "bem_field_2d" in lower:
        return "cross_track"
    if "local_2d_field" in lower or len([t for t in tracks if t != "other"]) > 1:
        return "cross_track"
    if tracks == ["bem"]:
        return "bem"
    if tracks == ["field"]:
        return "field"
    if tracks == ["2d_fdtd"]:
        return "local_2d"
    return "legacy_mixed"


def classify_role(name: str) -> str:
    lower = name.lower()
    role_patterns = [
        ("snapshot_audit", ["result_milestone_snapshot_audit"]),
        ("holistic_report", ["holistic_report"]),
        ("presentation_pack", ["presentation_evidence_pack"]),
        ("storyboard", ["storyboard"]),
        ("team_brief", ["team_meeting", "team_presentation", "meeting_evidence_brief"]),
        ("delivery_checklist", ["delivery_checklist"]),
        ("handoff_scoreboard", ["handoff_readiness_scoreboard", "handoff_budget"]),
        ("table_pack", ["table_pack"]),
        ("evidence_audit", ["evidence_audit"]),
        ("design_contract", ["design_contract", "contract"]),
        ("command_plan", ["command_plan", "command_design"]),
        ("execution_audit", ["execution_audit"]),
        ("readiness_scorecard", ["readiness", "scorecard"]),
        ("policy_synthesis", ["policy", "synthesis"]),
        ("audit", ["audit"]),
        ("probe", ["probe"]),
        ("smoke", ["smoke"]),
    ]
    for role, patterns in role_patterns:
        if any(pattern in lower for pattern in patterns):
            return role
    return "other_checkpoint"


def first_summary_label(path: Path) -> str:
    data_dir = path / "data"
    if not data_dir.exists():
        return ""
    for summary_path in sorted(data_dir.glob("*summary*.json")):
        try:
            payload = json.loads(summary_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            for key in ["policy_label", "label", "run_kind", "experiment_label"]:
                value = payload.get(key)
                if value:
                    return str(value)
            summary = payload.get("summary")
            if isinstance(summary, dict):
                for key in ["policy_label", "label", "run_kind", "experiment_label"]:
                    value = summary.get(key)
                    if value:
                        return str(value)
    return ""


def build_record(path: Path, tracked_paths: set[str]) -> CheckpointRecord:
    match = NUMBERED_DIR_RE.match(path.name)
    if not match:
        raise ValueError(f"not a numbered checkpoint: {path}")
    checkpoint_id, name_tail = match.groups()
    category = classify_category(path.name)
    destination = ARCHIVE_ROOT / category / path.name
    files = [child for child in path.rglob("*") if child.is_file()]
    tracked_before = any(str(child) in tracked_paths for child in files)
    tracks = ",".join(classified_tracks(path.name))
    return CheckpointRecord(
        checkpoint_id=checkpoint_id,
        name=path.name,
        primary_category=category,
        role=classify_role(path.name),
        related_tracks=tracks,
        source_path=str(path),
        archived_path=str(destination),
        tracked_before_move=tracked_before,
        file_count=len(files),
        figure_count=sum(1 for child in files if child.suffix.lower() in {".png", ".pdf"}),
        data_count=sum(1 for child in files if child.suffix.lower() in {".csv", ".json", ".npy", ".npz"}),
        doc_count=sum(1 for child in files if child.suffix.lower() in {".md", ".ipynb"}),
        summary_label=first_summary_label(path),
        note=f"{name_tail.replace('_', ' ')}; archived from generated summary checkpoint stream.",
    )


def discover_records(tracked_paths: set[str]) -> list[CheckpointRecord]:
    records: list[CheckpointRecord] = []
    for path in sorted(SUMMARY_ROOT.iterdir(), key=lambda p: p.name):
        if path.is_dir() and NUMBERED_DIR_RE.match(path.name):
            records.append(build_record(path, tracked_paths))
    return sorted(records, key=lambda record: int(record.checkpoint_id))


def move_checkpoints(records: list[CheckpointRecord]) -> None:
    for record in records:
        source = Path(record.source_path)
        destination = Path(record.archived_path)
        if not source.exists():
            continue
        if destination.exists():
            raise FileExistsError(f"archive destination already exists: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))


def move_top_level_misc(tracked_paths: set[str]) -> list[dict[str, str]]:
    misc_records: list[dict[str, str]] = []
    for source in sorted(SUMMARY_ROOT.iterdir(), key=lambda p: p.name):
        if source.is_dir():
            continue
        if source.name == ".gitkeep":
            continue
        destination = ARCHIVE_ROOT / "legacy_misc" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise FileExistsError(f"archive destination already exists: {destination}")
        file_path = str(source)
        misc_records.append(
            {
                "name": source.name,
                "source_path": file_path,
                "archived_path": str(destination),
                "tracked_before_move": str(file_path in tracked_paths).lower(),
            }
        )
        shutil.move(str(source), str(destination))
    return misc_records


def write_index(records: list[CheckpointRecord], misc_records: list[dict[str, str]]) -> None:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    index_path = ARCHIVE_ROOT / "checkpoint_index.csv"
    fields = list(CheckpointRecord.__dataclass_fields__)
    with index_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: getattr(record, field) for field in fields})

    misc_path = ARCHIVE_ROOT / "legacy_misc_index.csv"
    with misc_path.open("w", newline="") as handle:
        fieldnames = ["name", "source_path", "archived_path", "tracked_before_move"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(misc_records)

    category_counts: dict[str, int] = {}
    role_counts: dict[str, int] = {}
    for record in records:
        category_counts[record.primary_category] = category_counts.get(record.primary_category, 0) + 1
        role_counts[record.role] = role_counts.get(record.role, 0) + 1

    readme = [
        "# Generated Checkpoint Archive",
        "",
        "This folder holds numbered generated checkpoint outputs that previously",
        "sat at the top level of `outputs/summary_tables`. They are preserved here",
        "so `outputs/summary_tables` can remain reserved for weekly synthesized",
        "report folders such as `wk00`, `wk01`, `wk02`, `wk03`, and `WK05`.",
        "",
        "Use `checkpoint_index.csv` to find the source, category, role, and related",
        "track for each archived checkpoint.",
        "",
        "## Category Counts",
        "",
        "| Category | Count | Meaning |",
        "| --- | ---: | --- |",
    ]
    category_meanings = {
        "local_2d": "Derived local 2D/FDTD detector, policy, audit, or design checkpoints.",
        "field": "Derived field-side GSSI/QC/provenance checkpoints.",
        "bem": "Derived BEM-only checkpoints.",
        "cross_track": "Checkpoints spanning more than one track, such as 2D-field or BEM-field-2D packs.",
        "snapshot_audits": "Script/test snapshot and milestone provenance audits.",
        "team_reporting": "Team brief, presentation, storyboard, or delivery checklist packs.",
        "legacy_mixed": "Older or ambiguous generated outputs that do not cleanly fit one track.",
    }
    for category, count in sorted(category_counts.items()):
        readme.append(f"| `{category}` | {count} | {category_meanings.get(category, 'Generated checkpoint archive category.')} |")
    readme.extend(
        [
            "",
            "## Role Counts",
            "",
            "| Role | Count |",
            "| --- | ---: |",
        ]
    )
    for role, count in sorted(role_counts.items()):
        readme.append(f"| `{role}` | {count} |")
    if misc_records:
        readme.extend(
            [
                "",
                "## Legacy Misc",
                "",
                "Non-directory top-level generated files were moved to `legacy_misc/`",
                "and indexed in `legacy_misc_index.csv`.",
            ]
        )
    readme.append("")
    (ARCHIVE_ROOT / "README.md").write_text("\n".join(readme))


def main() -> None:
    if not SUMMARY_ROOT.exists():
        raise FileNotFoundError(SUMMARY_ROOT)
    tracked_paths = parse_git_tracked_paths()
    records = discover_records(tracked_paths)
    write_index(records, [])
    move_checkpoints(records)
    misc_records = move_top_level_misc(tracked_paths)
    write_index(records, misc_records)
    remaining_numbered = [path.name for path in SUMMARY_ROOT.iterdir() if path.is_dir() and NUMBERED_DIR_RE.match(path.name)]
    if remaining_numbered:
        raise RuntimeError(f"numbered summary checkpoints still remain: {remaining_numbered[:5]}")
    print(json.dumps({"archived_checkpoints": len(records), "archived_misc": len(misc_records)}, indent=2))


if __name__ == "__main__":
    main()
