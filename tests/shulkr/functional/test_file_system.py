import os


def test_when_running_with_yarn_repo_only_contains_git_gitignore_yarn_and_src_directories(run_yarn):
	assert set(os.listdir(run_yarn.repo_path)) == set(['.git', '.gitignore', '.shulkr', '.yarn', 'src'])


def test_when_running_with_yarn_src_directory_is_not_empty(run_yarn):
	src_dir = os.path.join(run_yarn.repo_path, 'src')
	assert len(os.listdir(src_dir)) > 0


def test_when_running_with_decompilermc_repo_only_contains_git_gitignore_yarn_client_and_server_directories(run_mojang):
	assert set(os.listdir(run_mojang.repo_path)) == set(['.git', '.gitignore', '.shulkr', '.DecompilerMC', 'src'])


def test_when_running_with_decompilermc_src_directory_is_not_empty(run_mojang):
	src_dir = os.path.join(run_mojang.repo_path, 'src')
	assert len(os.listdir(src_dir)) > 0
