from git import Repo


def test_git_repo_initiated(run_yarn):
	# Make sure this is a git repo. If it's not, an error will be thrown.
	Repo(run_yarn.repo_path)


def test_commits_created(run_yarn):
	repo = Repo(run_yarn.repo_path)
	actual = [commit.message.rstrip() for commit in repo.iter_commits()]
	actual.reverse()

	# Calculate expected commit messages from versions
	expected = ['add .gitignore']
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
	root_tree = repo.head.commit.tree
	actual = set([obj.name for obj in (root_tree.trees + root_tree.blobs)])
	expected = set(['.gitignore', 'src'])
	assert actual == expected


def test_when_running_with_decompilermc_gitignore_client_and_server_are_tracked(run_mojang):
	repo = Repo(run_mojang.repo_path)

	# List files and directories that were changed directly under the root
	root_tree = repo.head.commit.tree
	actual = set([obj.name for obj in (root_tree.trees + root_tree.blobs)])
	expected = set(['.gitignore', 'client', 'server'])
	assert actual == expected


def test_tags_created(run_yarn):
	repo = Repo(run_yarn.repo_path)
	actual = set([tag.name for tag in repo.tags])
	expected = set(run_yarn.versions)
	assert actual == expected


def test_when_running_with_yarn_working_tree_clean(run_yarn):
	repo = Repo(run_yarn.repo_path)
	assert len(repo.git.status(porcelain=True)) == 0


def test_when_running_with_decompilermc_working_tree_clean(run_mojang):
	repo = Repo(run_mojang.repo_path)
	assert len(repo.git.status(porcelain=True)) == 0
