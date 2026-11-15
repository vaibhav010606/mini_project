# 05 Software requirements specification (Review-1)

**Status:** draft v1. The structure follows the usual ISO/IEC/IEEE 29148-style SRS outline.

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements of `logad`, a batch ML pipeline and command-line toolset for log anomaly detection and its evaluation.

### 1.2 Scope

In scope: ingesting public log datasets, parsing, building sequences, leakage-free splitting, training and evaluating classical and deep detectors, robustness and efficiency/energy benchmarks, reporting, and a command-line replay demo.

Out of scope: web or mobile applications, databases, production deployment, and processing of private or customer logs (course rules).

### 1.3 Definitions

| Term | Meaning |
|---|---|
| Log message | One raw line with a timestamp |
| Template / event | The constant part of a message after parsing, identified by an event ID |
| Novel template | A message that matches no template learned from training data |
| Session | All messages sharing an identifier (for example HDFS `block_id`) |
| Window | A fixed, non-overlapping block of messages or time |
| Anomalous sequence | A sequence containing at least one anomalous message |
| FAR | False-alert rate, FP / (FP + TN) |
| Chronological split | Train, validation and test periods in time order, with no overlap |

### 1.4 References

[00 Execution plan](00_execution_plan.md), [02 Literature survey](02_literature_survey.md), [Loghub](https://github.com/logpai/loghub), Le & Zhang (ICSE 2022).

## 2. Overall description

- **Product perspective.** A stand-alone batch pipeline plus a `replay` command. It mimics the detection stage of an AIOps tool but is not connected to any live system.
- **Product functions.** Download, parse, build sequences, split, train, evaluate, perturb, benchmark, report, replay.
- **User classes.** (a) A student or researcher running experiments; (b) a reviewer reproducing the results; (c) the intended beneficiary persona, an on-call engineer who needs few false alarms.
- **Operating environment.** Windows 11, Linux and Google Colab; Python 3.10 or newer (3.11 recommended); CPU, with an optional CUDA GPU.
- **Constraints.** Course rules (no web or mobile app, no database, public data); a fixed semester; free-tier compute.
- **Assumptions and dependencies.** Loghub stays available on Zenodo; its labels are usable ground truth; PyTorch, Drain3, sentence-transformers and CodeCarbon install on the target machines.

## 3. Specific requirements

### 3.1 Functional requirements

| ID | Requirement | Priority | Acceptance test |
|---|---|---|---|
| FR1 | Download Loghub datasets, verify checksums, and keep raw data out of git | Must | Check script passes on a clean machine |
| FR2 | Parse with Drain3: fit on train, match val/test, flag novel templates | Must | Fixture tests; novelty rate reported per split |
| FR3 | Build labelled sequences (sessions or fixed windows) with start times | Must | Counts match the EDA and README figures |
| FR4 | Create chronological and random splits with no overlap | Must | Leakage tests pass |
| FR5 | Provide three representations: IDs, counts, semantic vectors | Must | Shape and type tests |
| FR6 | Train and score at least 4 classical models plus DeepLog-style, CNN, LogRobust-style and the proposed model behind one `Detector` interface | Must | All pass the smoke test |
| FR7 | Choose thresholds on validation only (F1-optimal and false-alert-budget modes) | Must | Test labels are never used |
| FR8 | Compute metrics and confidence intervals and save per-run JSON/CSV | Must | Values match hand-computed cases |
| FR9 | Generate seeded perturbations (replace, delete, duplicate, reword) | Must | Rate and label-preservation tests |
| FR10 | Measure latency, throughput, memory, parameters and energy/CO2e | Must | Output contains every field |
| FR11 | `replay` streams a log file and prints alerts with scores and the most surprising events | Should | Works on the bundled sample |
| FR12 | One command regenerates all tables and figures from configs | Must | Clean-clone run |

### 3.2 External interfaces

- **Command line:** `logad download | parse | build | train | evaluate | robustness | bench | replay`, each driven by a YAML config.
- **Inputs:** raw Loghub log files and their label files.
- **Outputs:** `sequences.parquet`, `results/<run_id>.json`, CSV tables and PNG figures.

### 3.3 Non-functional requirements

| ID | Attribute | Requirement | Verification |
|---|---|---|---|
| NFR1 | Reproducibility | Fixed seeds, pinned dependencies, config hash per run; a rerun is within 0.5 F1 points (document GPU non-determinism) | Rerun test |
| NFR2 | Performance | Initial targets, to revisit after week 3: HDFS preprocessing within 60 minutes on a laptop CPU; SemLite-F p95 latency within 20 ms per sequence at batch 1 on CPU | `bench` output |
| NFR3 | Memory | Peak RAM within 8 GB using chunked reads | Measured in `bench` |
| NFR4 | Portability | Windows 11, Linux and Colab; Python 3.11 | CI matrix |
| NFR5 | Maintainability | Type hints, docstrings, `ruff` clean, coverage at least 80% | CI |
| NFR6 | Security and privacy | No raw logs or secrets in git; data fetched by script; licences respected | Review checklist |
| NFR7 | Usability | README quick start in 10 commands or fewer; clear CLI errors | Fresh-machine run |
| NFR8 | Explainability | Each alert lists the sequence ID, the score and the most surprising events | `replay` output |
| NFR9 | Environmental | Energy and CO2e logged for every training run | Results JSON |
| NFR10 | Documentation | Every module documented; results traceable to a config | Review checklist |

### 3.4 Data requirements

- Datasets: HDFS_v1 and BGL (primary), Thunderbird subset and OpenStack (optional). See [data/README.md](../data/README.md).
- Raw data stays outside git. Processed data are Parquet files under the git-ignored `data/` directory.

## 4. Traceability

| Research question | Requirements | Experiments | Tests |
|---|---|---|---|
| RQ1 | FR2, FR3, FR4, FR7, FR8 | E0, E1 | Parser, split and threshold leakage tests |
| RQ2 | FR5-FR8 | E2 | Metric and model tests |
| RQ3 | FR5, FR9 | E3, E5 | Perturbation tests |
| RQ4 | FR10, NFR9 | E4 | Efficiency-harness test |
| All | FR12, NFR1 | All | End-to-end smoke test |

## 5. Open issues

- Confirm the HDFS timestamps and the BGL label format (week 1).
- Fix the NFR2 targets after the week-3 benchmark.
- Decide whether the optional datasets are in scope.
