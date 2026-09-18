# Outputs

Each run writes to `outputs/<run_id>/`:

```text
config.resolved.yaml  exact parameters used
metrics.json          machine-readable final metrics
run.json              time, git commit, seed, environment and status
oof.*                 optional out-of-fold predictions (not committed if large)
submission.csv        optional Kaggle submission (usually not committed)
artifacts/             model/operator checkpoints (not committed)
```

Only this README is tracked by default. Promote concise conclusions to
`RESULTS.md`; do not use Git as model storage.

