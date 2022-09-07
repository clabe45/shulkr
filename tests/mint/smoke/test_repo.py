import os


class TestRepo:
	def test_init_creates_git_directory(self, repo):
		git_dir = os.path.join(repo.path, '.git')
		assert os.path.exists(git_dir)

	def test_clone_creates_git_directory(self, shallow_cloned_repo):
		git_dir = os.path.join(shallow_cloned_repo.path, '.git')
		assert os.path.exists(git_dir)
