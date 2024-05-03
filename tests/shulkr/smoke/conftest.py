import subprocess
import tempfile
from typing import Generator, List

from minecraft.version import clear_manifest, load_manifest
from mint.repo import Repo

import pytest


class RunResult:
    def __init__(self, exit_code: int, output: str, error: str) -> None:
        """
        Args:
                status_code (int): The exit code of the command.
                output (str): Stdout
                error (str): Stderr
        """

        self.exit_code = exit_code
        self.output = output
        self.error = error


@pytest.fixture(autouse=True)
def manifest():
    load_manifest()
    yield
    clear_manifest()


@pytest.fixture
def repo(mocker):
    tmp_dir = tempfile.TemporaryDirectory(prefix="shulkr-test")
    repo = Repo.init(tmp_dir.name)
    mocker.patch("shulkr.repo.repo", repo)

    yield repo

    # tmp_dir is removed when it goes out of scope


def create_command(repo_path: str) -> List[str]:
    return ["pipenv", "run", "start", "-p", repo_path]


@pytest.fixture(scope="session")
def run() -> Generator[RunResult, None, None]:
    """
    Run shulkr with no versions

    It is expected to display a warning message stating that no versions are
    selected.

    Yields:
            Stderr (if present), otherwise None
    """

    with tempfile.TemporaryDirectory(prefix="shulkr") as repo_path:
        command = create_command(repo_path)
        p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout = p.stdout.decode("utf-8")
        stderr = p.stderr.decode("utf-8")
        yield RunResult(p.returncode, stdout, stderr)
