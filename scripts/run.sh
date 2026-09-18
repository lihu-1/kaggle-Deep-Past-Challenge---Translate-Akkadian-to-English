#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-configs/base.yaml}"
RUN_ID="${2:-baseline}"

python -m src.run --config "${CONFIG_PATH}" --run-id "${RUN_ID}"

