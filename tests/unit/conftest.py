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


@pytest.fixture(scope='function')
def repo(mocker):
	mocker.patch('git.Repo')
	repo = git.Repo()

	mocker.patch.object(repo, 'add')
	mocker.patch.object(repo.index, 'commit')

	return repo


@pytest.fixture(scope='function')
def versions():
	load_manifest(MANIFEST_DATA, earliest_supported_version_id='abcdef')

	snapshot = Version.of('abcdef')
	release = Version.of('1.0.0')
	return TestVersions(snapshot, release)
