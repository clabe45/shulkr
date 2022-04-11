import os


def test_repo_only_contains_git_gitignore_yarn_and_src_directories(run):
	assert set(os.listdir(run.repo_path)) == set(['.git', '.gitignore', '.yarn', 'src'])


def test_src_directory_are_not_empty(run):
	src_dir = os.path.join(run.repo_path, 'src')
	assert len(os.listdir(src_dir)) > 0
