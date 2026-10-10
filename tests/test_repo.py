import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = [
    "replica-architect",
    "replica-backend",
    "replica-brand",
    "replica-build",
    "replica-deploy",
    "replica-design",
    "replica-diff",
    "replica-entrepreneur",
    "replica-launch",
    "replica-recon",
    "replica-test",
    "replica-workflow",
]


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


class Repo(unittest.TestCase):
    def test_twelve_skills_in_agents_directory(self):
        found = sorted(
            d for d in os.listdir(SKILLS_DIR)
            if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
        )
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 200, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 50, s)

    def test_native_agents_has_no_claude_manifest(self):
        agents_dir = os.path.dirname(SKILLS_DIR)
        self.assertFalse(
            os.path.exists(os.path.join(agents_dir, ".claude-plugin")),
            "Claude plugin manifest must not be in .agents directory"
        )

    def test_readme_carries_the_reel_copy(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# The Replica skill"))
        for line in (
            "Free, MIT, no signup, no API key, nothing to connect.",
            "One reverse-engineers the app you want to clone. One rebuilds it. One tests it "
            "for bugs. And one is the Entrepreneur: it reads what the app's users hate and "
            "fixes it in yours, so you have an app you can sell.",
            "## Fine print",
        ):
            self.assertIn(line, readme)
        for s in SKILLS:
            self.assertIn("`%s`" % s, readme)

    def test_no_em_dashes_anywhere(self):
        bad = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for fn in filenames:
                if fn.endswith((".md", ".py", ".json", ".ts", ".csv")):
                    path = os.path.join(dirpath, fn)
                    with open(path, encoding="utf-8") as fh:
                        if chr(0x2014) in fh.read():
                            bad.append(os.path.relpath(path, ROOT))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
