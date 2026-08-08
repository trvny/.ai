#!/usr/bin/env python3
"""Merge a complete YAML profile with one or more partial overlays."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install it with: python -m pip install pyyaml"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "profiles",
        nargs="+",
        type=Path,
        help="Base profile followed by zero or more overlays; later values win",
    )
    parser.add_argument("--output", type=Path, help="Write merged YAML to this file")
    parser.add_argument(
        "--schema",
        type=Path,
        help="Validate the merged profile against this JSON Schema",
    )
    return parser.parse_args()


def load_mapping(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Profile not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise SystemExit(f"Profile root must be a YAML mapping: {path}")
    return raw


def merge_mapping(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge mappings; later scalars and lists replace earlier values."""
    merged = deepcopy(base)
    for key, value in overlay.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = merge_mapping(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def merge_profiles(paths: list[Path]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for path in paths:
        merged = merge_mapping(merged, load_mapping(path))
    return merged


def validate_profile(profile: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "jsonschema is required for --schema. Install it with: "
            "python -m pip install jsonschema"
        ) from exc

    if not schema_path.is_file():
        raise SystemExit(f"Schema not found: {schema_path}")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(profile, schema)
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        raise SystemExit(f"Profile validation failed at {location}: {exc.message}") from exc


def dump_profile(profile: dict[str, Any]) -> str:
    return yaml.safe_dump(
        profile,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )


def main() -> None:
    args = parse_args()
    profile = merge_profiles(args.profiles)
    if args.schema:
        validate_profile(profile, args.schema)
    output = dump_profile(profile)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
