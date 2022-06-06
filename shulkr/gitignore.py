import os

from shulkr.repo import get_repo


def _gitignore_path() -> str:
	repo = get_repo()

	return os.path.join(repo.path, '.gitignore')


def _create_gitignore() -> None:
	print('Creating gitignore')

	repo = get_repo()

	with open(_gitignore_path(), 'w+') as gitignore:
		to_ignore = ['.yarn', '.DecompilerMC']
		gitignore.write('\n'.join(to_ignore) + '\n')

	repo.git.add('.gitignore')
	repo.git.commit(message='add .gitignore')


def ensure_gitignore_exists() -> None:
	"""
	Create and commit a .gitignore file if one does not exist
	"""

	if not os.path.isfile(_gitignore_path()):
		_create_gitignore()
