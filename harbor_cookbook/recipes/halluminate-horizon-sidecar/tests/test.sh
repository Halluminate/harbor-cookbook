#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y curl

curl -LsSf https://astral.sh/uv/0.9.7/install.sh | sh
source "$HOME/.local/bin/env"

uv run --with mcp python3 /tests/grade.py
