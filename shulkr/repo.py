from __future__ import annotations

import click

from mint.repo import NoSuchRepoError, Repo


def init_repo(repo_path: str) -> None:
	"""
	Load information about the current shulkr/git repo

	Must be called before get_repo()

	Args:
		repo_path (str): Path to the working tree of the repo
	"""

	global repo

	try:
		repo = Repo(repo_path)

	except FileNotFoundError:
		click.echo('Initializing git')
		repo = Repo.init(repo_path)

	except NotADirectoryError:
		click.echo('Initializing git')
		repo = Repo.init(repo_path)

	except NoSuchRepoError:
		click.echo('Initializing git')
		repo = Repo.init(repo_path)


def get_repo() -> Repo:
	return repo


repo = None
