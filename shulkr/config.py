from __future__ import annotations
import os

import toml

from shulkr.repo import get_repo


class Config:
	def __init__(
		self,
		repo_path: str,
		mappings: str,
		message_template: str,
		tag: bool,
		undo_renamed_vars: bool
	) -> None:

		self.repo_path = repo_path
		self.mappings = mappings
		self.message_template = message_template
		self.tag = tag
		self.undo_renamed_vars = undo_renamed_vars

	def save(self) -> None:
		"""
		Write this configuration as TOML to the .shulkr file in the
		corresponding shulkr repo
		"""

		raw_config = {
			'mappings': self.mappings,
			'message': self.message_template,
			'tag': self.tag,
			'experimental': {
				'undo_renamed_vars': self.undo_renamed_vars
			}
			# No need to store the repo path (since it is supplied to the CLI
			# and defaults to the CWD)
		}

		config_path = _config_path_for_repo(self.repo_path)
		with open(config_path, 'w+') as config_file:
			toml.dump(raw_config, config_file)


def _config_path_for_repo(repo_path: str) -> str:
	return os.path.join(repo_path, '.shulkr')


def _load_config(repo_path: str) -> Config:
	config_path = _config_path_for_repo(repo_path)
	with open(config_path, 'r') as config_file:
		raw_config = toml.load(config_file)

	return Config(
		repo_path=repo_path,
		mappings=raw_config['mappings'],
		message_template=raw_config['message'],
		tag=raw_config['tag'],
		undo_renamed_vars=raw_config['experimental']['undo_renamed_vars']
	)


def _commit_config() -> None:
	repo = get_repo()

	repo.git.add('.shulkr')
	repo.git.commit(message='add .shulkr')


def _create_config(
	repo_path: str,
	mappings: str,
	message_template: str,
	tag: bool,
	undo_renamed_vars: bool
) -> Config:

	global config

	config = Config(
		repo_path,
		mappings,
		message_template,
		tag,
		undo_renamed_vars
	)
	config.save()
	_commit_config()

	return config


def config_exists(repo_path: str) -> bool:
	return os.path.exists(
		_config_path_for_repo(repo_path)
	)


def init_config(
	repo_path: str,
	mappings: str,
	message_template: str,
	tag: bool,
	undo_renamed_vars: bool
) -> None:
	"""
	Initialize the config state

	If a .shulkr file exists for the current repo, it will be loaded.
	Otherwise, a new one will be created with the specified mappings.

	Args:
		repo_path (str): _description_
		mappings (str): _description_
	"""

	global config

	if config_exists(repo_path):
		config = _load_config(repo_path)
	else:
		config = _create_config(
			repo_path,
			mappings,
			message_template,
			tag,
			undo_renamed_vars
		)


def clear_config() -> None:
	"""
	Unload the config from memory

	Used in tests
	"""

	global config

	config = None


def get_config():
	return config


config = None
