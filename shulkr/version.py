"""
Module for management of Minecraft versions
"""

import os
import shutil

from java import undo_renames
from minecraft.source import generate_sources
from minecraft.version import Version
from mint.command import GitCommandError

from shulkr.config import get_config
from shulkr.repo import get_repo


def _commit_version(version: Version) -> None:
	repo = get_repo()
	message_template = get_config().message_template

	commit_msg = message_template.strip().replace('{}', str(version))
	if get_config().undo_renamed_vars and head_has_versions():
		commit_msg += '\n\nRenamed variables reverted'

	repo.git.add('src')

	repo.git.commit(message=commit_msg)


def _tag_version(version: Version) -> None:
	repo = get_repo()

	repo.git.tag(version)


def create_version(version: Version) -> None:
	"""
	Generate the sources for a Minecraft version and commit to the repo

	Args:
		version (Version): Version to create
		undo_renamed_vars (bool): If set, this function will attempt to revert
			any variables that were renamed in the new version
		message_template (str): Template for commit messages ('{}'s will be
			replaced with the version name)
		tag (bool): If set, the commit will be tagged
	"""

	# 1. Generate source code for the current version
	print(f'\nGenerating sources for Minecraft {version}')

	repo = get_repo()
	mappings = get_config().mappings
	repo_path = repo.path

	try:
		generate_sources(version, mappings, repo_path)
	except BaseException as e:
		# Undo src/ deletions
		if head_has_versions():
			repo.git.restore('src')
		else:
			path = os.path.join(repo.path, 'src')
			if os.path.exists(path):
				shutil.rmtree(path)

		raise e

	# 2. If there are any previous versions, undo the renamed variables
	if get_config().undo_renamed_vars and head_has_versions():
		print('Undoing renamed variables')
		undo_renames(get_repo().to_gitpython())

	# 3. Commit the new version to git
	print('Committing to git')
	_commit_version(version)

	# 4. Tag
	if get_config().tag:
		_tag_version(version)


def head_has_versions() -> bool:
	"""
	Check if any versions have been generated on the current branch

	Raises:
		e:

	Returns:
		bool: True if at least one version was found on the current branch
	"""

	repo = get_repo()

	try:
		# List tags reachable by HEAD
		repo.git.describe(tags=True)

		# If we made it here, there is at least one tag.
		return True

	except GitCommandError as e:
		if 'fatal: No names found, cannot describe anything.' in e.stderr:
			return False

		raise e


def get_latest_generated_version() -> Version:
	"""
	Get the most recent version commit on the current branch

	Returns:
		Version:
	"""

	if not head_has_versions():
		return None

	repo = get_repo()

	# Get most recent tag reachable by HEAD
	tag_name = repo.git.describe(tags=True)

	return Version.of(tag_name)
