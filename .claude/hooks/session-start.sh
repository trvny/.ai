#!/usr/bin/env bash
# SessionStart, cloud sessions only. Never fails the session.
# Installs the Python deps the validate workflow uses, so tests/ and tools/
# run without a manual pip install.
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

python3 -c 'import yaml, jsonschema' 2>/dev/null && exit 0
python3 -m pip install -q --disable-pip-version-check pyyaml jsonschema 2>/dev/null \
  || python3 -m pip install -q --disable-pip-version-check --break-system-packages pyyaml jsonschema \
  || echo "pip: pyyaml/jsonschema install failed" >&2

exit 0
