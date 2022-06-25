from mint.repo import Repo


def test_git_repo_initiated(run_yarn):
	# Make sure this is a git repo. If it's not, an error will be thrown.
	Repo(run_yarn.repo_path)


def test_commits_created(run_yarn):
	repo = Repo(run_yarn.repo_path)
	history = repo.git.rev_list('HEAD').splitlines()
	actual = [repo.git.log("--format='%B'", commit, n=1) for commit in history]
	actual.reverse()

	# Calculate expected commit messages from versions
	expected = ['add .shulkr', 'add .gitignore']
	if run_yarn.undo_renamed_vars:
		expected.append(f'version {run_yarn.versions[0]}')
		expected.extend([
			f'version {version}\n\nRenamed variables reverted'
			for version in run_yarn.versions[1:]
		])
	else:
		expected.extend([f'version {version}' for version in run_yarn.versions])

	assert actual == expected


def test_when_running_with_yarn_gitignore_and_src_are_tracked(run_yarn):
	repo = Repo(run_yarn.repo_path)

	# List files and directories that were changed directly under the root
	actual = set(repo.git.ls_tree('HEAD', name_only=True).splitlines())
	expected = set(['.gitignore', '.shulkr', 'src'])
	assert actual == expected


def test_when_running_with_decompilermc_gitignore_src_are_tracked(run_mojang):
	repo = Repo(run_mojang.repo_path)

	# List files and directories that were changed directly under the root
	actual = set(repo.git.ls_tree('HEAD', name_only=True).splitlines())
	expected = set(['.gitignore', '.shulkr', 'src'])
	assert actual == expected


def test_tags_created(run_yarn):
	repo = Repo(run_yarn.repo_path)
	actual = set(repo.git.tag(list=True).splitlines())
	expected = set(run_yarn.versions)
	assert actual == expected


def test_when_running_with_yarn_working_tree_clean(run_yarn):
	repo = Repo(run_yarn.repo_path)
	assert len(repo.git.status(porcelain=True)) == 0


def test_when_running_with_decompilermc_working_tree_clean(run_mojang):
	repo = Repo(run_mojang.repo_path)
	assert len(repo.git.status(porcelain=True)) == 0
