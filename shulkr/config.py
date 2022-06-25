from __future__ import annotations
import os

import toml

from shulkr.repo import get_repo


class Config:
	def __init__(self, repo_path: str, mappings: str = None) -> None:
		self.repo_path = repo_path
		self.mappings = mappings

	def save(self) -> None:
		"""
		Write this configuration as TOML to the .shulkr file in the
		corresponding shulkr repo
		"""

		raw_config = {
			'mappings': self.mappings
			# No need to store the repo path (since it is supplied to the CLI
			# and defaults to the CWD)
		}

		config_path = _config_path_for_repo(self.repo_path)
		with open(config_path, 'w+') as config_file:
			toml.dump(raw_config, config_file)


def _config_path_for_repo(repo_path: str) -> str:
	return os.path.join(repo_path, '.shulkr')


def _config_exists(repo_path: str) -> bool:
	return os.path.exists(
		_config_path_for_repo(repo_path)
	)


def _load_config(repo_path: str) -> Config:
	config_path = _config_path_for_repo(repo_path)
	with open(config_path, 'r') as config_file:
		raw_config = toml.load(config_file)

	return Config(
		repo_path=repo_path,
		mappings=raw_config['mappings']
	)


def _commit_config() -> None:
	repo = get_repo()

	repo.git.add('.shulkr')
	repo.git.commit(message='add .shulkr')


def _create_config(repo_path: str, mappings: str) -> Config:
	global config

	config = Config(repo_path, mappings)
	config.save()
	_commit_config()

	return config


def init_config(repo_path: str, mappings: str) -> None:
	"""
	Initialize the config state

	If a .shulkr file exists for the current repo, it will be loaded.
	Otherwise, a new one will be created with the specified mappings.

	Args:
		repo_path (str): _description_
		mappings (str): _description_
	"""

	global config

	if _config_exists(repo_path):
		config = _load_config(repo_path)
	else:
		config = _create_config(repo_path, mappings)


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
