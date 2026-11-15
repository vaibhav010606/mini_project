# 02 Literature survey (Review-1)

**Status:** starter table. The bibliographic details below were checked against public sources on 2026-11-15. The *Key result* and *Limitations / gap* columns are for you to fill by reading each paper (TODO). Target: at least 20 papers and a written synthesis.

## How to use this file

1. Read the week-1 papers first: rows 1, 2, 3, 7 and 8.
2. For every paper, fill in the key result (with the number and the dataset), what it assumes, and what it does not test.
3. Write the synthesis only after the table is complete.

## A. Core papers

| # | Paper | Venue, year | Method | Supervision | Datasets | Key result | Limitations / gap |
|---|---|---|---|---|---|---|---|
| 1 | Le & Zhang, [Log-based Anomaly Detection with Deep Learning: How Far Are We?](https://arxiv.org/abs/2202.04301) | ICSE 2022 | Empirical study of DeepLog, LogAnomaly, PLELog, LogRobust and CNN | n/a | HDFS, BGL, Spirit, Thunderbird | Random training-data selection inflates semi-supervised results (DeepLog, BGL, 1-hour windows: F1 0.927 random vs 0.426 chronological) | Five models with public code and four datasets, per the paper |
| 2 | Du et al., [DeepLog](https://users.cs.utah.edu/~lifeifei/papers/deeplog.pdf) | CCS 2017 | LSTM models the log as a sequence and predicts the next event; per-entry detection; workflow construction for diagnosis; online update from feedback | Semi-supervised (normal data) | TODO | TODO | TODO |
| 3 | Zhang et al., [Robust Log-based Anomaly Detection on Unstable Log Data (LogRobust)](https://doi.org/10.1145/3338906.3338931) | ESEC/FSE 2019 | Semantic vectors for log events plus an attention-based Bi-LSTM; targets unstable logs | Supervised | Hadoop, a Microsoft online service | TODO | Parsing sensitivity is discussed in row 9; TODO |
| 4 | Meng et al., [LogAnomaly](https://www.ijcai.org/proceedings/2019/658) | IJCAI 2019 | template2vec semantic vectors; detects sequential and quantitative anomalies; merges new templates | Titled unsupervised; Le & Zhang group it as semi-supervised | Two public datasets (HDFS among them) | TODO | TODO |
| 5 | Yang et al., [PLELog](https://2021.icse-conferences.org/details/icse-2021-papers/85/Semi-supervised-Log-based-Anomaly-Detection-via-Probabilistic-Label-Estimation) | ICSE 2021 | Probabilistic label estimation plus an attention-based GRU on semantic embeddings | Semi-supervised | HDFS, BGL | Authors report an average 181.6% F1 improvement over compared approaches | TODO |
| 6 | Guo, Yuan, Wu, [LogBERT](https://arxiv.org/abs/2103.04475) | IJCNN 2021 | Self-supervised BERT trained on normal sequences with masked log-key prediction and volume-of-hypersphere minimisation | Self-supervised (normal logs) | Three log datasets (see paper) | Authors report it outperforms the compared methods | TODO |
| 7 | He et al., [Drain](https://pinjiahe.github.io/files/pdf/research/ICWS17.pdf) | ICWS 2017 | Online log parsing with a fixed-depth parse tree | n/a (parser) | Five real-world datasets, over 10M messages | Authors report the best accuracy on four of five datasets and 51.85-81.47% faster than the compared online parser | TODO |
| 8 | Zhu et al., [Loghub](https://arxiv.org/abs/2008.06448) | arXiv 2008.06448 (ISSRE 2023 per the repository) | 19 real-world log datasets for AI-driven log analytics | n/a | n/a | Authors report about 90,000 downloads | Logs are, where possible, not sanitised |
| 9 | [Log-based Anomaly Detection Without Log Parsing](https://arxiv.org/abs/2108.01955) | arXiv 2108.01955 (authors and venue: verify) | Parsing-free detection | TODO | TODO | TODO | Reports that LogRobust depends on parsing quality (confirm in the paper) |
| 10 | Landauer et al., [Deep Learning for Anomaly Detection in Log Data: A Survey](https://arxiv.org/abs/2207.03820) | Machine Learning with Applications 12, 2023 | Systematic review of models, preprocessing, techniques and evaluations | n/a | n/a | No quantitative comparison of approaches | TODO |
| 11 | He et al., [A Survey on Automated Log Analysis for Reliability Engineering](https://arxiv.org/abs/2009.07237) | ACM Computing Surveys 54(6), 2021 | Surveys 158 papers across logging, compression, parsing and mining | n/a | n/a | n/a | TODO |

## B. LLM-era papers

Two different papers are both called LogGPT, so always cite them by arXiv ID.

| # | Paper | Notes (confirm in the paper) |
|---|---|---|
| 12 | [LogPrompt: Interpretable Online Log Analysis Using Large Language Models with Prompt Strategies](https://arxiv.org/abs/2308.07610) | Experiments with ChatGPT on nine log datasets; chronological splits |
| 13 | [LogGPT: Log Anomaly Detection via GPT](https://arxiv.org/abs/2309.14482) | Evaluates on HDFS, BGL and Thunderbird |
| 14 | [LogGPT: Exploring ChatGPT for Log-Based Anomaly Detection](https://arxiv.org/abs/2309.01189) | Tests ChatGPT on BGL and Spirit against DeepLog, LogAnomaly and LogRobust |
| 15 | [LLM-Enhanced Log Anomaly Detection: A Comprehensive Benchmark](https://arxiv.org/abs/2604.12218) | 2026 benchmark of traditional pipelines, fine-tuned transformers and prompt-based LLMs on HDFS, BGL, Thunderbird and Spirit |

## C. Energy and efficiency (for the environmental section)

| # | Paper | Notes |
|---|---|---|
| 16 | Wang et al., [Energy and Carbon Considerations of Fine-Tuning BERT](https://arxiv.org/abs/2311.10267) | Measurement methods and a DistilBERT-style efficiency comparison |
| 17 | Strubell et al., Energy and Policy Considerations for Deep Learning in NLP (arXiv 1906.02243, ACL 2019) | Verify the details before citing |

## D. Classic papers to read (not verified on 2026-11-15; confirm details before citing)

- Xu et al., SOSP 2009: mining console logs with PCA; origin of the HDFS data.
- Oliner and Stearley, DSN 2007, "What supercomputers say": origin of the BGL, Thunderbird and Spirit logs.
- He et al., ISSRE 2016: experience report on system log analysis for anomaly detection.
- Lu et al., 2018: convolutional neural network for log anomaly detection.
- Chen et al., 2021: experience report on deep-learning-based log analysis.
- Loghub-2.0 (ISSTA 2024), referenced in the Loghub README.

## E. Synthesis outline (write after the table is complete)

1. Pipeline stages: parsing, grouping, representation, detection.
2. Supervision regimes and what each assumes about labels.
3. Representations: event index, counts, semantic vectors, parsing-free.
4. Evaluation pitfalls: random splits, grouping choice, imbalance, label noise, parser choice.
5. The LLM era and its cost and latency.
6. The efficiency and energy gap in the literature.

## F. Gap statement (draft 3 bullets, each tied to table rows)

- TODO
- TODO
- TODO
