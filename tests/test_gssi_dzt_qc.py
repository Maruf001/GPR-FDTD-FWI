from pathlib import Path

import numpy as np
import pytest

from run_gssi_dzt_qc import (
    background_removed_profile,
    build_profile_record,
    depth_from_time_m,
    field_dataset_output_root,
    parse_dzx_metadata,
    parse_scan_range,
)


def test_parse_scan_range_counts_inclusive_endpoints():
    parsed = parse_scan_range("0,806")

    assert parsed["start"] == 0
    assert parsed["end"] == 806
    assert parsed["trace_count"] == 807


def test_field_dataset_output_root_uses_dataset_family():
    root = field_dataset_output_root(
        "outputs/field_experiments",
        "local_gssi_51600s_2026_06_09",
    )

    assert root == Path("outputs/field_experiments/local_gssi_51600s_2026_06_09")


@pytest.mark.parametrize("dataset_id", ["", "../bad", "public/../bad", "/tmp/bad"])
def test_field_dataset_output_root_rejects_unsafe_dataset_id(dataset_id):
    with pytest.raises(ValueError):
        field_dataset_output_root("outputs/field_experiments", dataset_id)


def test_parse_dzx_metadata_handles_default_namespace(tmp_path):
    dzx = tmp_path / "profile.DZX"
    dzx.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<DZX xmlns="www.geophysical.com/DZX/1.020000">
  <GlobalProperties>
    <verticalUnit>cm</verticalUnit>
    <horizontalUnit>m</horizontalUnit>
    <dielectric>2.25</dielectric>
    <unitsPerScan>0.003333</unitsPerScan>
  </GlobalProperties>
  <DataCollection>
    <system>SIR4K</system>
    <softwareVersion>1.4.35</softwareVersion>
    <depthRange>0.450000</depthRange>
    <scanPerMeters>300.000000</scanPerMeters>
    <samplesPerScan>512</samplesPerScan>
    <antModelNumber>70</antModelNumber>
  </DataCollection>
  <File>
    <Profile>
      <scanRange>0,806</scanRange>
      <WayPt>
        <scan>806</scan>
        <localCoords>-0.003332, 0.000000, 0</localCoords>
      </WayPt>
    </Profile>
  </File>
</DZX>
""",
        encoding="utf-8",
    )

    metadata = parse_dzx_metadata(dzx)

    assert metadata["present"]
    assert metadata["system"] == "SIR4K"
    assert metadata["dielectric"] == 2.25
    assert metadata["samples_per_scan"] == 512
    assert metadata["primary_scan_range"]["trace_count"] == 807
    assert metadata["waypoints"][0]["scan"] == 806


def test_build_profile_record_uses_header_and_flags_missing_dzx(tmp_path):
    dzt = tmp_path / "profile.DZT"
    dzt.write_bytes(b"synthetic dzt bytes")
    dzx = {"present": False, "path": str(tmp_path / "profile.DZX")}
    header = {
        "rh_nsamp": 512,
        "rh_bits": 32,
        "rh_nchan": 1,
        "rh_zero": 2,
        "rhf_range": 5.0,
        "rhf_epsr": 2.25,
        "rhf_spm": 300.0,
        "rhf_depth": 0.5,
        "rh_antname": ["51600S", None],
        "antfreq": [1600, None],
    }
    data = np.arange(12, dtype=np.int32).reshape(3, 4)

    record = build_profile_record(dzt, dzx, header, 0, data)

    assert record["samples"] == 3
    assert record["traces"] == 4
    assert record["profile_length_m"] == 0.01
    assert record["antenna_name"] == "51600S"
    assert record["antenna_frequency_mhz"] == 1600.0
    assert "missing_dzx_sidecar" in record["warnings"]
    assert record["sha256"]


def test_background_removed_profile_subtracts_time_sample_median():
    data = np.array([[1.0, 2.0, 100.0], [5.0, 7.0, 9.0]])

    corrected = background_removed_profile(data)

    np.testing.assert_allclose(corrected[0], [-1.0, 0.0, 98.0])
    np.testing.assert_allclose(corrected[1], [-2.0, 0.0, 2.0])


def test_depth_from_time_uses_two_way_travel_time():
    assert round(depth_from_time_m(5.0, 2.25), 6) == 0.499654
