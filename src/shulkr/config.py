from __future__ import annotations
import os

import click
import toml

from shulkr.repo import get_repo


class Config:
	"""
	A class representing the configuration of a shulkr repo

	Attributes:
		repo_path (str): The path to the shulkr repo
		mappings (str): The path to the mappings file
		message_template (str): The template for the commit message
		tag (bool): Whether or not to tag the commit
		undo_renamed_vars (bool): Whether or not to undo renamed variables
	"""

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
	"""
	Get the path to the .shulkr file for a repo

	Args:
		repo_path (str): The path to the repo

	Returns:
		str: The path to the .shulkr file
	"""

	return os.path.join(repo_path, '.shulkr')


def _load_config(repo_path: str) -> Config:
	"""
	Load the config from the .shulkr file in the repo

	Args:
		repo_path (str): The path to the repo

	Returns:
		Config: The loaded config
	"""

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
	"""
	Commit the .shulkr file to the repo
	"""

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
	"""
	Create a new config and save it to the .shulkr file

	Args:
		repo_path (str): The path to the repo
		mappings (str): The path to the mappings file
		message_template (str): The template for the commit message
		tag (bool): Whether or not to tag the commit
		undo_renamed_vars (bool): Whether or not to undo renamed variables

	Returns:
		Config: The created config
	"""

	global config

	click.echo('Saving config')

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
	"""
	Check if a .shulkr file exists for the repo

	Args:
		repo_path (str): The path to the repo

	Returns:
		bool: True if a .shulkr file exists. False otherwise.
	"""

	return os.path.exists(
		_config_path_for_repo(repo_path)
	)


def init_config(
	repo_path: str,
	mappings: str,
	message_template: str,
	tag: bool,
	undo_renamed_vars: bool
) -> bool:
	"""
	Initialize the config state

	If a .shulkr file exists for the current repo, it will be loaded.
	Otherwise, a new one will be created with the specified mappings.

	Args:
		repo_path (str): The path to the repo
		mappings (str): The path to the mappings file
		message_template (str): The template for the commit message
		tag (bool): Whether or not to tag the commit
		undo_renamed_vars (bool): Whether or not to undo renamed variables

	Returns:
		bool: True if a config was loaded. False if a new one was created.
	"""

	global config

	if config_exists(repo_path):
		config = _load_config(repo_path)
		return True
	else:
		config = _create_config(
			repo_path,
			mappings,
			message_template,
			tag,
			undo_renamed_vars
		)
		return False


def clear_config() -> None:
	"""
	Unload the config from memory

	Used in tests
	"""

	global config

	config = None


def get_config():
	"""
	Get the config

	Returns:
		Config: The config
	"""

	return config


config = None
