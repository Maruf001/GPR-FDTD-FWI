from run_gssi_field_survey_geometry_audit import classify_geometry, parse_dzx_profile


def test_parse_dzx_profile_reads_scan_range_and_waypoints(tmp_path):
    dzx = tmp_path / "profile.DZX"
    dzx.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<DZX xmlns="www.geophysical.com/DZX/1.020000">
  <GlobalProperties>
    <unitsPerScan>0.003333</unitsPerScan>
  </GlobalProperties>
  <DataCollection>
    <scanPerMeters>300.0</scanPerMeters>
    <gridId>Grid</gridId>
  </DataCollection>
  <File>
    <Profile>
      <scanRange>0,100</scanRange>
      <WayPt><scan>0</scan><localCoords>0.0, 0.0, 0</localCoords></WayPt>
      <WayPt><scan>100</scan><localCoords>1.0, 0.0, 0</localCoords></WayPt>
    </Profile>
    <scanRange>0,100</scanRange>
  </File>
</DZX>
""",
        encoding="utf-8",
    )

    profile = parse_dzx_profile(dzx)

    assert profile["grid_id"] == "Grid"
    assert profile["scan_range_start"] == 0
    assert profile["scan_range_end"] == 100
    assert profile["waypoint_count"] == 2
    assert profile["waypoint_endpoint_distance_m"] == 1.0


def test_classify_geometry_rejects_profiles_without_crossline_file():
    rows = [
        {
            "trace_derived_profile_length_m": 1.0,
            "waypoint_length_ratio_to_trace_length": 1.0,
            "dzx_waypoint_start_y_m": 0.0,
            "dzx_waypoint_end_y_m": 0.0,
        },
        {
            "trace_derived_profile_length_m": 1.0,
            "waypoint_length_ratio_to_trace_length": 1.0,
            "dzx_waypoint_start_y_m": 0.5,
            "dzx_waypoint_end_y_m": 0.5,
        },
    ]

    summary = classify_geometry(rows, no_dzg=True)

    assert summary["classification"] == "independent_2d_line_profiles"
    assert summary["has_reliable_waypoint_lengths"] is True
    assert summary["no_dzg_file"] is True
    assert "no DZG" in summary["reasons"][0]


def test_classify_geometry_requires_reliable_waypoint_lengths():
    rows = [
        {
            "trace_derived_profile_length_m": 2.0,
            "waypoint_length_ratio_to_trace_length": 0.01,
            "dzx_waypoint_start_y_m": 0.0,
            "dzx_waypoint_end_y_m": 0.0,
        },
        {
            "trace_derived_profile_length_m": 2.0,
            "waypoint_length_ratio_to_trace_length": 0.01,
            "dzx_waypoint_start_y_m": 1.0,
            "dzx_waypoint_end_y_m": 1.0,
        },
    ]

    summary = classify_geometry(rows, no_dzg=False)

    assert summary["classification"] == "independent_2d_line_profiles"
    assert summary["has_crossline_file"] is True
    assert summary["has_reliable_waypoint_lengths"] is False
