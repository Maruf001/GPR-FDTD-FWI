## Executive finding

I found **no single public dataset that perfectly matches “raw 1600 MHz GSSI DZT/DZX reinforced-concrete rebar scans with full as-built cover, diameter, and 3D ground truth.”** The best public strategy is therefore a **portfolio**:

1. **Direct rebar lab benchmark:** Vigo / SMAR 2024 pulsed + SFCW rebar dataset.
2. **Field civil/rebar variability:** Guangzhou University raw IDS `.dt` dataset with reinforced concrete, tunnels, and utilities.
3. **Real bridge-deck benchmark:** SDNET2021, especially for GSSI bridge-deck GPR + defect ground truth.
4. **Raw commercial-format parser/controlled-target benchmark:** TU1208 / IFSTTAR geophysical test-site radargrams.
5. **FWI algorithm sanity benchmark:** MERL-GPR synthetic gprMax/FWI dataset with exact permittivity and cylindrical target ground truth.

Several other sources are useful, but many are **image-only**, **synthetic only**, **login/gated**, or **not clearly raw waveform data**. I would not use image-only datasets as FWI validation data; they are better for detector pretraining, hyperbola classification, and qualitative comparison.

---

## High-priority datasets suitable for near-term use

### 1. GPR dataset: pulsed radar and SFCW data for rebar detection — Vigo / SMAR 2024

**Direct URL / DOI:** Zenodo dataset; DOI **10.5281/zenodo.10962520**.
**Hosting source:** Zenodo.
**Data format / raw availability:** Two downloadable archives: **“Pulsed radar.zip”** and **“SFCW.zip.”** The landing page describes these as experimental GPR data for rebar detection, but the exact internal file formats are not exposed in the metadata view, so the first step should be zip inspection. The data are very likely closer to waveform/B-scan experimental data than derived paper images, but I would verify before treating them as raw.
**Antenna frequencies:** SFCW radar from **400–6000 MHz** and pulsed radar with **2.3 GHz** central frequency.
**Acquisition geometry:** Lab specimens; three specimens total: one calibration specimen and two specimens for horizontal and vertical resolution testing. The landing page does not list trace spacing, profile spacing, time window, or sample count.
**Target / scene:** Reinforced-concrete lab specimens with rebars of **8–32 mm diameter**.
**Ground truth / labels:** Strong physical ground truth for diameter and specimen design. Exact bar positions, cover depths, and profile geometry need to be checked in the archive or associated SMAR 2024 paper.
**License / restrictions:** Zenodo lists **GPL v3+**. That is unusual for data, so be careful if redistributing converted versions or combining with software.
**File size / practicality:** Very practical: about **3.7 MB total** across the two zip files.
**Reader compatibility:** Not apparently GSSI DZT/DZX. Python compatibility depends on the internal files; likely manageable after inspection. If files are ASCII, CSV, MAT, or vendor export, import should be straightforward. `readgssi` is probably not relevant unless DZT is unexpectedly included.
**Relevance score:** **5 / 5**.
**Main risks / limitations:** Exact file format and full scan geometry are not visible from the landing page. Frequency is 2.3 GHz / SFCW, not your local 1600 MHz GSSI antenna, but it is still the most directly relevant public lab rebar dataset I found. ([Zenodo][1])

**Why it matters for your project:** This is the best near-term dataset for **diameter sensitivity**, **x/z localization**, **rebar-resolution limits**, and **wavelet/frequency calibration**. It is small enough to use as the first public-data import and QC target.

---

### 2. GPR DATASET — Guangzhou University GPR Group

**Direct URL / DOI:** Zenodo dataset; DOI **10.5281/zenodo.14637589**.
**Hosting source:** Zenodo.
**Data format / raw availability:** The dataset explicitly says it provides **raw GPR data** in **IDS GeoRadar `.dt` format**.
**Antenna frequencies:** The landing page says commercial GPR systems at **various frequencies** were used, but does not list all frequencies in the metadata.
**Acquisition geometry:** Field scans from multiple civil scenes. The landing page does not specify trace spacing, profile spacing, time window, or sample count. These may be in the files, headers, folders, or associated papers.
**Target / scene:** Tunnel linings, underground pipelines, and **reinforced concrete components**. The rebar data come from a residential area in Foshan and include varying rebar densities and orientations.
**Ground truth / labels:** The page emphasizes raw data and research use, but does not clearly state full as-built target coordinates, diameters, cover depths, or annotations. Associated publications include rebar localization, field GPR FWI, RTM, and defect detection, so useful metadata may exist outside the landing page.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** One zip file, about **3.8 GB**. Practical, but not tiny; plan a staged download and checksum.
**Reader compatibility:** This is **not GSSI DZT**. `readgssi` is not the right first tool. IDS `.dt` support may require IDS software exports, RGPR/R tooling, or a custom parser. Keep this as an import milestone rather than assuming immediate Python readability.
**Relevance score:** **4.5 / 5**.
**Main risks / limitations:** Ground-truth richness is unclear; file format may be the main friction; frequencies and scan geometry need extraction from headers or documentation. ([Zenodo][2])

**Why it matters for your project:** This is one of the few public sources I found that explicitly claims **raw field GPR data** and includes **reinforced-concrete/rebar scenes**. It is highly relevant for the synthetic-to-field bridge, even if it requires parser work.

---

### 3. SDNET2021: Annotated NDE Dataset for Subsurface Structural Defects

**Direct URL / DOI:** UND Commons dataset; DOI **10.31356/data019**.
**Hosting source:** University of North Dakota Commons.
**Data format / raw availability:** Dataset files include GPR data, ground truth, test points, impact-echo data, and IRT images. File types listed include **CSV, JPEG, PNG, PDF, DWG, DOCX, and LVM**. The landing page does not list original GSSI DZT files, so treat this as **annotated GPR signal/image data rather than raw DZT** unless manual inspection proves otherwise.
**Antenna frequencies:** The associated paper reports **GSSI SIR-3000 with a 2600 MHz antenna**.
**Acquisition geometry:** Five in-service bridge decks. For one detailed bridge example, the paper reports **209 scans**, a **12 ns** vertical time scale, and **512 samples per scan**. It also describes transverse and longitudinal scans, with example spacing of **0.6 m transverse** and **3 m longitudinal** on one bridge.
**Target / scene:** Reinforced-concrete bridge decks, delamination, corrosion-related defects, and visible rebar interfaces in B-scans.
**Ground truth / labels:** Strong for bridge-deck condition: ground-truth maps from repair/chain dragging after milling, with classes including sound/no delamination, shallow delamination above the top mat, and deeper delamination below the top mat. It is not primarily a diameter-estimation dataset.
**License / restrictions:** The paper states the data are under the **UND Commons license**; verify exact reuse terms before redistribution.
**File size / practicality:** GPR data file listed around **1.94 GB**; impact-echo data are also large. Download is practical.
**Reader compatibility:** CSV/image-style formats should be Python-readable. It is GSSI-acquired, but not necessarily distributed as DZT. `readgssi` may not apply to the public files.
**Relevance score:** **4 / 5**.
**Main risks / limitations:** Excellent for field bridge-deck benchmarking and defect mapping, weaker for exact rebar radius/diameter inversion. Public data may be processed/converted rather than raw DZT. ([UND Scholarly Commons][3])

**Why it matters for your project:** SDNET2021 is the best public benchmark I found for **real bridge-deck GPR with independent NDE ground truth**. It is especially useful for 2.5D bridge-deck diagnostics, uncertainty scoring, and validating whether your inversion-derived features correlate with defects.

---

### 4. TU1208 Open Database of Radargrams — IFSTTAR / Gustave Eiffel geophysical test site

**Direct URL / DOI:** Zenodo dataset; DOI **10.5281/zenodo.1211173**.
**Hosting source:** Zenodo; related to the TU1208 Civil Engineering Applications of Ground Penetrating Radar database.
**Data format / raw availability:** Supplementary zip of about **200.7 MB**. The associated documentation describes multiple commercial formats including **DZT, DZX, RD3, and DT**. The paper notes that most data are raw without filtering or gain, while some older data were preprocessed and 2017 GPR1 includes both raw `.dzt` and preprocessed `.dzx` information.
**Antenna frequencies:** Multiple systems/frequencies, including examples around **200, 400, 500, 800, and 900 MHz**.
**Acquisition geometry:** Controlled test-site profiles; the associated paper tables list profile lengths, scans per meter, sample counts, ranges, and bit depths for many lines. It includes parallel-line acquisitions and multiple campaigns.
**Target / scene:** Controlled urban/geophysical test site with buried objects and subsurface structures. Not concrete rebar, but useful for pipes, voids, cylinders, and controlled-target inversion workflows.
**Ground truth / labels:** Test-site geometry and acquisition tables provide stronger ground-truth context than many field datasets, although you should extract target coordinates from the paper/supplement before using it quantitatively.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** About **200 MB**, very practical.
**Reader compatibility:** Strong. DZT files can likely be tested with `readgssi`; RD3/DT can be handled through RGPR or custom import. The `readgssi` documentation specifically supports reading GSSI DZT/DZX-related data and exporting to formats such as CSV, HDF5, NumPy, SEG-Y, and JSON headers, while noting that not every GSSI header variant is guaranteed. ([Zenodo][4])
**Relevance score:** **4 / 5**.
**Main risks / limitations:** Frequencies and target scale are less like high-frequency concrete rebar work. It is better for **import, QC, velocity, controlled-target FDTD/FWI testing, and parser validation** than for rebar-cover or diameter claims.

**Why it matters for your project:** This is a good bridge between your local **GSSI DZT/DZX workflow** and public controlled-target data. It can validate your import stack, time-zero handling, velocity fitting, and FDTD/FWI machinery before applying it to local concrete scans.

---

### 5. Ground Penetrating Radar Corrosion Data — Wong et al.

**Direct URL / DOI:** Mendeley Data; DOI **10.17632/wbdr5pdxbd.1**.
**Hosting source:** Mendeley Data.
**Data format / raw availability:** The landing page describes a dataset related to GPR corrosion studies, but the web metadata I could access did **not** expose the internal file list, file size, or exact formats. Treat raw waveform availability as **uncertain until inspected**.
**Antenna frequencies:** Multiple systems/frequencies are listed: **GSSI SIR4000 2 GHz**, **GSSI SIR20 2 GHz**, **Mala ProEx 1.6 GHz**, and **GSSI SIR20 2.6 GHz**.
**Acquisition geometry:** Specimens and field marine structures under multiple conditions. The landing page mentions cover depths of **45, 50, and 75 mm** for some specimens, but does not provide full trace spacing, profile spacing, time windows, or sample counts.
**Target / scene:** Reinforced-concrete corrosion, saline exposure, accelerated corrosion, hairline cracks, marine structures, delamination, internal cracks, surface cracks, corrosion, and section loss.
**Ground truth / labels:** Condition labels and cover-depth information are partially described. Exact target coordinates and bar diameters are not clear from the landing page.
**License / restrictions:** **CC BY 4.0** on the Mendeley page.
**File size / practicality:** Not visible from the accessible metadata.
**Reader compatibility:** Potentially very relevant to your local data because it includes GSSI and 1.6–2.6 GHz systems. But compatibility depends entirely on whether the actual files are DZT, RD3/RAD, exported images, CSV, MAT, or another format.
**Relevance score:** **3.5–4 / 5**, conditional on raw-file availability.
**Main risks / limitations:** Internal file format and rawness are not confirmed from the landing page. Use this as a high-priority **inspection target**, not as a guaranteed raw benchmark. ([Mendeley Data][5])

**Why it matters for your project:** If the downloadable files include raw or minimally processed GPR profiles, this becomes a top-tier frequency-bridge dataset because it includes **1.6 GHz Mala** and **2.0/2.6 GHz GSSI** data on reinforced concrete deterioration.

---

### 6. MERL-GPR: 2D synthetic GPR FWI / inverse-scattering dataset

**Direct URL / DOI:** Zenodo dataset; DOI **10.5281/zenodo.8145084**.
**Hosting source:** Zenodo.
**Data format / raw availability:** Synthetic gprMax/FWI-style dataset, not field raw data. The archive includes modeled wavefields, source coefficients, and trained models; unzipped size is about **1.72 GB**.
**Antenna frequencies:** Uses a **1 GHz Ricker source**, with frequency-domain information extracted from **0.5–1.5 GHz** over 50 frequencies.
**Acquisition geometry:** **400** simulated 2D underground structures. Each domain is **0.5 m × 0.5 m**, with air over layered ground and two cylindrical objects in the lower layer.
**Target / scene:** Synthetic layered media with cylindrical inclusions; one cylinder is air-like and another has variable permittivity. Radii are sampled between **0.03 and 0.06 m**.
**Ground truth / labels:** Excellent: exact permittivity model, geometry, and wavefield information.
**License / restrictions:** **CC BY-SA 4.0**.
**File size / practicality:** Download zip about **1.6 GB**; practical.
**Reader compatibility:** Designed for computational use; Python import should be straightforward after reading the archive structure. Not relevant to `readgssi`.
**Relevance score:** **4 / 5** for FDTD/FWI development; **2.5 / 5** for field rebar validation.
**Main risks / limitations:** Synthetic only; not reinforced concrete; cylinders are dielectric/air-like rather than steel rebars; no commercial antenna or real coupling effects. ([Zenodo][6])

**Why it matters for your project:** This is useful for **FWI gradient checks, misfit behavior, ambiguity studies, radius/permittivity tradeoffs, and reproducible inverse-scattering baselines** before you spend GPU time on 3D concrete/rebar simulations.

---

## Medium-priority datasets useful for calibration, import testing, or method comparison

### 7. CMU-GPR-Dataset

**Direct URL / DOI:** GitHub repository; no DOI found in the repository metadata I inspected.
**Hosting source:** GitHub, CMU Robotics / rpl-cmu.
**Data format / raw availability:** CSV-style data with synchronized odometry, GPR traces, camera, IMU, and total-station measurements. The repository describes “raw traces” plus processing steps.
**Antenna frequencies:** **Sensors & Software Noggin 500**, i.e., 500 MHz class.
**Acquisition geometry:** 15 sequences with mobile acquisition and revisitation. The data include GPR measurements, wheel odometry, IMU, camera, and total-station ground truth.
**Target / scene:** Subsurface localization / robotic mapping context, not concrete rebar.
**Ground truth / labels:** Strong pose/trajectory ground truth; not strong target-object ground truth for rebar/diameter.
**License / restrictions:** **CC BY-NC-SA 4.0**; noncommercial academic use.
**File size / practicality:** Individual sequences range from tens of MB to about 1.2 GB; full unprocessed groups are around **1.3–4.0 GB**. Practical but not tiny.
**Reader compatibility:** Python-friendly because key measurements are CSV; not a DZT/readgssi dataset.
**Relevance score:** **3 / 5**.
**Main risks / limitations:** Frequency and scene are far from concrete rebar. Use for pose-aware GPR data structures, revisitation, and 2.5D/3D acquisition concepts rather than rebar inversion. ([GitHub][7])

---

### 8. GprMax Deep Learning Challenge 1 / Kaggle FWI data

**Direct URL / DOI:** Kaggle competition/dataset page; no DOI found in the accessible metadata.
**Hosting source:** Kaggle.
**Data format / raw availability:** Synthetic `.npy` B-scan arrays and ground-truth relative-permittivity labels. The accessible paper text describes processed time-varying-gain B-scans with input size **230 × 230** and ground-truth permittivity labels of **224 × 224**.
**Antenna frequencies:** Generated with gprMax; specific antenna/wavelet details should be taken from the competition files/rules.
**Acquisition geometry:** One-shot multi-offset synthetic GPR for full-waveform inversion. Evaluation data include missing traces.
**Target / scene:** Synthetic subsurface permittivity reconstruction, not concrete/rebar-specific.
**Ground truth / labels:** Excellent synthetic ground truth: relative permittivity maps.
**License / restrictions:** Kaggle competition terms; do not assume open CC-style reuse.
**File size / practicality:** Depends on Kaggle download; requires account/login.
**Reader compatibility:** Very Python-friendly via NumPy arrays. Not relevant to `readgssi`.
**Relevance score:** **3.5 / 5**.
**Main risks / limitations:** Synthetic and processed; not a public civil-infrastructure raw-data benchmark. Still useful for inversion baselines and missing-trace robustness. ([arXiv][8])

---

### 9. Synthetic 3D GPR dataset across a realistic sedimentary model

**Direct URL / DOI:** Mendeley Data; DOI **10.17632/by3yh79hx4.1**.
**Hosting source:** Mendeley Data.
**Data format / raw availability:** Synthetic 3D GPR reflection dataset plus the underlying realistic sedimentary model. The landing page states that MATLAB and Python code are provided to read and visualize the data.
**Antenna frequencies:** Not visible in the accessible landing-page metadata.
**Acquisition geometry:** Full 3D modeled GPR reflection dataset across a realistic sedimentary surface/model.
**Target / scene:** Sedimentary stratigraphy, not civil infrastructure or rebar.
**Ground truth / labels:** Strong synthetic ground truth from the underlying model.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** Not visible in the metadata I could access; likely larger than small 2D examples.
**Reader compatibility:** Good, because Python/MATLAB reader code is explicitly provided.
**Relevance score:** **3 / 5**.
**Main risks / limitations:** Geologic scale and physics are not concrete/rebar-like. Its value is mainly for **3D volume handling, visualization, and HPC memory/performance planning**. ([Mendeley Data][9])

---

### 10. Non-destructive Methods for Reinforcement Mapping in Concrete Members: Databases

**Direct URL / DOI:** Zenodo dataset; DOI **10.5281/zenodo.17292599**.
**Hosting source:** Zenodo.
**Data format / raw availability:** CSV/XLSX-style tabular database, not waveform data. The dataset contains **3,463 test results** from literature, including **784 GPR tests**.
**Antenna frequencies:** Frequency appears as one of the GPR variables where available, but this is not a raw scan repository.
**Acquisition geometry:** Literature-extracted measurements rather than profiles.
**Target / scene:** Reinforcement mapping in concrete members using cover meters and GPR.
**Ground truth / labels:** Includes variables such as estimated spacing, number of bars, diameter, cover depth, and effective depth, depending on source study.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** Very small: GPR database CSV is about **128 kB**; total dataset under 1 MB.
**Reader compatibility:** Trivial in Python/pandas.
**Relevance score:** **2.5 / 5**.
**Main risks / limitations:** No waveform, no B-scans, no raw FWI value. Use it for priors, error ranges, and literature calibration targets, not signal processing. ([Zenodo][10])

---

### 11. Pavement tack-coat GPR datasets — Gustave Eiffel / Andreoli et al.

**Direct URL / DOI:** Data in Brief 2025 datasets; experimental paper DOI **10.1016/j.dib.2025.112009** and synthetic paper DOI **10.1016/j.dib.2025.111794**.
**Hosting source:** Data in Brief / associated institutional repositories.
**Data format / raw availability:** The accessible metadata describes experimental and synthetic GPR databases for pavement tack-coat characterization, with hybrid ML/FWI motivation. I did not find a clean repository file listing in the accessible search results, so raw-format details remain to be verified.
**Antenna frequencies:** Experimental database used impulse GPR with multiple central frequencies and ground-coupled bowtie antennas. Specific frequencies need confirmation from the full dataset documentation.
**Acquisition geometry:** Controlled multi-layer pavement structures with geometry and tack-coat variations.
**Target / scene:** Pavement layers and tack-coat bonding, not rebar.
**Ground truth / labels:** Controlled laboratory pavement structure should provide meaningful ground truth for layer geometry and material state.
**License / restrictions:** Data in Brief articles are open; the visible article metadata lists **CC BY 4.0**. Verify dataset-specific terms before redistribution.
**File size / practicality:** Not verified from accessible metadata.
**Reader compatibility:** Unknown until repository files are inspected.
**Relevance score:** **3–3.5 / 5**, mainly for FWI/ML methodology.
**Main risks / limitations:** Not concrete/rebar, and direct downloadable raw-data details were not visible from the sources I could access. ([PubMed][11])

---

### 12. GPRPy / NSGeophysics example datasets

**Direct URL / DOI:** GitHub repository / project site; no single dataset DOI found in the pages inspected.
**Hosting source:** GitHub and NSGeophysics/GPRPy resources.
**Data format / raw availability:** Example data for learning and testing GPRPy, including common-offset profiles, data cubes, velocity analysis, and dune examples.
**Antenna frequencies:** Varies by example; not necessarily civil-infrastructure focused.
**Acquisition geometry:** Educational examples including profiles and data cubes.
**Target / scene:** Mostly geophysical examples, not rebar.
**Ground truth / labels:** Limited; educational rather than benchmark-grade.
**License / restrictions:** Check repository license before reuse.
**File size / practicality:** Practical for testing.
**Reader compatibility:** Good for Python/GPRPy workflows; RGPR is also an open-source GPR package for reading, exporting, analyzing, processing, and visualizing GPR data.
**Relevance score:** **2.5 / 5**.
**Main risks / limitations:** Useful for import/QC practice, not for rebar localization or diameter estimation. ([GitHub][12])

---

## Low-priority or image-only datasets

### 13. TIGPR: Transportation Infrastructure GPR dataset

**Direct URL / DOI:** Mendeley Data; DOI **10.17632/ckgvrft232.1**.
**Hosting source:** Mendeley Data.
**Data format / raw availability:** Image dataset. The landing page describes 2D B-scan images of **200 × 200** and 3D B-scan/C-scan images of **320 × 320**.
**Antenna frequencies:** Equipment includes IDS-FastWave, MALA GX750, and GeoScope 3D-Radar, but exact frequency settings are not fully exposed in the metadata.
**Acquisition geometry:** Roads, bridges, tunnels, and airports; image dimensions correspond to **10 m length** and **1 m depth**.
**Target / scene:** Cracks, interlayer debonding, looseness, voids, and other transportation-infrastructure defects.
**Ground truth / labels:** ML-style labels/classes for damage detection/classification/segmentation.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** Not visible in the accessible metadata.
**Reader compatibility:** Image-based; easy in Python, but not waveform/FWI data.
**Relevance score:** **2.5 / 5**.
**Main risks / limitations:** Good for image detection and segmentation comparisons; weak for waveform inversion or rebar-cover estimation. ([Mendeley Data][13])

---

### 14. Intelligent recognition of subsurface utilities and voids: GPR dataset for deep learning

**Direct URL / DOI:** Mendeley Data; DOI **10.17632/ww7fd9t325.1**; also mirrored/organized on GitHub.
**Hosting source:** Mendeley Data and GitHub.
**Data format / raw availability:** The article and repository describe **JPEG radargrams**, not raw waveform files. The dataset includes **2,239** images of utilities, voids, and intact zones.
**Antenna frequencies:** **200 MHz** and **400 MHz** GPR.
**Acquisition geometry:** Field data from Morocco, 2019–2024; exact trace spacing and time windows are not visible from the dataset landing page.
**Target / scene:** Buried utilities, cavities/voids, and intact zones.
**Ground truth / labels:** Image-level labels/classes; not precise target geometry suitable for FWI.
**License / restrictions:** Mendeley lists **CC BY 4.0**; the associated article text indicates a CC BY-NC open-access license for the article, so verify dataset license before redistribution.
**File size / practicality:** Image dataset; practical.
**Reader compatibility:** Easy for Python image pipelines. Not a `readgssi` or waveform dataset.
**Relevance score:** **2.5 / 5**.
**Main risks / limitations:** Useful for hyperbola/void detector robustness, but not concrete/rebar and not raw waveform. ([Mendeley Data][14])

---

### 15. Deep learning model for rebar detection from GPR data

**Direct URL / DOI:** Zenodo; DOI **10.5281/zenodo.16902131**.
**Hosting source:** Zenodo.
**Data format / raw availability:** Primarily model/notebook artifacts and example images, not a raw waveform dataset. Files include trained models, an example PNG, and a notebook.
**Antenna frequencies / geometry:** Not a primary acquisition dataset.
**Target / scene:** Rebar detection in GPR images, including validation on a reinforced-concrete pedestrian bridge.
**Ground truth / labels:** Detection-model context; raw labels and waveform data are not clearly provided as a standalone benchmark.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** Models archive about **1.7 GB** plus smaller files.
**Reader compatibility:** Python/Jupyter model workflow; not waveform import.
**Relevance score:** **2 / 5**.
**Main risks / limitations:** Useful as a detector baseline or literature pointer, not FDTD/FWI data. ([Zenodo][15])

---

### 16. Deep learning model for delamination detection from GPR data

**Direct URL / DOI:** Zenodo; DOI **10.5281/zenodo.14607117**.
**Hosting source:** Zenodo.
**Data format / raw availability:** Software/notebook/model artifact. It depends on SDNET2021 rather than replacing it.
**Antenna frequencies / geometry:** Inherited from SDNET2021 if used.
**Target / scene:** Bridge-deck delamination detection.
**Ground truth / labels:** Uses SDNET2021 labels.
**License / restrictions:** Check Zenodo record and associated repository.
**File size / practicality:** About **19.4 MB** for the software archive.
**Reader compatibility:** Python/Jupyter/MATLAB-style workflow.
**Relevance score:** **2 / 5**.
**Main risks / limitations:** Not a dataset for waveform/FWI. Use only as an ML baseline or SDNET2021 reference implementation. ([Zenodo][16])

---

### 17. MCG GPR dataset

**Direct URL / DOI:** Zenodo; DOI **10.5281/zenodo.14270869**.
**Hosting source:** Zenodo.
**Data format / raw availability:** PNG images and segmentation masks, not raw waveforms.
**Antenna frequencies / geometry:** Mixed public image sources; not a uniform acquisition dataset.
**Target / scene:** General GPR segmentation content, including geologic/beach-style sources.
**Ground truth / labels:** Segmentation masks created using image-processing methods and manual correction.
**License / restrictions:** **CC BY 4.0**.
**File size / practicality:** About **1.4 GB**.
**Reader compatibility:** Python image segmentation tools.
**Relevance score:** **1.5–2 / 5**.
**Main risks / limitations:** Too far from reinforced-concrete waveform inversion; only useful for generic image segmentation experiments. ([Zenodo][17])

---

## Promising papers or repositories where data appear not directly public

### A. Rutgers / Dana automated rebar analysis dataset

The GitHub repository describes a very relevant bridge-deck rebar dataset, including raw **GSSI SIR-20 `.DZT`** files and IDS `.DT` files, plus positive and negative hyperbola samples. However, the README states that users should **contact Dr. Kristin Dana** to use the dataset, so I do **not** treat it as a directly public downloadable dataset. Potential relevance is **5 / 5** if access is granted, especially for your local GSSI DZT/DZX workflow. ([GitHub][18])

### B. Open_GPR_Dataset_for_Bridge_Deck / InfraSmartLab

The repository describes **20,000 simulated GPR scans** generated using gprMax for automated rebar detection in bridge decks, with variation in antenna frequency, rebar configuration, spacing, material properties, and bounding-box labels. However, the repository I inspected contains only a README and an access-request process; it does not expose direct dataset files. Treat it as promising but gated/request-based, not a direct public benchmark. ([GitHub][19])

### C. DECKGPRH1.0 / Asadi-style bridge-deck B-scan image datasets

The literature describes bridge-deck GPR image datasets with thousands of cropped B-scan images and rebar targets, but I did not find a direct public repository with raw files or complete download metadata. These are promising for image-level detector comparison, but not reliable near-term FWI datasets unless the authors provide access. ([DigitalCommons@URI][20])

### D. FHWA LTBP / InfoBridge bridge-deck GPR

The FHWA LTBP GPR protocol is highly relevant: it specifies bridge-deck GPR data fields, including antenna frequency, range, samples per scan, scans per unit, line locations, direction, and data BLOB / ASCII file fields for **DZT or DT files**. The protocol also targets deterioration, rebar/conduit location, cover/deck thickness, voids, and honeycombing. However, I did not identify a simple direct public dataset landing page for bulk raw DZT/DT download through InfoBridge during this search. Treat LTBP/InfoBridge as a high-value future data-mining target, not a confirmed near-term download. ([Federal Highway Administration][21])

---

## Top 5 shortlist for your GPR-FDTD-FWI project

### Recommended top 5

| Rank | Dataset                            | Why it makes the shortlist                                                    | Best use                                                                |
| ---: | ---------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
|    1 | **Vigo pulsed/SFCW rebar dataset** | Direct lab rebar dataset with known diameter range and high-frequency GPR     | Rebar localization, diameter sensitivity, frequency/wavelet calibration |
|    2 | **Guangzhou GPR DATASET**          | Raw field `.dt` data with reinforced concrete/rebar, tunnels, and utilities   | Field variability, synthetic-to-field bridge, parser development        |
|    3 | **SDNET2021**                      | Real GSSI bridge-deck GPR with independent NDE ground truth                   | Bridge-deck diagnostics, 2.5D mapping, condition labels                 |
|    4 | **TU1208 IFSTTAR radargrams**      | Public raw commercial-format controlled-target data, including DZT/DZX/RD3/DT | Import/QC, velocity fitting, controlled FDTD/FWI tests                  |
|    5 | **MERL-GPR**                       | Synthetic gprMax/FWI dataset with exact model ground truth                    | FWI algorithm validation, ambiguity analysis, synthetic benchmark       |

**Conditional swap:** If the Wong corrosion dataset download contains raw or minimally processed GPR profiles, I would promote it into the top 5, likely replacing MERL-GPR for field-data calibration. Its 1.6–2.6 GHz concrete/corrosion coverage is unusually relevant to your local **GSSI 51600S / 1600 MHz** situation. ([Mendeley Data][5])

---

## Recommended integration plan

### Phase 0 — CPU-only inventory and import QC

Start with the smallest and most directly relevant data:

1. **Vigo rebar dataset**: unzip, list internal formats, extract A-scan/B-scan arrays, time axes, trace spacing, and specimen metadata.
2. **TU1208**: test DZT/DZX import using `readgssi`; test RD3/DT paths with RGPR or custom readers.
3. **SDNET2021**: import public CSV/GPR files, ground-truth maps, bridge geometry, and scan metadata.
4. **Guangzhou**: inspect IDS `.dt` headers/folders and determine whether an existing parser/export path is usable.
5. **MERL-GPR**: load synthetic arrays and ground-truth permittivity models.

For your own GSSI DZT/DZX data, `readgssi` is the most relevant first-pass Python tool because its documentation describes DZT/DZX modules and export paths to CSV, HDF5, NumPy, SEG-Y, and JSON headers. Its PyPI page also warns that GSSI file structures can vary and not every header has been tested, so use it as a practical parser to validate, not as a guaranteed black box. ([Read GSSI][22])

Recommended canonical internal format:

```text
dataset/
  raw/
  processed_minimal/
  metadata.json
  scans.h5 or scans.zarr
    /bscan/amplitude[n_trace, n_sample]
    /axes/time_ns[n_sample]
    /axes/x_m[n_trace]
    /geometry/profile_id
    /labels/targets
    /labels/defects
    /processing_log
```

Keep **raw**, **minimally processed**, and **analysis-ready** versions separate. For FWI, never overwrite the raw data with background removal, migration, gain, or image normalization.

---

### Phase 1 — Velocity and dielectric calibration

Use the datasets differently:

**Vigo:**
Use the known rebar diameters and controlled specimens to estimate effective concrete velocity/permittivity, compare pulsed 2.3 GHz against SFCW 400–6000 MHz, and quantify how diameter changes affect amplitude, phase, and hyperbola curvature. This is the best first public dataset for your radius/diameter sensitivity study.

**SDNET2021:**
Use the reported 2600 MHz GSSI setup, 12 ns time window, 512 samples, and bridge-deck scan geometry to benchmark field-style rebar reflections, attenuation trends, and defect-map agreement. It is more useful for **cover/depth, defect confidence, and bridge-deck mapping** than for rebar diameter.

**TU1208:**
Use controlled objects and commercial raw formats to validate your velocity-fitting pipeline, time-zero correction, trace spacing handling, and parser robustness. This is especially useful before trusting local GSSI DZT/DZX imports.

**Guangzhou:**
After `.dt` import is solved, use rebar scenes for field variability, orientation effects, and domain transfer. Because labels may be incomplete, combine manual annotation with model-driven hyperbola fitting.

**MERL-GPR:**
Use exact synthetic permittivity/radius ground truth to test FWI gradients, inversion stability, and ambiguity/confidence metrics. This is where you can safely stress-test loss functions before field complications dominate.

---

### Phase 2 — Match datasets to 2D, 2.5D, and 3D experiments

| Dataset                  |                       2D FDTD/FWI |    2.5D bridge/field mapping |                                        3D extension value |
| ------------------------ | --------------------------------: | ---------------------------: | --------------------------------------------------------: |
| Vigo rebar               |                         Excellent |                      Limited | Low–medium; lab profiles only unless grid exists in files |
| Guangzhou                |    Good if profiles are separable |                         Good |         Medium; depends on profile/grid layout in archive |
| SDNET2021                |         Good for individual lines |                    Excellent |                  Medium–high for bridge-deck volumes/maps |
| TU1208                   | Excellent for controlled profiles | Good for parallel-line tests | Medium; useful for 3D geometry/import but not rebar scale |
| MERL-GPR                 |           Excellent synthetic FWI |                          Low |              Medium for algorithmic scaling, but it is 2D |
| CMU-GPR                  |                     Low for rebar |  Good for pose-aware mapping |              Medium for robotics-style repeated traversal |
| 3D sedimentary synthetic |                     Low for rebar |                          Low |          High for 3D volume handling and HPC benchmarking |

---

### Phase 3 — When these datasets justify future A100 / 3D FWI work

Use an A100/HPC justification only after the CPU pipeline proves four things:

1. **Import success:** raw or minimally processed arrays are reproducibly loaded with correct time axes, trace spacing, and metadata.
2. **Calibration success:** effective velocity/permittivity estimates are stable across at least Vigo, TU1208, SDNET2021, and your local GSSI data.
3. **2D baseline gap:** 2D FDTD/FWI explains clean lab data but fails systematically on field profiles with cross-line structure, oblique bars, grids, or 3D scattering.
4. **3D target value:** SDNET2021, Guangzhou, your local GSSI scans, or a future bridge/slab grid provide enough profile density to make 3D inversion scientifically meaningful rather than just computationally impressive.

The strongest HPC story is:

> “We validated waveform import and 2D inversion on public controlled rebar/cylinder data; field bridge/slab data show residuals and uncertainty patterns consistent with out-of-plane scattering and grid effects; therefore 3D FDTD/FWI is required to resolve rebar grids, cover, confidence, and defect interactions.”

For that argument, the most useful combination is **Vigo + SDNET2021 + Guangzhou + TU1208 + local GSSI 1600 MHz**. MERL-GPR and Kaggle/gprMax data support the algorithmic side, but public field data are what make the 3D/HPC case persuasive.

[1]: https://zenodo.org/records/10962520 "GPR dataset: pulsed radar and SFCW data for rebar detection (experimental data)"
[2]: https://zenodo.org/records/14637589 "GPR DATASET"
[3]: https://commons.und.edu/data/19 "
\"SDNET2021: Annotated NDE Dataset for Structural Defects\" by Eberichi Ichi and Sattar Dorafshan
"
[4]: https://zenodo.org/records/1211173 "Supplementary Files: TU1208 Open Database of Radargrams: The Dataset of the IFSTTAR Geophysical Test Site"
[5]: https://data.mendeley.com/datasets/wbdr5pdxbd/1 "Ground Penetrating Radar (GPR) Corrosion Data (Wong, 2023) - Mendeley Data"
[6]: https://zenodo.org/records/8145084 "MERL Ground Penetrating Radar Dataset (MERL-GPR)"
[7]: https://github.com/rpl-cmu/CMU-GPR-Dataset "GitHub - rpl-cmu/CMU-GPR-Dataset: Dataset and utilities for research on localizing ground penetrating radar (GPR). · GitHub"
[8]: https://arxiv.org/html/2410.14386v1?utm_source=chatgpt.com "A Numerical Case Study for Lunar and Martian Environments"
[9]: https://data.mendeley.com/datasets/by3yh79hx4/1 "A synthetic 3D ground-penetrating radar (GPR) data set across a realistic sedimentary model - Mendeley Data"
[10]: https://zenodo.org/records/17292599 "Non-destructive Methods for Reinforcement Mapping in Concrete Members: Databases"
[11]: https://pubmed.ncbi.nlm.nih.gov/40955415/ "Experimental GPR datasets to characterize multi-layered pavement structures-Tack coat evaluation using hybridization method - PubMed"
[12]: https://github.com/NSGeophysics/GPRdata "GitHub - NSGeophysics/GPRdata: Additional example GPR data. · GitHub"
[13]: https://data.mendeley.com/datasets/ckgvrft232 "TIGPR: A Multi-View Ground Penetrating Radar Detection Data for Damage Assessment of Transportation Infrastructure - Mendeley Data"
[14]: https://data.mendeley.com/datasets/ww7fd9t325/1 "Intelligent recognition of subsurface utilities and voids: A Ground Penetrating Radar dataset for Deep Learning applications - Mendeley Data"
[15]: https://zenodo.org/records/16902131 "Deep learning model for rebar detection from GPR data"
[16]: https://zenodo.org/badge/latestdoi/909646043 "Deep learning model for delamination detection from GPR data"
[17]: https://zenodo.org/records/14270869 "MCG GPR dataset"
[18]: https://github.com/kjdana/automated_rebar_analysis_dataset "GitHub - kjdana/automated_rebar_analysis_dataset: Dataset used for automated rebar analysis. · GitHub"
[19]: https://github.com/InfraSmartLab/Open_GPR_Dataset_for_Bridge_Deck "GitHub - InfraSmartLab/Open_GPR_Dataset_for_Bridge_Deck · GitHub"
[20]: https://digitalcommons.uri.edu/cs_facpubs/29/?utm_source=chatgpt.com "A Machine Learning Based Approach for Automatic Rebar ..."
[21]: https://www.fhwa.dot.gov/publications/research/infrastructure/structures/ltbp/16007/034.cfm?utm_source=chatgpt.com "Long-Term Bridge Performance (LTBP) Program Protocols ..."
[22]: https://readgssi.readthedocs.io/ "readgssi 0.0.22 documentation — readgssi  documentation"
