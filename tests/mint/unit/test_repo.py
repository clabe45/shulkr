import pytest

from mint.repo import Repo


@pytest.fixture(autouse=True)
def fs(mocker) -> None:
	mocker.patch('mint.command.subprocess.os.path.exists', return_value=True)
	mocker.patch('mint.command.subprocess.os.path.isfile', return_value=False)


@pytest.fixture(autouse=True)
def subprocess(mocker) -> None:
	mocker.patch('mint.command.subprocess')


class TestRepo:
	def test_clone_returns_repo_with_same_path(self):
		repo = Repo.clone('bar.git', 'bar')
		assert repo.path == 'bar'
