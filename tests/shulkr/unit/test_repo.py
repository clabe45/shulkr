from shulkr.repo import init_repo


def test_init_repo_returns_true_if_repo_exists(mocker, empty_repo):
	mocker.patch('shulkr.repo.click')
	mocker.patch('shulkr.repo.Repo')

	assert init_repo(empty_repo.path)


def test_init_repo_returns_false_if_repo_directory_does_not_exist(mocker):
	mocker.patch('shulkr.repo.click')
	mocker.patch('shulkr.repo.Repo', side_effect=FileNotFoundError)

	assert not init_repo('/tmp/does-not-exist')
