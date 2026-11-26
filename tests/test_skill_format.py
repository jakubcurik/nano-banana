"""Repository checks: SKILL.md follows the Agent Skills format, manifests agree, README links resolve.

Standard library only. Run:  python -m unittest discover -s tests -p "test_skill_format.py"
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "nano-banana"


def frontmatter(text):
    block = re.match(r"---\n(.*?)\n---\n", text, re.S).group(1)
    fields = {}
    key = None
    for line in block.splitlines():
        top = re.match(r"^([a-z-]+):\s*(.*)$", line)
        if top:
            key = top.group(1)
            value = top.group(2)
            fields[key] = "" if value in (">", "|") else value
        elif key == "metadata" and re.match(r"^\s+[a-z-]+:", line):
            nested, _, value = line.strip().partition(":")
            fields["metadata." + nested] = value.strip()
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


class SkillFormatTests(unittest.TestCase):
    def setUp(self):
        self.fields = frontmatter((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))

    def test_name_matches_folder_and_pattern(self):
        name = self.fields["name"]
        self.assertEqual(name, SKILL_DIR.name)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)

    def test_description_length(self):
        self.assertTrue(0 < len(self.fields["description"]) <= 1024, len(self.fields["description"]))

    def test_only_portable_fields(self):
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        top_level = {k for k in self.fields if "." not in k}
        self.assertLessEqual(top_level, allowed)

    def test_compatibility_length(self):
        self.assertLessEqual(len(self.fields["compatibility"]), 500)

    def test_skill_md_stays_short(self):
        lines = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 500)


class ManifestTests(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / ".claude-plugin" / name).read_text(encoding="utf-8"))

    def test_versions_agree(self):
        skill_version = frontmatter((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))["metadata.version"].strip('"')
        self.assertEqual(self.load("plugin.json")["version"], skill_version)

    def test_marketplace_lists_the_plugin(self):
        plugin = self.load("plugin.json")
        marketplace = self.load("marketplace.json")
        self.assertIn(plugin["name"], [p["name"] for p in marketplace["plugins"]])

    def test_icon_exists(self):
        self.assertTrue((ROOT / ".claude-plugin" / "icon.png").is_file())


class ReadmeTests(unittest.TestCase):
    def test_relative_links_and_images_exist(self):
        for readme in [ROOT / "README.md", *sorted((ROOT / "i18n").glob("README.*.md"))]:
            text = readme.read_text(encoding="utf-8")
            targets = re.findall(r'(?:src|href)="([^"#]+)"', text) + re.findall(r"\]\(([^)#\s]+)", text)
            for target in targets:
                if re.match(r"^(https?:|mailto:)", target):
                    continue
                self.assertTrue((readme.parent / target).exists(), f"{readme.name}: missing {target}")


if __name__ == "__main__":
    unittest.main()
