from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = ROOT / "codex" / "git-hooks" / "git_commit_guard.py"
SPEC = importlib.util.spec_from_file_location("git_commit_guard", GUARD_PATH)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class CommitMessageTests(unittest.TestCase):
    def validate(self, message: str) -> list[str]:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            handle.write(message)
            path = Path(handle.name)
        try:
            return guard.validate_commit_message(path)
        finally:
            path.unlink(missing_ok=True)

    def test_accepts_conventional_subject(self) -> None:
        self.assertEqual([], self.validate("feat(auth): rotate refresh tokens\n"))

    def test_rejects_missing_scope(self) -> None:
        self.assertTrue(self.validate("docs: update setup\n"))

    def test_rejects_unknown_type(self) -> None:
        self.assertTrue(self.validate("eval(model): add cases\n"))

    def test_accepts_merge_subject(self) -> None:
        self.assertEqual([], self.validate("Merge branch 'main'\n"))

    def test_rejects_ai_attribution(self) -> None:
        self.assertTrue(
            self.validate("fix(api): handle retries\n\nCo-Authored-By: Codex <bot@example.com>\n")
        )


class PathTests(unittest.TestCase):
    def test_blocks_context_files_at_any_depth(self) -> None:
        paths = ["AGENTS.md", "docs/MEMORY.md", ".agents/skills/x/SKILL.md", "src/app.py"]
        self.assertEqual(paths[:3], guard.banned_paths(paths))

    def test_allows_normal_files(self) -> None:
        self.assertEqual([], guard.banned_paths(["src/app.py", "docs/architecture.md"]))


class IntegrationTests(unittest.TestCase):
    def run_git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8"
        )

    def test_global_hooks_block_and_allow_real_commits(self) -> None:
        with tempfile.TemporaryDirectory(prefix="codex-hook-test-") as tmp:
            repo = Path(tmp) / "project"
            repo.mkdir()
            self.run_git(repo, "init")
            self.run_git(repo, "config", "user.name", "Test User")
            self.run_git(repo, "config", "user.email", "test@example.com")
            self.run_git(repo, "config", "core.hooksPath", str(ROOT / "codex" / "git-hooks"))

            (repo / "app.py").write_text("print('ok')\n", encoding="utf-8")
            self.run_git(repo, "add", "app.py")
            bad = self.run_git(repo, "commit", "-m", "fix: missing scope")
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("COMMIT BLOCKED", bad.stderr)

            good = self.run_git(repo, "commit", "-m", "fix(app): add entrypoint")
            self.assertEqual(0, good.returncode, good.stderr)

            (repo / "AGENTS.md").write_text("local only\n", encoding="utf-8")
            self.run_git(repo, "add", "AGENTS.md")
            banned = self.run_git(repo, "commit", "-m", "docs(agent): add guidance")
            self.assertNotEqual(0, banned.returncode)
            self.assertIn("personal context files", banned.stderr)


if __name__ == "__main__":
    unittest.main()
