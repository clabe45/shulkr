from git import Repo


def test_git_repo_initiated(generate_1_18):
	# Make sure this is a git repo. If it's not, an error will be thrown.
	Repo(generate_1_18.repo_path)


def test_commit_created(generate_1_18):
	repo = Repo(generate_1_18.repo_path)

	commit_msgs = [commit.message for commit in repo.iter_commits()]
	assert commit_msgs == ['version 1.18']


def test_tag_created(generate_1_18):
	repo = Repo(generate_1_18.repo_path)
	assert [tag.name for tag in repo.tags] == ['1.18']
