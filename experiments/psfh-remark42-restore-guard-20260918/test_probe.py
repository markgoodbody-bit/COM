"""No-Docker regression for per-invocation cleanup ownership."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("restore_probe", Path(__file__).with_name("probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ContainerIsolationTest(unittest.TestCase):
    def test_failed_starts_only_clean_their_own_unique_name(self):
        names = []
        for _ in range(2):
            commands = []

            def fake_run(args, check=True):
                commands.append(args)
                if args[:2] == ["docker", "run"]:
                    raise RuntimeError("synthetic startup failure")

            with patch.object(probe, "run", side_effect=fake_run), patch(
                "sys.argv", ["probe.py", "--out", "unused-result.json"]
            ):
                with self.assertRaisesRegex(RuntimeError, "synthetic startup failure"):
                    probe.main()
            self.assertEqual(commands[0][:2], ["docker", "run"])
            name = commands[0][commands[0].index("--name") + 1]
            self.assertRegex(name, r"^psfh-remark42-restore-guard-[0-9a-f]{32}$")
            self.assertEqual(commands[1:], [["docker", "rm", "-f", name]])
            names.append(name)
        self.assertNotEqual(*names)


if __name__ == "__main__":
    unittest.main()
