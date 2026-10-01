# Spatia·CODEX — spatial-proteomics CRO website

A static, self-contained website for a CODEX / PhenoCycler spatial-proteomics contract
research service. The antibody library, cell-type coverage and application panels are
derived from the Nolan-lab CODEX antibody inventory.

## Contents
- `index.html` — the complete site (HTML + CSS + JS + data all inlined; no build step, no dependencies).
- `data.json` — machine-readable export of the antibodies, panels and cell-type mapping.
- `build_data.py` / `build_site.py` — scripts that generated `data.json` and `index.html` from the inventory.
- `.nojekyll` — tells GitHub Pages to serve files as-is.

## What it shows
- **148 in-stock antibodies** (searchable, filterable by compartment), each mapped to the cell type(s) it resolves.
- **9 ready-to-run panels**: Tumor Microenvironment, Immune Checkpoint & Exhaustion, Autoimmunity & Chronic Inflammation, Lymphoid Architecture / TLS, Myeloid & Innate, NK & Cytotoxicity, Tumour Epithelium & EMT, Stroma/Vasculature, GI/Mucosal (eosinophilic disease).
- **Cell types & states** resolvable, grouped by lineage with representative markers.

## Deploy to GitHub Pages
1. Create a repo (e.g. `spatia-codex-site`) and copy these files into it (the site must be at the repo root, or in a `/docs` folder).
2. Push to GitHub.
3. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**, Branch: `main` (root, or `/docs`), Save.
4. The site publishes at `https://<user>.github.io/<repo>/` within a minute.

Local preview: `python3 -m http.server` in this folder, then open `http://localhost:8000`.

## Updating the data
Edit the `A` (antibodies) and `P` (panels) dictionaries in `build_data.py`, then run
`python3 build_data.py && python3 build_site.py` to regenerate `data.json` and `index.html`.

_For research use only. Antibody list reflects the Nolan-lab CODEX inventory; clones/conjugations confirmed at project scoping._
