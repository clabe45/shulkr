import os

import git
import pytest

from shulkr.minecraft.version import Version, load_manifest


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


@pytest.fixture
def repo(mocker):
	mocker.patch('git.Repo')
	return git.Repo()


@pytest.fixture
def commit(mocker):
	mocker.patch('git.objects.commit.Commit')
	return git.objects.commit.Commit


@pytest.fixture
def versions():
	load_manifest(MANIFEST_DATA, earliest_supported_version_id='abcdef')

	snapshot = Version.of('abcdef')
	release = Version.of('1.0.0')
	return TestVersions(snapshot, release)


@pytest.fixture
def root_dir():
	script_dir = os.path.dirname(__file__)
	return os.path.realpath(
		os.path.join(script_dir, '..', '..')
	)
