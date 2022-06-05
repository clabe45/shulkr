from tempfile import TemporaryDirectory

import git
import pytest

from shulkr.minecraft.version import clear_manifest, load_manifest


@pytest.fixture(autouse=True)
def manifest():
	load_manifest()
	yield
	clear_manifest()


@pytest.fixture
def repo(mocker):
	tmp_dir = TemporaryDirectory(prefix='shulkr-test')
	repo = git.Repo.init(tmp_dir.name)
	mocker.patch('shulkr.git.repo', repo)

	yield repo

	# tmp_dir is removed when it goes out of scope
