import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_existing_wavefield_animation_backfill import (  # noqa: E402
    backfill_existing_wavefield_inventories,
    discover_wavefield_entries,
    is_true_wavefield_gif,
)


def _write_test_gif(path):
    frame1 = Image.fromarray(np.zeros((14, 18), dtype=np.uint8))
    frame2_array = np.zeros((14, 18), dtype=np.uint8)
    frame2_array[3:11, 5:13] = 255
    frame2 = Image.fromarray(frame2_array)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame1.save(path, save_all=True, append_images=[frame2], duration=80, loop=0)


def test_is_true_wavefield_gif_excludes_schematic():
    assert is_true_wavefield_gif("true_nominal_wavefield.gif")
    assert not is_true_wavefield_gif("geometric_wave_propagation.gif")
    assert not is_true_wavefield_gif("source_pulse_noise_context.png")


def test_discover_wavefield_entries_validates_existing_gif(tmp_path):
    run_dir = tmp_path / "001_demo"
    gif_path = run_dir / "figures" / "true_nominal_wavefield.gif"
    _write_test_gif(gif_path)
    summary_path = run_dir / "data" / "true_nominal_wavefield_animation_summary.json"
    summary_path.parent.mkdir(parents=True)
    summary_path.write_text(json.dumps({"backend": "cpu"}), encoding="utf-8")

    entries = discover_wavefield_entries(run_dir)

    assert len(entries) == 1
    assert entries[0]["summary_present"]
    assert entries[0]["validation"]["frame_count"] == 2


def test_backfill_existing_wavefield_inventories_writes_audit_and_notes(tmp_path):
    root = tmp_path / "experiments"
    root.mkdir()
    empty_run = root / "002_no_wavefield"
    empty_run.mkdir()
    run_dir = root / "001_demo"
    _write_test_gif(run_dir / "figures" / "true_nominal_wavefield.gif")

    result = backfill_existing_wavefield_inventories(
        root,
        audit_json=root / "wavefield_audit.json",
        audit_csv=root / "wavefield_audit.csv",
    )

    assert result["counts"] == {"skipped": 1, "generated": 1}
    assert (run_dir / "data" / "existing_true_wavefield_animations_summary.json").exists()
    assert "existing_true_wavefield_animations:start" in (
        run_dir / "figures" / "FIGURE_NOTES.md"
    ).read_text(encoding="utf-8")
    assert (root / "wavefield_audit.csv").exists()

    second = backfill_existing_wavefield_inventories(root)

    assert second["counts"] == {"skipped": 2}
    row = next(item for item in second["rows"] if item["run_number"] == 1)
    assert row["reason"] == "existing true wavefield inventory"
