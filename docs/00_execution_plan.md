# Execution plan: log anomaly detection

**Status:** draft v1, 2026-11-15
**Working title:** Leakage-free, robustness- and energy-aware log anomaly detection, with a lightweight semantic detector

**Assumptions** (edit if they are wrong):

- A 14-week semester, with Review-1 near week 6 and Review-2 near week 14.
- A team of 3 (the roles merge for 2).
- Windows laptops plus a free Colab/Kaggle GPU; Python 3.11 or newer.
- The project guide approves the topic in week 1.

---

## 1. Project definition

**Problem.** Large systems write millions of log lines a day. People cannot read them, and fixed alert rules either miss faults or flood on-call engineers. The task is to flag anomalous log sequences early, with few false alarms, without letting test information leak into training.

**Fit with the course rules.**

- ML/DL is the core, written in Python.
- There is no web or mobile app and no database: the data are files and the interface is a command line.
- It uses public data only, so it is not an internship project.
- It compares 6+ methods from the literature (CO1) and turns them into a working pipeline (CO2). Teamwork evidence for CO3 is the contribution matrix, the [meeting log](meeting_log.md) and the pull-request history.

**Research questions**

- **RQ1 Protocol.** How much do scores shrink under a chronological split with the parser fitted on training data only? Le & Zhang report DeepLog's BGL F1 falling from 0.927 (random split) to 0.426 (chronological) with 1-hour windows. Reproducing that direction is the first check (E0).
- **RQ2 Comparison.** Which model gives the best F1, PR-AUC and recall at a fixed false-alert rate on HDFS and BGL?
- **RQ3 Robustness.** How do models degrade when log statements change (unseen templates, noisy events)? Expectation: index-based models degrade faster than semantic ones.
- **RQ4 Cost.** What do latency, memory and energy/CO2e cost per model?

**What is already done versus what is yours.** Le & Zhang already study training-data selection, grouping, class imbalance, label noise, parsers and early detection. Candidate contributions, to confirm in the [literature survey](02_literature_survey.md):

1. A strict protocol (chronological split plus train-only parser), including HDFS. The paper says HDFS has no timestamps and leaves it out of the chronological study. The raw lines are believed to carry them, so verify in week 1.
2. A false-alert-budget metric.
3. Perturbation-based robustness tests.
4. A latency and energy benchmark.
5. A lightweight semantic detector (SemLite-F) with ablations.

---

## 2. Rubric to deliverables

| Rubric item | Deliverable | Week |
|---|---|---|
| **Review-1 (20 marks)** | | |
| Preliminary study | [01_preliminary_study.md](01_preliminary_study.md): background, dataset EDA, baseline v0 results | 1-4 |
| Literature survey | [02_literature_survey.md](02_literature_survey.md): at least 20 papers with a comparison table | 2-3 |
| Problem formulation and tools | [03_problem_formulation.md](03_problem_formulation.md) and [04_tools_log.md](04_tools_log.md) | 3 |
| SRS, functional and non-functional requirements | [05_SRS.md](05_SRS.md) | 4 |
| High-level design | [06_HLD.md](06_HLD.md) | 4-5 |
| Documentation and presentation | Review-1 report (PDF) and 12 slides | 5-6 |
| **Review-2 (30 marks)** | | |
| Low-level design | `07_LLD.md` (draft in section 7 below) | 7 |
| Implementation | `src/logad/`, configs, CLI | 7-12 |
| Testing | `tests/`, CI, `08_test_report.md` | 7-13 |
| Experiment results and analysis | `results/`, `09_results_analysis.md` | 8-12 |
| Environmental and social context | `10_environment_social.md` (plan in section 11), `model_card.md` | 13 |
| Documentation and presentation | Final report, 15 slides, 3-minute CLI demo, viva prep | 13-14 |

---

## 3. Team and workflow

- **Three people**
  - *Data and infra:* ingestion, parsing, features, CI, tests.
  - *Modelling:* classical, deep and proposed models, ablations.
  - *Evaluation and docs:* metrics, robustness, efficiency and energy, report, slides.
- **Two people:** A takes data, evaluation and tests; B takes models, docs and the tools log.
- **Everyone:** reviews each other's pull requests, owns at least two document sections, and presents in at least one review.
- **Rhythm:** a weekly 30-minute sync recorded in [meeting_log.md](meeting_log.md); pull requests with one reviewer; conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`); tags `review1`, `results-v1` and `review2`.
- **Originality:** write in your own words and cite every paper and piece of code you use. LogADEmpirical is MIT-licensed; keep its notice if you copy anything.

---

## 4. Data and protocol

| Dataset | Size | Labels | Role |
|---|---|---|---|
| HDFS_v1 | 1.47 GiB, 11,175,629 lines, 38.7 h | 575,061 block sessions, 16,838 anomalous (2.93%) | Primary |
| BGL | 708.76 MiB, 4,747,963 lines, 214.7 days | 348,460 anomalous messages (7.34%) | Primary |
| Thunderbird | 29.6 GiB, 211,212,192 lines | Per message | Optional: first 10M lines only |
| OpenStack | 58.6 MiB, 207,820 lines | Labelled | Optional smoke test |

Sizes come from the Loghub README; counts come from Le & Zhang's dataset table.

- **Source.** Download from the Zenodo links in [Loghub](https://github.com/logpai/loghub), record checksums in [data/README.md](../data/README.md), and never commit raw data. Spirit is not in Loghub's table, so skip it.
- **Sequences.** HDFS: one sequence per `block_id`. BGL: non-overlapping windows of 100 messages (primary) plus 1-hour windows (secondary, for the E0 reproduction check). A sequence is anomalous if any message in it is.
- **Splits.** Chronological 70/10/20 (train/val/test) by sequence start time. Use val only for thresholds and early stopping, and touch test only for final runs. Use a random 80/20 split only as the RQ1 contrast.
- **Parser.** Drain3: train with `add_log_message`, infer with `match`. Start from the defaults (depth 4, similarity 0.4) and tune on a hand-labelled 2k-line sample. Fit on the train split. A val/test message that matches no learned template is flagged *novel* and gets a new ID outside the training vocabulary. Report the novel-template rate per split. Expect almost no effect on HDFS (48 event types in the paper) and a larger one on BGL (1,847).
- **Training sets.** Semi-supervised models (DeepLog-style, SemLite-F) train on normal training sequences only. Supervised models use the labelled training sequences.

---

## 5. Method

The architecture diagram and component list are in [06_HLD.md](06_HLD.md).

### Models

| Tier | Model | Input | Supervision |
|---|---|---|---|
| Classical | PCA residual, Isolation Forest | Event counts | Unsupervised |
| Classical | Logistic regression, Random Forest | Event counts | Supervised |
| Deep | DeepLog-style (2-layer LSTM, 128 units, next-event top-g rule) | Event IDs | Normal only |
| Deep | CNN (3 conv layers + max-pool) | Semantic vectors | Supervised |
| Deep | LogRobust-style (2-layer BiLSTM, 128 units, attention) | Semantic vectors | Supervised |
| **Proposed** | **SemLite-F** | Frozen MiniLM template embeddings | Normal only |
| Stretch | LogAnomaly, PLELog, LogBERT | n/a | Authors' code only |

- Layer sizes follow the settings Le & Zhang report.
- Semantic vectors come from embedding the unique template text with `all-MiniLM-L6-v2` (about 22M parameters, 384 dimensions; check the model card). Only hundreds to thousands of templates need embedding, so it is cheap.
- **SemLite-F** is a small GRU or Transformer that forecasts the next template's embedding. The score is the cosine distance to the actual next template. A reworded or unseen template still has a meaningful embedding, whereas an index model can only mark it unknown.
- Write the models yourselves in current PyTorch. [LogADEmpirical](https://github.com/LogIntelligence/LogADEmpirical) (MIT) pins PyTorch 1.7.0 and an NVIDIA GPU, and its README points to a `dev` branch, so use it only to cross-check numbers.

### Metrics

- Anomaly-class precision, recall, F1 and specificity (Le & Zhang recommend adding specificity), plus PR-AUC and MCC.
- Recall at a false-alert rate of at most 1% and at most 0.1%. This is the number an on-call engineer cares about.
- Thresholds are fixed on val. Use 5 seeds (mean and standard deviation) and a bootstrap 95% CI for the top models. Use non-overlapping test windows.

### Experiments

| ID | Purpose | Design | Priority |
|---|---|---|---|
| E0 | Sanity | Reproduce the direction of the paper: DeepLog on BGL 1-hour windows, random far above chronological; good models reach F1 above 0.9 on HDFS | Must |
| E1 | RQ1 | {random, chronological, chronological + train-only parser} x {Random Forest, DeepLog-style, SemLite-F} | Must |
| E2 | RQ2 | All models, strict protocol, both datasets, 5 seeds | Must |
| E3 | RQ3 | Replace, delete or duplicate events at 5-30%. Also reword template text, which gives a new ID. Keep thresholds fixed | Must |
| E4 | RQ4 | Parameters, size, CPU p50/p95 latency at batch 1, throughput at batch 256, peak RAM, training time, energy and CO2e | Must |
| E5 | Ablation | SemLite-F without augmentation; ID target vs embedding target; GRU vs Transformer; MiniLM vs fastText; score aggregation | Must |
| EA | Error analysis | Inspect 30 false positives and 30 false negatives per dataset; categorise the causes | Must |
| E6 | Early detection | Score prefixes at 25/50/75/100% of each sequence | Should |
| E7 | Label budget | Train supervised models on 1/5/20/100% of the anomalies | Should |

### Compute

- Preprocess on the laptop with chunked reads and Parquet files, within 8 GB of RAM.
- Train classical models on CPU and the deep models on a Colab/Kaggle T4.
- In week 3, time one epoch of each model and set a GPU-hour budget before launching any grid.

---

## 6. Requirements

The functional (FR1-FR12) and non-functional (NFR1-NFR10) requirements, with acceptance tests and a traceability matrix, are in [05_SRS.md](05_SRS.md).

---

## 7. Low-level design draft

This section becomes `07_LLD.md` in week 7.

```text
mini_project/
  README.md  pyproject.toml  .gitignore  .gitattributes           (exist)
  .github/workflows/ci.yml  .github/pull_request_template.md       (exist)
  data/README.md  docs/                                            (exist; datasets are git-ignored)
  src/logad/seed.py  tests/test_seed.py                            (exist)
  configs/{data,model,experiment}/*.yaml                           (planned)
  src/logad/data/       download.py loghub.py sequences.py splits.py
  src/logad/parsing/    drain.py novelty.py
  src/logad/features/   ids.py counts.py semantic.py
  src/logad/models/     base.py classical.py deeplog.py cnn.py attn_bilstm.py semlite.py
  src/logad/eval/       metrics.py threshold.py robustness.py early.py efficiency.py energy.py
  src/logad/cli.py  config.py                                      (planned)
  scripts/reproduce.py  results/  notebooks/                       (planned)
```

- **Interfaces.**
  - `Sequence(seq_id, event_ids, t_start, label)`.
  - `Detector.fit(train, val)` and `Detector.score(seqs) -> float[]`, where a higher score means more anomalous.
  - `choose_threshold(scores, y, mode)` and `evaluate(scores, y, threshold)`.
- **Data schema.** `sequences.parquet` holds `seq_id, t_start, event_ids, label, split`. Templates are stored once, with their embeddings.
- **CLI.** `logad download | parse | build | train | evaluate | robustness | bench | replay`, driven by YAML configs. A run ID is the config hash plus the seed.
- **Tracking.** Plain JSON/CSV results, with no database. MLflow is optional.

---

## 8. Testing plan

Aim for at least 30 meaningful tests. CI enforces 80% coverage.

- **Parser:** fixture lines give the expected templates; train-only fitting never sees val or test lines; novel templates are flagged.
- **Sequences and splits:** window counts are correct and the label rule holds; `max(train t) <= min(val t) <= min(test t)`; no sequence is in two splits.
- **Metrics:** P/R/F1/MCC match hand-computed values; budgeted recall is right on a tiny case; thresholds come from val only.
- **Models:** output shapes are right; loss falls on a tiny overfit batch; the same seed gives the same scores; a saved model reloads; unseen templates do not crash.
- **Robustness:** the perturbation rate is respected, labels are unchanged, and runs are seeded.
- **End to end:** a 2k-line bundled sample runs in under 60 seconds on CPU.
- **CI:** GitHub Actions runs `ruff`, `pytest` and coverage on Windows and Linux.
- **Tripwire:** E0 doubles as a regression check. If random and chronological splits give no gap on BGL, suspect a pipeline bug.

---

## 9. Timeline

| Week | Work | Exit criterion |
|---|---|---|
| 1 | Repo and CI skeleton, guide approval, download HDFS/BGL, EDA, read 5 core papers | Line counts match; HDFS timestamps and BGL label field checked |
| 2 | Survey table (12+ papers), Drain3 on both datasets, tool mini-exercises | Templates saved; parse time measured |
| 3 | Sequences, labels, chronological split, problem formulation, GPU budget | Leakage tests pass; time-per-epoch table |
| 4 | Classical baselines on both datasets, SRS, HLD | Baseline table v0 |
| 5 | Review-1 report, slides, dry run, guide feedback | Report v1 |
| 6 | **Review-1** presentation, fix feedback | Tag `review1` |
| 7 | LLD, DeepLog-style model, pipeline tests | E0 reproduced |
| 8 | CNN, LogRobust-style, thresholds and metrics, E2 on HDFS | One full run per model |
| 9 | BGL runs, E1 | E1 table |
| 10 | SemLite-F, E5 ablations | Ablation table |
| 11 | E3 robustness, E4 latency and energy | Robustness curves, Pareto plot |
| 12 | E6/E7, 5-seed reruns, error analysis, freeze results | Tag `results-v1` |
| 13 | `replay` demo, environment/social write-up, test report, model card, final report | README quick start works on a fresh machine |
| 14 | **Review-2** slides, rehearsals, viva prep, submit | Tag `review2` |

If your dates differ, keep the order and shrink weeks 1-4. Either way, get the classical baselines in before Review-1.

---

## 10. Presentations and viva

- **Review-1 slides (12):** title; why logs and AIOps matter; problem and scope; literature map; gap and RQs; data and EDA; baseline v0; FR/NFR highlights; HLD; tools; plan and roles; risks and expected outcomes.
- **Review-2 slides (15), plus a live `replay` demo:** recap; LLD; implementation; tests and coverage; protocol; E1; E2; E3; E4/E5; ablation; error analysis; environment and social; limitations; conclusion; future work.
- **Likely viva questions:**
  - Why F1 on the anomaly class rather than accuracy?
  - Why a chronological split?
  - Why fit the parser on train only?
  - How is the threshold chosen, and what happens when logs change?
  - Why LSTM or GRU rather than an LLM?
  - What does a false-alert budget mean to an on-call engineer?
  - How reliable is your carbon estimate?
  - What privacy risks do logs carry?
  - What would break in production?

---

## 11. Environmental and social context plan

This becomes `10_environment_social.md` and `model_card.md` in week 13.

- **Energy.**
  - Log energy and CO2e for every training and benchmark run with [CodeCarbon](https://docs.codecarbon.io/latest/how-to/transformers/), and report the project's total.
  - Treat the numbers as estimates: published comparisons find that software energy tools can be off by tens of percent.
  - Plot F1 against energy and latency, cap hyperparameter search at a fixed trial budget, and cache embeddings.
  - Do not invent numbers for downtime or waste avoided. Say qualitatively that earlier detection can reduce them.
- **People.**
  - Outages affect the people who depend on the services, and false alarms cause alert fatigue. The false-alert-budget metric makes that visible.
  - Logs can contain user and host identifiers, and Loghub says its logs are, where possible, not sanitised. Keep raw logs out of git, anonymise anything you collect, and say so in the model card.
  - The data are old Hadoop and supercomputer logs, so do not claim the results generalise.
  - Alerts are decision support for a human, and log monitoring must not be used to profile individuals.
- **Deliverables:** `10_environment_social.md` and `model_card.md` (intended use, out-of-scope use, data, metrics, limitations).

---

## 12. Risks and cut order

| Risk | Mitigation |
|---|---|
| Thunderbird is too large | Use the first 10M lines or drop it; HDFS and BGL are enough |
| Your numbers differ from the papers | Expected, since protocols differ. Report the direction and explain |
| The proposed model does not win | Still a valid result, and the ablations explain it. Fallback: fuse DeepLog-style and count-vector scores |
| The reference repo will not install | Use your own PyTorch 2.x code and cross-check on Colab |
| Label noise or parser choice | Document under threats to validity; run one alternative-parser check |
| Compute overrun | Week-3 budget plus the cut order below |
| A teammate is unavailable | Pair on each module; PR reviews spread the knowledge |

**Cut order:** Thunderbird and OpenStack, then LogAnomaly/PLELog/LogBERT/LLM baselines, then E7, E6, the replay demo, and the Transformer ablation.

**Never cut:** the leakage-free protocol, tests, results analysis, the environment and social section, and documentation.

---

## 13. First-week checklist

- [ ] Fill in the team table in the README and agree roles and a meeting slot.
- [ ] Get the guide's approval on title and scope (no UI, no database, public data).
- [ ] Download HDFS_v1 and BGL, and record checksums in `data/README.md`.
- [ ] EDA: confirm 11,175,629 and 4,747,963 lines, check the HDFS timestamps and the BGL label field.
- [ ] Read Le & Zhang, DeepLog, LogRobust, Drain and the Loghub paper; start the survey table.
- [ ] Time Drain3 on a 100k-line sample.
- [ ] Install `pip install -e ".[dev,ml]"` and confirm `ruff check .` and `pytest` pass.
- [ ] Decide a licence for the repository with your guide.

---

## 14. Verification notes

Checked against public sources on 2026-11-15:

- Loghub dataset sizes and line counts.
- Le & Zhang's dataset statistics, setup and findings (arXiv HTML version).
- Existence and bibliographic details of the papers in the [literature survey](02_literature_survey.md).
- LogADEmpirical's licence (MIT) and requirements (PyTorch 1.7.0, NVIDIA GPU, README pointing to a `dev` branch).
- Drain3 behaviour: train with `add_log_message`, infer with `match`, defaults of similarity 0.4 and depth 4.

Not checked:

- The contents of the Zenodo archives (label files, timestamps) and the BGL label format.
- Drain3's latest version, the `all-MiniLM-L6-v2` model size, and free-tier GPU limits.
- The classic papers listed as unverified in the literature survey.
