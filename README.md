# Deep Past — Translate Akkadian to English

> 推理方案与运行说明： [SOLUTION.md](SOLUTION.md)

Private solution repository for `deep-past-challenge-translate-akkadian-to-english`.

## 1. Objective

- Task: `Akkadian-to-English translation`
- Primary metric: `competition-defined translation score` (`higher/lower is better`)
- Validation: `text/group-aware holdout; confirm split after inspecting data`
- Compute: `Kaggle notebook / GPU as needed`
- Current best: see [RESULTS.md](RESULTS.md)

## 2. Repository boundaries

```text
configs/       versioned experiment parameters; one file per meaningful run
notebooks/     exploration, validation checks, visual diagnostics; not core logic
src/           reusable data, model/operator, training/search, inference code
outputs/       generated run artifacts; only tiny summaries are committed
scripts/       thin shell entrypoints; business logic stays in src/
data/          local/Kaggle inputs; never committed
```

If code is needed by two runs, move it from a notebook into `src/`. A notebook
must not be the only place where the best submission can be reproduced.

## 3. Setup

```bash
python -m pip install -r requirements.txt
export KAGGLE_INPUT_DIR=/kaggle/input/deep-past-challenge-translate-akkadian-to-english
```

Local data may instead be exposed at `./data/raw`.

## 4. Reproduce

Smoke test:

```bash
bash scripts/run.sh configs/smoke.yaml smoke
```

Train/search and validate:

```bash
bash scripts/run.sh configs/base.yaml exp001
```

Generate a submission from a completed run:

```bash
python -m src.submit --run-dir outputs/exp001 \
  --output outputs/exp001/submission.csv
```

The run directory must contain the resolved configuration, metrics, environment
metadata and any lightweight result summary needed to explain the score.

## 5. Validation contract

Before trusting a score, document:

1. split construction and random seed;
2. leakage checks, including duplicate/group/time leakage;
3. exact local metric implementation;
4. whether preprocessing is fitted on train only;
5. public/private leaderboard risks.

## 6. Experiment workflow

1. Copy `configs/base.yaml` to `configs/expNNN_short_name.yaml`.
2. Change one main hypothesis at a time.
3. Run with a unique ID: `expNNN-short-name-sSEED`.
4. Append one row to `experiments.csv` after the run.
5. Promote only decision-relevant runs to `RESULTS.md`.
6. Record leaderboard submissions in `submissions.csv`.

## 7. Kaggle submission checklist

- [ ] submission columns, order and row count match `sample_submission.csv`
- [ ] no NaN/inf or invalid class/range values
- [ ] inference uses the same preprocessing as validation
- [ ] model/operator artifact belongs to the recorded run
- [ ] notebook/package versions and dataset paths are recorded
- [ ] submission is logged in `submissions.csv`

## 8. Status

- Baseline: not run
- Best validation: TBD
- Best public LB: TBD
- Next experiment: establish a leakage-safe baseline

