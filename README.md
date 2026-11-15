# Log anomaly detection (ML mini project)

[![CI](https://github.com/vaibhav010606/mini_project/actions/workflows/ci.yml/badge.svg)](https://github.com/vaibhav010606/mini_project/actions/workflows/ci.yml)

Detecting anomalous behaviour in system logs with classical machine learning and deep learning, evaluated with a protocol that keeps test information out of training.

Working title: *Leakage-free, robustness- and energy-aware log anomaly detection, with a lightweight semantic detector.*

**Status:** week 1 scaffold. The data pipeline and models are not implemented yet. The schedule, requirements and design drafts are in [`docs/`](docs/).

## Research questions

1. **Protocol.** How much do reported scores shrink under a chronological split with the log parser fitted on training data only?
2. **Comparison.** Which model gives the best F1, PR-AUC and recall at a fixed false-alert rate on HDFS and BGL?
3. **Robustness.** How do models degrade when log statements change, and does a semantic model help?
4. **Cost.** What do latency, memory and energy (CO2e) cost per model?

## Scope

An ML pipeline and command-line tools only. There is no web or mobile app and no database, in line with the course rules. All data is public ([Loghub](https://github.com/logpai/loghub)); see [`data/README.md`](data/README.md). Datasets are never committed.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ruff check .
pytest
```

The deep-learning dependencies (PyTorch, sentence-transformers, Drain3, CodeCarbon) live in an extra, installed with `pip install -e ".[ml]"` once the models land.

## Documentation

| Doc | Purpose |
|---|---|
| [00 Execution plan](docs/00_execution_plan.md) | Master plan: scope, protocol, experiments, timeline, risks |
| [01 Preliminary study](docs/01_preliminary_study.md) | Background, dataset EDA, baseline v0 |
| [02 Literature survey](docs/02_literature_survey.md) | Paper table and reading list |
| [03 Problem formulation](docs/03_problem_formulation.md) | Formal definition, objectives, hypotheses |
| [04 Tools log](docs/04_tools_log.md) | Tools learned, with evidence |
| [05 SRS](docs/05_SRS.md) | Functional and non-functional requirements |
| [06 HLD](docs/06_HLD.md) | Architecture and design decisions |
| [Meeting log](docs/meeting_log.md) | Weekly syncs (teamwork evidence) |

## Layout

```text
src/logad/     package (seed.py now; data/, parsing/, features/, models/, eval/ planned)
tests/         pytest suite, mirrors src/
docs/          plan and review documents
data/          README only; datasets are git-ignored
.github/       CI workflow and pull-request template
```

## Team

TODO: names and roles (see section 3 of the execution plan).

## Licence

TODO: choose a licence with your guide before sharing the code more widely.
