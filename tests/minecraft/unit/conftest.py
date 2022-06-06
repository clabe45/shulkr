import os
from unittest.mock import MagicMock

import pytest

from minecraft.version import Version, clear_manifest, load_manifest


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
	load_manifest(MANIFEST_DATA, earliest_supported_version_id='abcdef')

	snapshot = Version.of('abcdef')
	release = Version.of('1.0.0')

	yield TestVersions(snapshot, release)

	clear_manifest()
