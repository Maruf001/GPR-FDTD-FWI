from run_close50_linear_sub30_bracket_policy import summarize_bracket_policy


def _row(seed, offset, *, x_ambiguous=False):
    return {
        "seed_label": seed,
        "tx_rx_offset_mm": offset,
        "truth_geometry_match": True,
        "strong_confidence": True,
        "strict_clean_row": not x_ambiguous,
        "x_ambiguity_width_mm": 1.0 if x_ambiguous else 0.0,
        "radius_ambiguity_width_mm": 0.0,
        "radius_margin_abs": 0.0015,
    }


def test_bracket_policy_flags_persistent_seed13_x_ambiguity():
    confidence_rows = [
        _row("seed21", 29.5),
        _row("seed21", 29.5),
        _row("seed13", 29.5, x_ambiguous=True),
        _row("seed13", 29.5),
        _row("seed13", 29.75, x_ambiguous=True),
        _row("seed13", 29.75),
    ]

    summary = summarize_bracket_policy(
        [{"seed_label": "seed21"}, {"seed_label": "seed13"}, {"seed_label": "seed13"}],
        confidence_rows,
        [{"objective_label": "highband", "truth_geometry_match": True}],
    )

    assert summary["policy_label"] == "close50_linear_sub30_seed13_x_ambiguity_persists"
    assert summary["tested_offsets_mm"] == "29.5,29.75"
    assert summary["seed13_x_ambiguous_offsets_mm"] == "29.5,29.75"
    assert summary["truth_geometry_row_count"] == 6
    assert summary["strong_confidence_row_count"] == 6
    assert summary["x_ambiguity_row_count"] == 2


def test_bracket_policy_can_still_report_clean_candidate():
    confidence_rows = [
        _row("seed21", 29.5),
        _row("seed21", 29.5),
        _row("seed13", 29.5),
        _row("seed13", 29.5),
    ]

    summary = summarize_bracket_policy(
        [{"seed_label": "seed21"}, {"seed_label": "seed13"}],
        confidence_rows,
        [],
    )

    assert summary["policy_label"] == "close50_linear_sub30_clean_candidate"
    assert summary["x_ambiguity_row_count"] == 0
