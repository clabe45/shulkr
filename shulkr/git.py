from __future__ import annotations
import os.path
from typing import Optional, TYPE_CHECKING

from git import (
	Commit,
	GitCommandError,
	InvalidGitRepositoryError,
	NoSuchPathError,
	Repo
)

from shulkr.config import get_config

if TYPE_CHECKING:
	from shulkr.minecraft.version import Version


def get_repo():
	global repo

	if not repo:
		config = get_config()

		try:
			repo = Repo(config.repo_path)

		except NoSuchPathError:
			print('Initializing git')
			repo = Repo.init(config.repo_path)

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


def head_has_versions() -> bool:
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


def create_gitignore() -> None:
	print('Creating gitignore')

	repo = get_repo()

	gitignore_path = os.path.join(repo.working_tree_dir, '.gitignore')

	with open(gitignore_path, 'w+') as gitignore:
		to_ignore = ['.yarn', '.DecompilerMC']
		gitignore.write('\n'.join(to_ignore) + '\n')

	repo.git.add('.gitignore')
	repo.git.commit(message='add .gitignore')


def commit_version(
	version: Version,
	undo_renamed_vars: bool,
	message_template: str
) -> None:

	repo = get_repo()

	commit_msg = message_template.strip().replace('{}', str(version))
	if undo_renamed_vars and head_has_versions():
		commit_msg += '\n\nRenamed variables reverted'

	if get_config().mappings == 'mojang':
		repo.git.add('client', 'server')
	else:
		repo.git.add('src')

	repo.git.commit(message=commit_msg)


def tag_version(version: 'Version') -> None:
	repo = get_repo()

	repo.create_tag(str(version))


repo = None
