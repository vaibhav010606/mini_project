# Data

Datasets are **never committed** (see `.gitignore`). Download them locally and record the checksums below.

## Source

[Loghub](https://github.com/logpai/loghub) is a collection of system log datasets hosted on Zenodo (record 8196385). Its page says the datasets are freely available for research or academic work. Cite the Loghub paper when you use them, and read the repository's own terms before any redistribution.

Loghub says that, where possible, the logs are not sanitised, anonymised or modified. Treat them as potentially containing identifiers, and keep raw copies out of git, screenshots and reports.

| Dataset | Raw size | Lines | Span | Role | SHA-256 |
|---|---|---|---|---|---|
| HDFS_v1 | 1.47 GiB | 11,175,629 | 38.7 hours | primary | TODO: record at download |
| BGL | 708.76 MiB | 4,747,963 | 214.7 days | primary | TODO: record at download |
| Thunderbird | 29.60 GiB | 211,212,192 | 244 days | optional (first 10M lines only) | TODO: record at download |
| OpenStack | 58.61 MiB | 207,820 | n/a | optional smoke test | TODO: record at download |

Sizes and line counts come from the Loghub README. Confirm the line counts in your own EDA (week 1).

## Local layout (git-ignored)

```text
data/raw/<dataset>/        downloaded archives and extracted logs
data/processed/<dataset>/  parquet files produced by the pipeline
```
