from __future__ import annotations

import json
import re
import sys
import tomllib
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.merge_profile import merge_mapping, merge_profiles, validate_profile
from tools.render_profile import language_for, render


class MergeProfileTests(unittest.TestCase):
    def test_recursive_merge_replaces_lists_and_scalars(self) -> None:
        base = {
            "nested": {"keep": 1, "replace": "old"},
            "items": [1, 2],
        }
        overlay = {
            "nested": {"replace": "new"},
            "items": [3],
        }

        self.assertEqual(
            merge_mapping(base, overlay),
            {
                "nested": {"keep": 1, "replace": "new"},
                "items": [3],
            },
        )
        self.assertEqual(base["nested"]["replace"], "old")
        self.assertEqual(base["items"], [1, 2])

    def test_null_is_an_explicit_overlay_value(self) -> None:
        merged = merge_mapping(
            {"personality": {"modifiers": {"warm": 2, "concise": 1}}},
            {"personality": {"modifiers": {"warm": None}}},
        )

        self.assertIsNone(merged["personality"]["modifiers"]["warm"])
        self.assertEqual(merged["personality"]["modifiers"]["concise"], 1)

    def test_default_profile_and_example_overlay_validate(self) -> None:
        profile = merge_profiles(
            [
                ROOT / "profiles/default.yaml",
                ROOT / "examples/profile.overlay.yaml",
            ]
        )
        validate_profile(profile, ROOT / "schema/style-profile.schema.json")

        self.assertEqual(profile["id"], "my-private-profile")
        self.assertEqual(profile["locale"], "pl-PL")
        self.assertEqual(profile["personality"]["base"], "friendly")
        self.assertEqual(profile["personality"]["modifiers"]["concise"], 2)
        self.assertEqual(profile["personality"]["modifiers"]["honest"], 1)
        self.assertEqual(profile["collaboration"]["verification"], "strict")
        self.assertEqual(profile["collaboration"]["initiative"], "balanced")


class RenderProfileTests(unittest.TestCase):
    @staticmethod
    def rendered(base_level: int | None = 1, modifier_level: int | None = 0) -> str:
        return render(
            {
                "personality": {
                    "base": "cynical",
                    "intensity": base_level,
                    "modifiers": {"cynical": modifier_level, "honest": 0},
                },
                "collaboration": {},
            },
            "en",
        )

    def test_base_and_modifier_intensities_are_distinct(self) -> None:
        self.assertIn("mostly in the background", self.rendered(0))
        self.assertIn("clearly visible", self.rendered(2))
        self.assertIn("strongly shape tone and phrasing", self.rendered(3))
        self.assertIn("Occasionally note hype", self.rendered(1, 1))
        self.assertIn("Notice hype and needless complexity", self.rendered(1, 2))
        self.assertIn("Consistently interrogate hype", self.rendered(1, 3))
        self.assertIn("Do not invent facts", self.rendered(1, 0))

    def test_null_base_intensity_uses_normal_baseline(self) -> None:
        rendered = self.rendered(None)
        self.assertNotIn("mostly in the background", rendered)
        self.assertNotIn("clearly visible", rendered)
        self.assertNotIn("strongly shape tone and phrasing", rendered)

    def test_language_is_inferred_from_locale(self) -> None:
        self.assertEqual(language_for({"locale": "pl-PL"}, "auto"), "pl")
        self.assertEqual(language_for({"locale": "en-US"}, "auto"), "en")
        self.assertEqual(language_for({"locale": "pl-PL"}, "en"), "en")


class RepositoryContractTests(unittest.TestCase):
    def test_provider_entrypoints_are_portable_import_shims(self) -> None:
        for name in ("CLAUDE.md", "GEMINI.md"):
            path = ROOT / name
            self.assertFalse(path.is_symlink(), f"{name} must not require symlink support")
            self.assertEqual(path.read_text(encoding="utf-8"), "@AGENTS.md\n")

    def test_provider_config_files_parse(self) -> None:
        with (ROOT / ".claude/settings.json").open(encoding="utf-8") as handle:
            json.load(handle)
        with (ROOT / ".codex/config.toml").open("rb") as handle:
            tomllib.load(handle)

    def test_codex_secret_filters_are_valid_and_effective(self) -> None:
        with (ROOT / ".codex/config.toml").open("rb") as handle:
            config = tomllib.load(handle)

        policy = config["shell_environment_policy"]
        self.assertNotIn("exclude", policy)
        self.assertNotIn("include_only", policy)

        filters = policy["filters"]
        excluded_patterns = [
            re.compile(pattern)
            for pattern, action in filters.items()
            if action == "exclude"
        ]
        self.assertTrue(excluded_patterns)

        for variable in (
            "OPENAI_API_KEY",
            "GITHUB_TOKEN",
            "ANTHROPIC_API_KEY",
            "CLOUDFLARE_API_TOKEN",
            "MY_SECRET_VALUE",
        ):
            self.assertTrue(
                any(pattern.search(variable) for pattern in excluded_patterns),
                f"expected {variable} to be excluded",
            )

        self.assertFalse(
            any(pattern.search("PATH") for pattern in excluded_patterns),
            "PATH should not be excluded by credential filters",
        )

    def test_published_skill_bundle_is_valid(self) -> None:
        with zipfile.ZipFile(ROOT / "skills/english-polish.skill") as archive:
            self.assertIsNone(archive.testzip())
            names = set(archive.namelist())
            self.assertIn("english-polish/SKILL.md", names)
            self.assertIn("english-polish/agents/openai.yaml", names)


if __name__ == "__main__":
    unittest.main()
