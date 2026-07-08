import numpy as np
from PIL import Image

from run_gssi_field_phase_anchor_qc import phase_quality_flag_counts, plot_phase_anchor_panel


def test_plot_phase_anchor_panel_handles_empty_picks(tmp_path):
    x_m = np.linspace(0.0, 1.0, 16)
    time_ns = np.linspace(0.0, 2.0, 32)
    data = np.sin(time_ns[:, None] * 3.0) * np.cos(x_m[None, :] * 2.0)
    processed = {"corrected": data}
    record = {"file": "empty.DZT"}
    path = tmp_path / "empty_panel.png"

    plot_phase_anchor_panel(record, processed, x_m, time_ns, [], path)

    with Image.open(path) as image:
        gray = np.asarray(image.convert("L"))
    assert gray.max() > gray.min()


def test_phase_quality_flag_counts_preserves_low_snr_count():
    rows = [
        {"phase_quality_flag": "low_snr"},
        {"phase_quality_flag": "usable"},
        {"phase_quality_flag": "low_snr"},
        {},
    ]

    assert phase_quality_flag_counts(rows) == {
        "low_snr": 2,
        "unknown": 1,
        "usable": 1,
    }
