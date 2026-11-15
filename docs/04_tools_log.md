# 04 Tools learning log (Review-1)

**Status:** template. For each tool, do one small exercise, commit the evidence (notebook or script), and record what you learned. This is the evidence for "learning necessary modern tools".

| Tool | Why it is needed here | Mini-exercise (evidence) | Owner | Status |
|---|---|---|---|---|
| Git and GitHub pull requests | Teamwork and review history (CO3) | Open a PR that fixes a typo in the docs and get it reviewed | | TODO |
| `venv` + `pyproject.toml` (editable install) | Reproducible environment | Fresh clone, `pip install -e ".[dev]"`, tests pass | | TODO |
| pandas + pyarrow (Parquet) | Large tables without a database | Load 1M log lines in chunks and save as Parquet | | TODO |
| scikit-learn | Classical baselines | Fit Isolation Forest on count vectors of a toy log | | TODO |
| Drain3 | Log parsing | Parse 100k HDFS lines, plot template frequencies | | TODO |
| PyTorch 2.x | LSTM, GRU, attention models | Train a tiny LSTM next-token model on a toy sequence | | TODO |
| sentence-transformers | Template embeddings (MiniLM) | Embed 50 templates and show nearest neighbours | | TODO |
| CodeCarbon | Energy and CO2e measurement | Wrap a training loop and read `emissions.csv` | | TODO |
| pytest + pytest-cov | Tests and coverage | Write a test with a fixture and read a coverage report | | TODO |
| ruff | Linting | Fix every warning in a small module | | TODO |
| GitHub Actions | CI | Read a failing run and fix it | | TODO |
| Jupyter + matplotlib | EDA and figures only | Reproduce one figure from a script | | TODO |
| Markdown / LaTeX | Reports | Build the Review-1 report PDF | | TODO |
