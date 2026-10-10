import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

from _load import load

sweep = load("replica-brand", "sweep")


def put(root, rel, text, binary=False):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w") as fh:
        fh.write(text)
    return path


class Sweep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        r = self.root = self.tmp.name
        put(r, "src/app/page.tsx", "export default function Page() {\n"
                                   "  return <h1>Slotwise</h1>\n}\n")
        put(r, "src/components/CalendlyEmbed.tsx", "// left over\n")
        put(r, "src/lib/copy.ts", "export const hero = 'The calendly alternative'\n")
        put(r, "src/styles/tokens.css", ":root { --accent: #006BFF; --bg: #fff; }\n")
        put(r, "src/lib/links.ts", "const help = 'https://help.calendly.com/x'\n")
        put(r, "src/lib/team.ts", "export const AcuitySchedulingSync = 1\n")
        put(r, "replica/recon.md", "# Recon: Calendly\n")
        put(r, "node_modules/x/index.js", "calendly\n")
        put(r, "public/logo.png", b"\x89PNG\0calendly", binary=True)
        put(r, "package-lock.json", '{"calendly": 1}\n')

    def tearDown(self):
        self.tmp.cleanup()

    def run_sweep(self, **kw):
        return sweep.sweep(self.root, avoid=["Calendly", "Acuity Scheduling"],
                           domains=["calendly.com"], colors=["#006bff"], **kw)

    def test_finds_names_paths_domains_and_colours(self):
        hits = self.run_sweep()
        kinds = {(h["kind"], os.path.basename(h["file"].rstrip("/"))) for h in hits}
        self.assertIn(("path", "CalendlyEmbed.tsx"), kinds)
        self.assertIn(("name", "copy.ts"), kinds)
        self.assertIn(("domain", "links.ts"), kinds)
        self.assertIn(("color", "tokens.css"), kinds)
        self.assertIn(("name", "team.ts"), kinds)   # AcuitySchedulingSync

    def test_skips_planning_folder_deps_locks_and_binaries(self):
        files = {h["file"] for h in self.run_sweep()}
        self.assertFalse(any(f.startswith("replica") for f in files))
        self.assertFalse(any("node_modules" in f for f in files))
        self.assertNotIn("package-lock.json", files)
        self.assertNotIn(os.path.join("public", "logo.png"), files)
        self.assertNotIn(os.path.join("src", "app", "page.tsx"), files)

    def test_include_replica(self):
        files = {h["file"] for h in self.run_sweep(include_replica=True)}
        self.assertIn(os.path.join("replica", "recon.md"), files)

    def test_short_hex_matches_long(self):
        put(self.root, "src/a.css", "a { color: #06f }\n")
        hits = sweep.sweep(self.root, colors=["#0066FF"])
        self.assertTrue(any(h["file"].endswith("a.css") for h in hits))

    def test_cli_exit_codes_and_config(self):
        cfg = put(self.root, "brand.json", json.dumps({"avoid": ["Calendly"]}))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(sweep.main([self.root, "--config", cfg]), 1)
        clean = tempfile.mkdtemp(dir=self.root)
        put(clean, "index.html", "<h1>Slotwise</h1>")
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(sweep.main([clean, "--avoid", "Calendly"]), 0)
        self.assertIn("Clean", buf.getvalue())
        with redirect_stderr(io.StringIO()):
            self.assertEqual(sweep.main([clean]), 2)

    def test_multiple_matches_and_line_numbers(self):
        # Multiple matches on one line: Calendly and Acuity Scheduling and a color
        put(self.root, "src/multi.ts", "line 1\nconst x = 'Calendly ' + 'AcuityScheduling' + '#006bff';\nline 3\n")
        hits = [h for h in self.run_sweep() if h["file"].endswith("multi.ts")]
        self.assertEqual(len(hits), 3)
        for h in hits:
            self.assertEqual(h["line"], 2)
        kinds = {h["kind"] for h in hits}
        self.assertEqual(kinds, {"name", "color"})

    def test_domains_and_punctuation(self):
        put(self.root, "src/punct.ts", "const url = 'https://calendly.com/user?ref=acuity-scheduling';\n")
        hits = [h for h in self.run_sweep() if h["file"].endswith("punct.ts")]
        self.assertTrue(any(h["kind"] == "domain" and h["match"] == "calendly.com" for h in hits))

    def test_generated_directories_skipped(self):
        put(self.root, "bin/Debug/output.txt", "Calendly should be ignored\n")
        put(self.root, "obj/Release/cache.txt", "Calendly should be ignored\n")
        put(self.root, "target/debug/build.log", "Calendly should be ignored\n")
        put(self.root, ".vs/config.txt", "Calendly should be ignored\n")
        files = {h["file"] for h in self.run_sweep()}
        self.assertFalse(any(f.startswith(("bin", "obj", "target", ".vs")) for f in files))

    def test_large_text_file(self):
        lines = ["function foo() { return 1; }\n"] * 5000
        lines[2500] = "const vendor = 'Calendly';\n"
        put(self.root, "src/large.js", "".join(lines))
        hits = [h for h in self.run_sweep() if h["file"].endswith("large.js")]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["line"], 2501)
        self.assertEqual(hits[0]["match"], "Calendly")

    def test_unicode_paths(self):
        put(self.root, "src/компонент/тест.ts", "const ref = 'Calendly';\n")
        hits = [h for h in self.run_sweep() if "компонент" in h["file"]]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["match"], "Calendly")

    def test_compact_json_and_summary_flags(self):
        cfg = put(self.root, "brand.json", json.dumps({"avoid": ["Calendly"]}))
        buf_compact = io.StringIO()
        with redirect_stdout(buf_compact):
            self.assertEqual(sweep.main([self.root, "--config", cfg, "--compact-json"]), 1)
        data = json.loads(buf_compact.getvalue())
        self.assertIsInstance(data, list)
        self.assertNotIn("\n", buf_compact.getvalue().strip())

        buf_sum = io.StringIO()
        with redirect_stdout(buf_sum):
            self.assertEqual(sweep.main([self.root, "--config", cfg, "--summary"]), 1)
        self.assertIn("Sweep failed", buf_sum.getvalue())


if __name__ == "__main__":
    unittest.main()
