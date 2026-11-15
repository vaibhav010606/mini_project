# 01 Preliminary study (Review-1)

**Status:** skeleton. Fill it in during weeks 1-4. This is the evidence for the "preliminary study" mark.

## 1. Background

Write 1-2 paragraphs on each, with citations:

- What logs are and how they are produced (logging statements, templates versus parameters).
- Anomaly types: sequential (wrong order or missing events), quantitative (unusual counts), and point anomalies.
- Why detection is hard: volume, class imbalance, scarce labels, log instability (software changes its logging statements), and latency needs.
- Industry practice today: threshold and regex alert rules, observability stacks, AIOps.

## 2. Datasets

Figures below come from public sources (Loghub README, Le & Zhang). Fill the last column from your own EDA.

| Dataset | Lines | Span | Grouping | Anomalies | Your EDA check |
|---|---|---|---|---|---|
| HDFS_v1 | 11,175,629 | 38.7 h | session (`block_id`) | 16,838 of 575,061 sessions (2.93%) | TODO |
| BGL | 4,747,963 | 214.7 days | 100-message windows, 1-hour windows | 348,460 messages (7.34%) | TODO |

EDA to-do list:

- [ ] Confirm the line counts.
- [ ] Check that HDFS lines carry timestamps, and that session start times can be recovered.
- [ ] Identify the BGL label field and how normal messages are marked.
- [ ] Sequence length distributions per dataset.
- [ ] Number of distinct templates after parsing.
- [ ] Anomaly rate over time (is it stable, or does it drift?).

## 3. Parser trial

Run Drain3 on a 100k-line sample of each dataset. Record the number of templates, the parse time, and 5-10 examples of wrong or merged templates.

## 4. Baseline v0 (week 4)

| Model | Dataset | Split | Precision | Recall | F1 | Specificity | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## 5. Observations and questions for the guide

- TODO
