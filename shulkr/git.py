from __future__ import annotations
import os.path
from typing import Optional

from git import Commit, InvalidGitRepositoryError, Repo

from shulkr.config import get_config


def get_repo():
	global repo

	if not repo:
		config = get_config()

		try:
			repo = Repo(config.repo_path)
		except InvalidGitRepositoryError:
			print('Initializing git')
			repo = Repo.init(config.repo_path)

	return repo


def get_blob(commit: Optional[Commit], path: str) -> bytes:
	config = get_config()

	if commit is None:
		p = os.path.join(config.repo_path, path)
		with open(p, 'r') as f:
			return f.read()

	parts = path.split('/')
	curr = commit.tree

	while len(parts) > 0:
		name = parts.pop(0)
		curr = curr[name]

	return curr.data_stream.read().decode()


def head_has_commits() -> bool:
	repo = get_repo()

	try:
		repo.iter_commits()
		return True

	except ValueError as e:
		if 'does not exist' in str(e):
			return False

		raise e


repo = None
