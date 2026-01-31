#!/usr/bin/env bash
set -euo pipefail

# Build a standalone Linux GUI app with Nuitka.
# Usage: ./build_nuitka.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 -m nuitka \
  --standalone \
  --enable-plugin=tk-inter \
  --enable-plugin=matplotlib \
  --include-package-data=infinite_discoveries \
  --include-data-file=ID_CE-banner.png=ID_CE-banner.png \
  --output-dir=dist/nuitka \
  infinite_discoveries/__main__.py
