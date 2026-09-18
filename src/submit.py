from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not (run_dir / "run.json").exists():
        raise FileNotFoundError(f"Unknown run directory: {run_dir}")
    raise SystemExit(
        f"Implement competition-specific inference and write {args.output}. "
        "Validate against sample_submission.csv before saving."
    )


if __name__ == "__main__":
    main()

