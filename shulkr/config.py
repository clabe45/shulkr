from __future__ import annotations
import os

import toml


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


def init_config(repo_path: str, mappings: str = None) -> Config:
	"""
	Read the config for the specified shulkr repo or create a new one if it
	doesn't exist

	Args:
		repo_path (str): Path to the shulkr repo
		mappings (str, optional): Mappings that will be used to decompile each
			version if creating a new config. Defaults to None.
	"""

	global config

	if _config_exists(repo_path):
		config = _load_config(repo_path)
	else:
		config = Config(repo_path, mappings)
		config.save()

	return config


def clear_config() -> None:
	global config

	config = None


def get_config():
	return config


config = None
