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


def parse_skill_metadata(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, "", text
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    name = name_m.group(1).strip() if name_m else None
    
    desc_lines = []
    in_desc = False
    for line in fm.splitlines():
        if line.startswith("description:"):
            in_desc = True
            val = line.split("description:", 1)[1].strip()
            if val and val not in (">-", "|-", ">", "|"):
                desc_lines.append(val)
        elif in_desc:
            if re.match(r"^[a-zA-Z0-9_-]+:", line):
                in_desc = False
            else:
                desc_lines.append(line.strip())
    desc = " ".join(" ".join(desc_lines).split())
    return name, desc, text


class Repo(unittest.TestCase):
    def test_twelve_skills_in_agents_directory(self):
        found = sorted(
            d for d in os.listdir(SKILLS_DIR)
            if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
        )
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            skill_path = os.path.join(SKILLS_DIR, s, "SKILL.md")
            name, desc, text = parse_skill_metadata(skill_path)
            self.assertEqual(name, s, "Skill name must match folder: %s" % s)
            self.assertTrue(desc, "Description is required for %s" % s)
            self.assertGreaterEqual(len(desc), 150, "Description too thin for %s: %d chars" % (s, len(desc)))
            self.assertLessEqual(len(desc), 350, "Description too verbose for %s: %d chars" % (s, len(desc)))

    def test_local_reference_links(self):
        for s in SKILLS:
            skill_dir = os.path.join(SKILLS_DIR, s)
            skill_path = os.path.join(skill_dir, "SKILL.md")
            with open(skill_path, encoding="utf-8") as fh:
                content = fh.read()
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", content):
                target = m.group(2)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = target.split("#")[0].split("?")[0]
                if target_path:
                    resolved = os.path.normpath(os.path.join(skill_dir, target_path))
                    self.assertTrue(os.path.exists(resolved),
                                    "Broken link in %s: %s -> %s" % (s, target, resolved))

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
