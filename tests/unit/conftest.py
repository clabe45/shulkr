import os

import git
import pytest

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
def empty_repo(mocker):
	repo = create_repo(mocker)

	# Since there are no commits, iter_commits() must throw an error
	e = ValueError('Reference at ... does not exist')
	repo.iter_commits.side_effect = mocker.Mock(side_effect=e)

	# get_repo() will return this value
	mocker.patch('shulkr.git.repo', repo)

	return repo


@pytest.fixture
def nonempty_repo(mocker):
	repo = create_repo(mocker)

	# Add a fake commit
	commit = create_commit(mocker)
	mocker.patch.object(repo, 'iter_commits', return_value=iter([commit]))

	# Add a fake tag for that commit
	tag = create_tag(mocker)
	repo.tags = [tag]

	# get_repo() will return this value
	mocker.patch('shulkr.git.repo', repo)

	return repo


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
