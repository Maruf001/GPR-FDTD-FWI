"""Tests for detector assignment reporting."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_detection_assignment_report import (  # noqa: E402
    assign_ranked_candidates,
    load_candidates_csv,
)


def test_load_candidates_csv_and_assign_rejects_duplicate_x(tmp_path):
    csv_path = tmp_path / "candidates.csv"
    csv_path.write_text(
        "\n".join([
            "rank,x_mm,z_mm,score,normalized_score,support_fraction,time_offset_ps",
            "1,148,85,10,1.0,1.0,350",
            "2,252,105,9,0.9,1.0,350",
            "3,252,65,8.5,0.85,1.0,750",
            "4,352,120,7,0.7,1.0,450",
        ]) + "\n",
        encoding="utf-8",
    )

    rows = load_candidates_csv(csv_path)
    assigned = assign_ranked_candidates(rows, count=3, min_x_separation_mm=45.0)

    assert [row["rank"] for row in assigned] == [1, 2, 4]
    assert [row["x_mm"] for row in assigned] == [148.0, 252.0, 352.0]
