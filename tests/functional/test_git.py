from git import Repo


def test_git_repo_initiated(run):
	# Make sure this is a git repo. If it's not, an error will be thrown.
	Repo(run.repo_path)


def test_commit_created(run):
	repo = Repo(run.repo_path)
	actual = set([commit.message for commit in repo.iter_commits()])
	expected = set([f'version {version}' for version in run.versions])
	assert actual == expected


def test_latest_commit_has_client_and_server(run):
	repo = Repo(run.repo_path)
	actual = set([tree.path for tree in repo.head.commit.tree.trees])
	expected = set(['client', 'server'])
	assert actual == expected


def test_tag_created(run):
	repo = Repo(run.repo_path)
	actual = set([tag.name for tag in repo.tags])
	expected = set(run.versions)
	assert actual == expected
