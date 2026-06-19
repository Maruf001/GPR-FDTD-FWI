import base64

import pandas as pd

import run_local_2d_field_standalone_report as report


def test_decode_experiment_name_explains_close14_as_spacing_not_offset():
    decoded = report.decode_experiment_name(
        "local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
    )
    close14 = decoded[decoded["term"] == "close14"].iloc[0]["meaning"]

    assert "14 mm apart" in close14
    assert "not the transmitter-receiver offset" in close14


def test_decode_experiment_name_explains_local2d_and_seed():
    decoded = report.decode_experiment_name(
        "local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
    )
    terms = set(decoded["term"])

    assert "local2d" in terms
    assert "seed21" in terms
    assert "fixed_radius" in terms


def test_md_table_limits_rows_and_escapes_pipes():
    df = pd.DataFrame(
        [
            {"term": "a|b", "meaning": "first"},
            {"term": "c", "meaning": "second"},
        ]
    )
    table = report.md_table(df, [("term", "Term"), ("meaning", "Meaning")], max_rows=1)

    assert "a\\|b" in table
    assert "1 more rows omitted" in table


def test_attachment_image_cell_embeds_png(tmp_path):
    png_path = tmp_path / "tiny.png"
    png_path.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="))

    cell = report.attachment_image_cell(1, "Tiny", png_path, "A tiny image.")

    assert "Figure 1. Tiny" in cell["source"]
    assert "attachment:figure_01_tiny.png" in cell["source"]
    assert "figure_01_tiny.png" in cell["attachments"]
    assert "image/png" in cell["attachments"]["figure_01_tiny.png"]
