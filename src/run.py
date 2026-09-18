from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    run_dir = Path(config["run"].get("output_root", "outputs")) / args.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    with open(run_dir / "config.resolved.yaml", "w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, sort_keys=False, allow_unicode=True)

    metadata = {
        "run_id": args.run_id,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "seed": config["run"]["seed"],
        "python": platform.python_version(),
        "platform": platform.platform(),
        "input_dir": os.getenv("KAGGLE_INPUT_DIR", "data/raw"),
        "status": "created",
    }
    (run_dir / "run.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    raise SystemExit(
        "Run scaffold created. Replace this line with the competition pipeline; "
        "keep orchestration here and domain logic in data/model/metric modules."
    )


if __name__ == "__main__":
    main()

