"""Offline source checks, not a fresh-aperture acceptance test."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "continuity/COMHEADS.md"


def routes(text):
    result = {}
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Route", "---"}:
            continue
        route, labels, destinations = cells
        paths = re.findall(r"`([^`]+)`", destinations)
        if not paths or route in result:
            raise ValueError("invalid or duplicate route")
        result[route] = (labels.split(", "), paths)
    return result


def select(table, label):
    # Model the documented label rule; not a runtime identity detector.
    normalized = re.sub(r"[\s_]+", "-", label.strip().lower()) if isinstance(label, str) else ""
    return next((name for name, (labels, _) in table.items()
                 if normalized in labels), "unassigned")


class COMHeadChecks(unittest.TestCase):
    def setUp(self):
        self.text = REGISTRY.read_text(encoding="utf-8")
        self.table = routes(self.text)

    def test_exact_roles_and_unique_aliases(self):
        self.assertEqual(set(self.table),
                         {"framework", "campfire", "campfire-framework", "build", "codex", "cc", "unassigned"})
        labels = [label for aliases, _ in self.table.values() for label in aliases]
        self.assertEqual(len(labels), len(set(labels)))

    def test_all_paths_resolve_within_repo(self):
        for _, paths in self.table.values():
            for path in paths:
                with self.subTest(path=path):
                    resolved = (ROOT / path).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT.resolve()))
                    self.assertTrue(resolved.is_file())
                    self.assertNotEqual(resolved, REGISTRY.resolve())

    def test_aliases_and_safe_unknown(self):
        for label in [None, "", "invented", "a Framework-like AI", "COM", "GPT",
                      "FROM: CLAUDE CODE", "Build Ninety", "Framework Build Five"]:
            self.assertEqual(select(self.table, label), "unassigned")
        for label, expected in [("codex-windows", "codex"), (" CODEX ", "codex"),
                                ("framework-build", "build"), ("build", "build"),
                                ("claude-code", "cc"), ("cc", "cc"),
                                ("campfire", "campfire"), ("framework", "framework"),
                                ("CLAUDE CODE", "cc"), ("Claude Code", "cc"),
                                ("claude_code", "cc"), ("CODEX WINDOWS", "codex"),
                                ("Codex Windows", "codex"), ("FRAMEWORK BUILD", "build"),
                                ("Framework Build", "build"), ("FRAMEWORK BUILD TWO", "build"),
                                ("Build Three", "build"), ("Build Four", "build"),
                                ("FW", "framework"), ("fw", "framework"),
                                ("Campfire Two", "campfire"),
                                ("CAMPFIRE FRAMEWORK", "campfire-framework"),
                                ("Campfire Framework", "campfire-framework"),
                                (" CLAUDE\t__CODE ", "cc")]:
            self.assertEqual(select(self.table, label), expected)

    def test_no_recursive_or_historical_loading_route(self):
        for _, paths in self.table.values():
            self.assertEqual(len(paths), len(set(paths)))
            self.assertNotIn("continuity/COMHEADS.md", paths)
            self.assertFalse(any("archive" in p.lower() or "RELOAD" in p for p in paths))
        self.assertIn("Select this route once", self.text)
        self.assertIn("not a requirement to restart dispatch", self.text)

    def test_registry_is_not_mutable_status_or_host_config(self):
        self.assertNotRegex(self.text, r"https?://|#[0-9]+|20\d\d-\d\d-\d\d|[a-f0-9]{32,64}")
        for forbidden in ["WRITES_ENABLED", "consumed=", "Bearer ", "workers.dev"]:
            self.assertNotIn(forbidden, self.text)

    def test_required_role_heads(self):
        self.assertEqual(self.table["codex"][1][:2],
                         ["coordination/build_ledger/BUILD_STATUS.md",
                          "coordination/ACTIVE_THREAD_POINTER.md"])
        self.assertIn("continuity/CAMPFIRE_ORIENTATION.md", self.table["campfire"][1])
        self.assertEqual(self.table["unassigned"][1], ["COM_STATE.md", "COM_PROTOCOL_WORKING.md"])
        self.assertIn("own durable local bootstrap first", self.text)
        self.assertIn("grants no Framework role", self.text)
        self.assertIn("never supplies the missing Framework role", self.text)
        self.assertIn("standing with Campfire orientation", self.text)

    def test_entry_links_and_existing_protocol(self):
        for path in ["README.md", "COM_STATE.md", "continuity/COMSYNC_PROTOCOL.md"]:
            self.assertIn("COMHEADS.md", (ROOT / path).read_text(encoding="utf-8"))
        self.assertIn("COMS and", self.text)
        self.assertIn("HELLO rules", self.text)
        self.assertIn("not authority", self.text)

    def test_parser_rejects_duplicate_route_fixture(self):
        row = "| codex | codex | `COM_STATE.md` |"
        with self.assertRaises(ValueError):
            routes(row + "\n" + row)

    def test_single_framework_route_owner(self):
        state = (ROOT / "COM_STATE.md").read_text(encoding="utf-8")
        section = state.split("## Framework-role routing", 1)[1].split("## Current source pointers", 1)[0]
        self.assertIn("COMHEADS.md", section)
        self.assertNotIn("```", section)
        self.assertNotIn("->", section)
        self.assertIn("conditional dependencies", section)
        self.assertIn("continuity/FRAMEWORK_HEAD.md", self.table["framework"][1])


if __name__ == "__main__":
    unittest.main()
