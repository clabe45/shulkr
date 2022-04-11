from git import Repo


def test_git_repo_initiated(run):
	# Make sure this is a git repo. If it's not, an error will be thrown.
	Repo(run.repo_path)


def test_commits_created(run):
	repo = Repo(run.repo_path)
	actual = set([commit.message.rstrip() for commit in repo.iter_commits()])

	# Calculate expected commit messages from versions
	if run.undo_renamed_vars:
		first = f'version {run.versions[0]}'
		rest = [
			f'version {version}\n\nRenamed variables reverted'
			for version in run.versions[1:]
		]
		expected = set([first] + rest)
	else:
		expected = set([f'version {version}' for version in run.versions])

	assert actual == expected


def test_latest_commit_has_gitignore_and_src(run):
	repo = Repo(run.repo_path)

	# List files and directories that were changed directly under the root
	root_tree = repo.head.commit.tree
	actual = set([obj.name for obj in (root_tree.trees + root_tree.blobs)])
	expected = set(['.gitignore', 'src'])
	assert actual == expected


def test_tags_created(run):
	repo = Repo(run.repo_path)
	actual = set([tag.name for tag in repo.tags])
	expected = set(run.versions)
	assert actual == expected


def test_working_tree_clean(run):
	repo = Repo(run.repo_path)
	assert len(repo.git.status(porcelain=True)) == 0
