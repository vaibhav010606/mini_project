# 03 Problem formulation (Review-1)

**Status:** draft v1.

## 1. Formal definition

- A log stream `L = (l_1, ..., l_n)` of raw messages, each with a timestamp `t_i`.
- A parser `P` maps each message to an event ID `e_i` in `E ∪ {UNK}`, where `E` is the set of templates learned from **training data only**. A message that matches no learned template is *novel*.
- A grouping `G` (sessions by identifier, or fixed non-overlapping windows) turns the stream into sequences `S_j = (e_j1, ..., e_jm)` with a start time `t_j` and a label `y_j` in `{0, 1}`. `y_j = 1` if any member message is anomalous.
- A detector `f` maps a sequence to a score `s_j = f(S_j)`. An alarm is raised when `s_j >= τ`.
- **No-leakage constraint.** `P` and `f` are fitted on sequences from the training period only. `τ` is chosen on the validation period. Test sequences are strictly later than both.

## 2. Objectives

1. Build a reproducible pipeline that applies the definition above to HDFS and BGL.
2. Compare classical, deep and proposed detectors under that protocol.
3. Quantify how scores change under weaker protocols (random split, parser fitted on all data).
4. Measure robustness to log change, and the latency and energy cost of each model.

## 3. Research questions

- **RQ1.** How much do scores shrink under a chronological split with a train-only parser?
- **RQ2.** Which model gives the best F1, PR-AUC and recall at a fixed false-alert rate?
- **RQ3.** How do models degrade when log statements change, and does a semantic model help?
- **RQ4.** What do latency, memory and energy/CO2e cost per model?

## 4. Hypotheses (expectations to test, not claims)

- **H1.** The strict protocol lowers F1 for semi-supervised models, with a larger drop on BGL than on HDFS.
- **H2.** On HDFS with session grouping, strong models reach F1 above 0.9 (Le & Zhang report this for all models they tested); on BGL under chronological windows, scores are lower and the ranking of models changes.
- **H3.** Models fed semantic vectors degrade more slowly than ID-based models under template rewording and event noise.
- **H4.** SemLite-F gives a better accuracy-per-joule trade-off than the attention-BiLSTM. Fix the margin after the week-8 baselines.

## 5. Success criteria

- E0 reproduces the *direction* of Le & Zhang's random-versus-chronological gap.
- E1-E5 and EA are complete on both datasets, with 5 seeds.
- All FRs pass their acceptance tests (see [05_SRS.md](05_SRS.md)).
- At least 30 tests, CI green, coverage at least 80%.
- Energy and CO2e are recorded for every training run.
- Review-1 and Review-2 reports and slides are submitted.

## 6. Scope and non-goals

- In scope: batch pipeline, evaluation harness, command-line replay demo.
- Out of scope: web or mobile apps, databases, production deployment, private or customer logs, and unsupported claims about real-world impact.

## 7. Assumptions and threats to validity

- Labels in HDFS and BGL are treated as ground truth, but they may contain errors (Le & Zhang show label noise hurts, especially supervised models).
- The logs are old (Hadoop and supercomputer systems), so results may not transfer to modern services.
- The parser choice affects results; one alternative-parser check is planned.
- Only public datasets are used, so there is no evidence about proprietary log formats.
