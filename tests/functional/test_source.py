import os


def test_repo_only_contains_git_client_and_server_directories(generate_1_18):
	assert os.listdir(generate_1_18.repo_path) == ['.git', 'client', 'server']


def test_server_and_client_src_directories_are_not_empty(generate_1_18):
	for env in ('client', 'server'):
		src_dir = os.path.join(generate_1_18.repo_path, env, 'src')
		assert len(os.listdir(src_dir))
