from tempfile import TemporaryDirectory
import pytest

from mint.repo import Repo

from command import Command


@pytest.fixture
def tempdir():
    with TemporaryDirectory() as tempdir:
        yield tempdir


@pytest.fixture
def repo(tempdir):
    yield Repo.init(tempdir)


@pytest.fixture
def git(repo):
    return Command("git", working_dir=repo.path)
