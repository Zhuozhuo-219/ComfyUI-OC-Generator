# Data Subset

This directory contains the tracked JSON subset used by the current node implementation.

- `data.json`: reduced category tree for the top categories and subcategories used by the shipped nodes
- `tags.json`: reduced prompt entries aligned with `data.json`

Runtime loading now prefers `/data` first and falls back to `/rawdata` only when the tracked subset is missing.

The local `/rawdata` directory remains the broader source dataset for future recuts, but it is intentionally ignored by Git.
