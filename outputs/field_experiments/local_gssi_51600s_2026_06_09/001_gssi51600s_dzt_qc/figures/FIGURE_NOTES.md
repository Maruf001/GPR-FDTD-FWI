# Figure Notes

## `field_profile_qc_context.png`

Profile-level system figure for the GSSI 51600S field data. It shows the
imported B-scan lengths and a generic x-z QC slice. Crossline offsets are not
encoded in the available DZX sidecars, so this is not a reconstructed 3D survey
geometry.

## `gssi_dzt_inventory.png`

Trace-count and distance inventory for each imported DZT channel. Blue bars
have a DZX sidecar; red bars were imported from the DZT header only.

## B-scan QC Figures

- `PROJECT001C__013_ch0_bscan_qc.png`: raw and median-background-removed B-scan for `PROJECT001C__013.DZT` channel 0.
- `PROJECT001C__014_ch0_bscan_qc.png`: raw and median-background-removed B-scan for `PROJECT001C__014.DZT` channel 0.
- `PROJECT001C__015_ch0_bscan_qc.png`: raw and median-background-removed B-scan for `PROJECT001C__015.DZT` channel 0.
- `PROJECT001C__016_ch0_bscan_qc.png`: raw and median-background-removed B-scan for `PROJECT001C__016.DZT` channel 0.

These figures are import/QC artifacts. They do not imply that the current 2D
FDTD/FWI model is ready to invert the measured data.
