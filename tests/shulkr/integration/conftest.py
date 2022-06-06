from tempfile import TemporaryDirectory

from mint.repo import Repo
import pytest
from minecraft.version import clear_manifest, load_manifest


@pytest.fixture(autouse=True)
def manifest():
	load_manifest()
	yield
	clear_manifest()


@pytest.fixture
def repo(mocker):
	tmp_dir = TemporaryDirectory(prefix='shulkr-test')
	repo = Repo.init(tmp_dir.name)
	mocker.patch('shulkr.repo.repo', repo)

	yield repo

	# tmp_dir is removed when it goes out of scope
