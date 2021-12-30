import git
import pytest


@pytest.fixture(scope='function')
def repo(mocker):
	mocker.patch('git.Repo')
	repo = git.Repo()

	mocker.patch.object(repo, 'add')
	mocker.patch.object(repo.index, 'commit')

	return repo
