from typing import Dict

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

load_manifest(MANIFEST_DATA, earliest_supported_version_id='abcdef')


class TestVersion:
	snapshot = Version.of('abcdef')
	release = Version.of('1.0.0')

	def test_next_of_snapshot_is_the_release(self):
		assert self.snapshot.next == self.release

	def test_next_of_release_is_none(self):
		assert self.release.next is None

	def test_release_does_not_equal_snapshot(self):
		assert self.release != self.snapshot

	def test_snapshot_is_less_than_release(self):
		assert self.snapshot < self.release

	def test_release_is_greater_than_snapshot(self):
		assert self.release > self.snapshot

	def test_snapshot_to_release_returns_list_containing_snapshot_and_release(self):
		assert self.snapshot.to(self.release) == [self.snapshot, self.release]

	def test_snapshot_to_snapshot_returns_list_containing_snapshot(self):
		assert self.snapshot.to(self.snapshot) == [self.snapshot]

	def test_snapshot_to_none_returns_list_containing_snapshot_and_release(self):
		assert self.snapshot.to(None) == [self.snapshot, self.release]

	def test_snapshot_to_release_excluding_snapshots_returns_list_containing_release(self):
		assert self.snapshot.to(self.release, snapshots=False) == [self.release]

	def test_release_to_snapshot_raises_version_error(self):
		with pytest.raises(ValueError):
			self.release.to(self.snapshot)

	def test_pattern_with_no_range_operator_returns_list_containing_version(self):
		assert Version.pattern('1.0.0') == [self.release]

	def test_pattern_with_two_dots_returns_list_containing_release(self):
		assert Version.pattern('..') == [self.release]

	def test_pattern_with_three_dots_returns_list_containing_snapshot_and_release(self):
		assert Version.pattern('...') == [self.snapshot, self.release]

	def test_pattern_with_release_two_dots_returns_list_containing_release(self):
		assert Version.pattern('1.0.0..') == [self.release]

	def test_pattern_with_release_two_dots_release_returns_list_containing_release(self):
		assert Version.pattern('1.0.0..1.0.0') == [self.release]

	def test_pattern_with_snapshot_three_dots_release_returns_list_containing_snapshot_and_release(self):
		assert Version.pattern('abcdef...1.0.0') == [self.snapshot, self.release]
