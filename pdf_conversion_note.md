# Notebook to PDF Conversion

## Command

```bash
jupyter nbconvert --to webpdf notebook.ipynb --no-input
```

`--no-input` hides code cells, showing only markdown and outputs.

## Dependencies

```bash
pip install nbconvert[webpdf] playwright
playwright install chromium
```

- `nbconvert` — Jupyter conversion tool
- `playwright` — headless Chromium for rendering HTML to PDF (newer nbconvert versions use this over pyppeteer)
- `playwright install chromium` — downloads the Chromium binary on first setup

## Environment Used

Conda env: `FNO` (Python 3.13)
