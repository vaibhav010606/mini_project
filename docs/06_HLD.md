# 06 High-level design (Review-1)

**Status:** draft v1.

## 1. Goals and constraints

- Answer RQ1-RQ4 reproducibly on HDFS and BGL.
- Keep test information out of training: the parser, the models and the thresholds.
- A batch pipeline plus command-line tools only. There is no web or mobile UI and no database (course rules).
- Run preprocessing and classical models on a laptop CPU, and the deep models on a free Colab/Kaggle GPU.

## 2. Architecture

```text
Loghub (Zenodo) -> [1 Ingest + checksum] -> raw logs
   -> [2 Parse: Drain3, fit on TRAIN only] -> template IDs + novelty flags
   -> [3 Group + label: sessions / 100-message windows] -> sequences (+ start time)
   -> [4 Chronological split: train | val | test]
   -> [5 Representations: counts | IDs | semantic vectors]
   -> [6 Detectors behind one interface: classical | DeepLog-style | CNN | LogRobust-style | SemLite-F]
   -> [7 Threshold chosen on VAL] -> [8 Evaluate: metrics, robustness, early detection, efficiency, energy]
   -> [9 Reports: tables, figures, model card]          [10 `replay` CLI demo]
```

## 3. Components

| # | Component | Responsibility | Input -> output |
|---|---|---|---|
| 1 | Ingest | Download, verify checksums, read raw logs in chunks | Zenodo archive -> raw log files |
| 2 | Parser | Learn templates on train, match val/test, flag novel templates | Raw lines -> event IDs, novelty flags |
| 3 | Sequencer | Group by session or window; label a sequence anomalous if any message is | Event IDs -> labelled sequences |
| 4 | Splitter | Chronological and random splits, with leakage checks | Sequences -> train/val/test |
| 5 | Featuriser | Event IDs, count vectors, semantic vectors | Sequences -> model inputs |
| 6 | Detector zoo | Fit and score through one `Detector` interface | Inputs -> anomaly scores |
| 7 | Calibrator | Choose a threshold on val (F1-optimal or false-alert budget) | Val scores -> threshold |
| 8 | Evaluator | Metrics, CIs, robustness, early detection, efficiency, energy | Scores -> result files |
| 9 | Reporter | Tables, figures and the model card | Results -> `docs/` and `results/` |
| 10 | Replay | Stream a log file and print alerts | Raw log -> alert lines |

## 4. Data flow and storage

`data/raw/<dataset>` -> `data/processed/<dataset>/parsed.parquet` -> `sequences.parquet` -> `results/<run_id>.json` and figures. All of these are files; there is no database. A run ID is the config hash plus the seed.

## 5. Technology stack

| Layer | Choice |
|---|---|
| Language | Python 3.11 |
| Parsing | Drain3 |
| Classical ML | scikit-learn |
| Deep learning | PyTorch 2.x |
| Template embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Data | pandas, pyarrow (Parquet) |
| Energy | CodeCarbon |
| Quality | pytest, pytest-cov, ruff, GitHub Actions |

## 6. Design decisions

| ID | Decision | Alternatives considered | Why |
|---|---|---|---|
| D1 | Drain3 parser, behind an interface | Spell, AEL, IPLoM (compared by Le & Zhang), parsing-free methods | Online, has a train/`match` split that suits the no-leakage rule; the interface allows one sensitivity check |
| D2 | Sessions for HDFS, non-overlapping 100-message windows for BGL (1-hour windows as a secondary check) | Sliding windows | Non-overlapping test windows avoid double counting and correlated bootstrap samples |
| D3 | Chronological 70/10/20 split | Random split | Random splits inflate semi-supervised results (Le & Zhang); random is kept only for the RQ1 contrast |
| D4 | Own PyTorch 2.x implementations | Reuse LogADEmpirical directly | That repo pins PyTorch 1.7.0; writing the models shows understanding and avoids install problems |
| D5 | Frozen `all-MiniLM-L6-v2` template embeddings | fastText (used by Le & Zhang) | Cheap, because only unique templates are embedded; the choice is ablated in E5 |
| D6 | Files and a CLI, no database or web UI | Dashboard or web app | Course rules |
| D7 | Thresholds chosen on val only, in two modes | Threshold tuned on test | Prevents leakage; the false-alert-budget mode reflects on-call practice |

## 7. Quality attributes

| Attribute | How the design supports it |
|---|---|
| Reproducibility | Seeds, config hashes, pinned dependencies at the results freeze, one-command rebuild (FR12) |
| Leakage safety | Split and parser checks are unit tests, and E0 is a regression tripwire |
| Efficiency | Chunked reads, Parquet, embedding only unique templates, small models |
| Explainability | `replay` shows the most surprising events per alert |

## 8. Open design questions

- Does `match` leave enough templates matched on BGL, or is a looser similarity threshold needed?
- Should SemLite-F use a GRU or a Transformer (decide from the E5 ablation)?
- How should novel templates be handled by the count-vector models (an extra UNK bucket)?
