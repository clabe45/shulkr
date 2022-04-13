import os

import git
import pytest
from shulkr.config import get_config
from shulkr.git import get_repo

from shulkr.minecraft.version import Version, clear_manifest, load_manifest


MANIFEST_DATA = {
	'latest': {
		'release': '1.0.0',
		'snapshot': '1.0.0'
	},
	'versions': [
		{
			'type': 'release',
			'id': '1.0.0'
		},
		{
			'type': 'snapshot',
			'id': 'abcdef'
		}
	]
}


class TestVersions:
	def __init__(self, snapshot: Version, release: Version) -> None:
		self.snapshot = snapshot
		self.release = release


def create_commit(mocker):
	return mocker.create_autospec(git.Commit)


def create_tag(mocker):
	tag = mocker.create_autospec(git.Tag)

	# To match 'versions' fixture, for testing Version.pattern()
	mocker.patch.object(tag, 'name', 'abcdef')

	return tag


def create_repo(mocker):
	repo = mocker.create_autospec(git.Repo)

	# Make the repo directory useful for testing shulkr.minecraft.source
	repo.working_tree_dir = os.path.abspath('foo')

	return repo


@pytest.fixture
def decompiler(mocker):
	"""
	Mock _setup_decompiler() to return a fake git repo with the current
	working_tree_dir
	"""

	def mocked_setup_decompiler(local_dir: str, _remote_url: str) -> git.Repo:
		"""Create a fake decompiler subdirectory (.yarn or .DecompilerMC)"""

		# It will be located directly under the shulkr repo directory
		repo = get_repo()
		decompiler_dir = os.path.join(repo.working_tree_dir, local_dir)

		# Create a fake git repo, and set the working_tree_dir property
		decompiler_repo = mocker.create_autospec(git.Repo)
		decompiler_repo.working_tree_dir = decompiler_dir

		return decompiler_repo

	# Tell the generate_sources functions to use our fake decompiler creator
	mocker.patch(
		'shulkr.minecraft.source._setup_decompiler',
		new=mocked_setup_decompiler
	)


@pytest.fixture
def empty_repo(mocker, decompiler):
	repo = create_repo(mocker)

	orig_git_tag = repo.git.tag

	def new_git_tag(*args):
		if args == ('--merged',):
			return ''

		return orig_git_tag(*args)

	mocker.patch.object(repo.git, 'tag', new=new_git_tag)

	# get_repo() will return this value
	mocker.patch('shulkr.git.repo', repo)

	return repo


@pytest.fixture
def nonempty_repo(mocker, decompiler):
	repo = create_repo(mocker)

	# Add a fake commit
	commit = create_commit(mocker)
	mocker.patch.object(repo, 'iter_commits', return_value=iter([commit]))

	# Add a fake tag for that commit
	tag = create_tag(mocker)

	orig_git_tag = repo.git.tag

	def new_git_tag(*args):
		if args == ('--merged',):
			return tag.name

		return orig_git_tag(*args)

	mocker.patch.object(repo.git, 'tag', new=new_git_tag)

	# get_repo() will return this value
	mocker.patch('shulkr.git.repo', repo)

	return repo


@pytest.fixture
def yarn_mappings():
	config = get_config()

	prev_mappings = config.mappings
	config.mappings = 'yarn'

	yield

	config.mappings = prev_mappings


@pytest.fixture
def mojang_mappings():
	config = get_config()

	prev_mappings = config.mappings
	config.mappings = 'mojang'

	yield

	config.mappings = prev_mappings


@pytest.fixture
def versions():
	load_manifest(MANIFEST_DATA, earliest_supported_version_id='abcdef')

	snapshot = Version.of('abcdef')
	release = Version.of('1.0.0')

	yield TestVersions(snapshot, release)

	clear_manifest()


@pytest.fixture
def root_dir():
	script_dir = os.path.dirname(__file__)
	return os.path.realpath(
		os.path.join(script_dir, '..', '..')
	)
