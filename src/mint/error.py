from command import CommandError


class GitError(CommandError):
	"""Raised when a git command fails."""
	pass
