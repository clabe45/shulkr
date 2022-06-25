import os
from unittest.mock import MagicMock

from mint.command import GitCommandError
from mint.repo import Repo
import pytest
from shulkr.config import Config, get_config
from shulkr.repo import get_repo


def create_repo(mocker, path: str):
	repo = MagicMock()

	# Make the repo directory useful for testing shulkr.minecraft.source
	repo.path = os.path.abspath(path)

	class MockGitCommand:
		def add():
			pass

		def checkout():
			pass

		def clean():
			pass

		def commit():
			pass

		def describe():
			pass

		def fetch():
			pass

		def reset():
			pass

		def tag():
			pass

		def rev_parse():
			pass

	repo.git = mocker.create_autospec(MockGitCommand())

	return repo


@pytest.fixture
def config(mocker):
	"""
	Use a fake config

	The advantage of using this fixture over calling init_config is that this
	fixture does not use any operating system resources.
	"""

	config = Config(
		repo_path=os.path.abspath('foo'),
		mappings='mojang',
		message_template='{}',
		tag=True,
		undo_renamed_vars=False
	)
	mocker.patch('shulkr.config.config', config)

	return config


@pytest.fixture
def decompiler(mocker):
	"""
	Mock _setup_decompiler() to return a fake git repo with the current
	path
	"""

	def mocked_setup_decompiler(local_dir: str, _remote_url: str) -> Repo:
		"""Create a fake decompiler subdirectory (.yarn or .DecompilerMC)"""

		# It will be located directly under the shulkr repo directory
		repo = get_repo()
		decompiler_dir = os.path.join(repo.path, local_dir)

		# Create a fake git repo, and set the path property
		return create_repo(mocker, decompiler_dir)

	# Tell the generate_sources functions to use our fake decompiler creator
	mocker.patch(
		'minecraft.source._setup_decompiler',
		new=mocked_setup_decompiler
	)


@pytest.fixture
def empty_repo(mocker, decompiler):
	repo = create_repo(mocker, 'foo')

	# Throw error when `git rev-parse` is called
	def rev_parse(*args, **kwargs):
		raise GitCommandError(
			'git rev-parse...',
			stderr="fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree."
		)

	mocker.patch.object(repo.git, 'rev_parse', side_effect=rev_parse)

	# Throw error when 'git describe' is called (it will only be called with
	# --tags)
	describe_error = GitCommandError(
		'git describe...',
		stderr='fatal: No names found, cannot describe anything.'
	)
	mocker.patch.object(repo.git, 'describe', side_effect=describe_error)

	# get_repo() will return this value
	mocker.patch('shulkr.repo.repo', repo)

	return repo


@pytest.fixture
def nonempty_repo(mocker, decompiler):
	repo = create_repo(mocker, 'foo')

	# Add a fake commit
	mocker.patch.object(
		repo.git,
		'rev_parse',
		return_value=iter(['9e71573c6ae5a52195274871a679a23379ad1274'])
	)

	# Add a fake tag for that commit (it will only be called with --tags)
	mocker.patch.object(repo.git, 'describe', return_value='abcdef')

	# get_repo() will return this value
	mocker.patch('shulkr.repo.repo', repo)

	return repo


@pytest.fixture
def yarn_mappings(config):
	config = get_config()

	prev_mappings = config.mappings
	config.mappings = 'yarn'

	yield

	config.mappings = prev_mappings


@pytest.fixture
def mojang_mappings(config):
	config = get_config()

	prev_mappings = config.mappings
	config.mappings = 'mojang'

	yield

	config.mappings = prev_mappings


@pytest.fixture
def root_dir():
	script_dir = os.path.dirname(__file__)
	return os.path.realpath(
		os.path.join(script_dir, '..', '..')
	)
