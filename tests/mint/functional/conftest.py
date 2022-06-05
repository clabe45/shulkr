from tempfile import TemporaryDirectory
import pytest

from mint.repo import Repo


@pytest.fixture
def tempdir():
	with TemporaryDirectory() as tempdir:
		yield tempdir


@pytest.fixture
def repo(tempdir):
	yield Repo.init(tempdir)


@pytest.fixture
def shallow_cloned_repo(tempdir):
	yield Repo.clone('https://github.com/clabe45/shulkr.git', tempdir, depth=1)
