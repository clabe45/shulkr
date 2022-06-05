from __future__ import annotations
import os

import git

from mint.command import GitCommand


class NoSuchRepoError(Exception):
	def __init__(self, path: str, *args: object) -> None:
		super().__init__(*args)

		self.path = path

	def __str__(self) -> str:
		return f'{self.path} is not a git repo'


class Repo:
	"""
	Git repo

	Creating a Repo object:
		# Use an existing repo
		repo = Repo(PATH)

		# Create an empty repo
		repo = Repo.init(PATH)

		# Clone a repo
		repo = Repo.clone(REMOTE_URL, DESTINATION)

	Using a Repo object:
		repo.git.commit('src', message='Some commit')  # or m='Some commit'
	"""

	def __init__(self, path: str, check_path=True) -> None:
		if check_path:
			Repo._ensure_repo_path_is_valid(path)

		self.path = path
		self.git = GitCommand(path)

	def to_gitpython(self) -> git.Repo:
		return git.Repo(self.path)

	@staticmethod
	def _ensure_repo_path_is_valid(path: str):
		if not os.path.exists(path):
			raise FileNotFoundError(path)

		# Make sure the path is a directory or a symlink
		if os.path.isfile(path):
			raise NotADirectoryError(path)

		git_dir = os.path.join(path, '.git')
		if not os.path.exists(git_dir) or os.path.isfile(git_dir):
			raise NoSuchRepoError(path)

	@staticmethod
	def init(path: str, **kwargs) -> Repo:
		if not os.path.exists(path):
			os.mkdir(path)

		repo = Repo(path, check_path=False)
		repo.git.init(**kwargs)
		return repo

	@staticmethod
	def clone(remote: str, dest: str, **kwargs) -> Repo:
		git = GitCommand()
		git.clone(remote, dest, **kwargs)
		return Repo(dest)
