from mint.error import GitError

from shulkr.config import config_exists
from shulkr.repo import get_repo


def _repo_has_commits() -> bool:
	"""
	Check if the current repo has commits.
	"""

	try:
		get_repo().git.rev_parse('HEAD')
		return True

	except GitError:
		return False


def is_compatible() -> bool:
	"""
	Check if the current repo is compatible with the current shulkr version.
	"""

	repo = get_repo()
	return config_exists(repo.path) or not _repo_has_commits()
