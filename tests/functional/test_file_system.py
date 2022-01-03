import os


def test_repo_only_contains_git_client_and_server_directories(run):
	assert set(os.listdir(run.repo_path)) == set(['.git', 'client', 'server'])


def test_server_and_client_src_directories_are_not_empty(run):
	for env in ('client', 'server'):
		src_dir = os.path.join(run.repo_path, env, 'src')
		assert len(os.listdir(src_dir)) > 0
