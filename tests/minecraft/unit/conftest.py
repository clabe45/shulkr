import os
from unittest.mock import MagicMock

import pytest

from minecraft.version import Version, clear_manifest, load_manifest


MANIFEST_DATA = {
	'latest': {
		'release': '1.20.5',
		'snapshot': 'abcdef'
	},
	'versions': [
		{
			'type': 'release',
			'id': '1.20.5'
		},
		{
			'type': 'snapshot',
			'id': 'abcdef'
		},
		{
			'type': 'release',
			'id': '1.20.4'
		}
	]
}


class TestVersions:
	def __init__(self, v1_20_4: Version, snapshot: Version, v1_20_5: Version) -> None:
		self.v1_20_4 = v1_20_4
		self.snapshot = snapshot
		self.v1_20_5 = v1_20_5
		self.release = v1_20_5


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
def versions():
	load_manifest(MANIFEST_DATA, earliest_supported_version_id='1.20.4')

	v1_20_4 = Version.of('1.20.4')
	snapshot = Version.of('abcdef')
	v1_20_5 = Version.of('1.20.5')

	yield TestVersions(v1_20_4, snapshot, v1_20_5)

	clear_manifest()
