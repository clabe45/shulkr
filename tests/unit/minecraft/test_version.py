import pytest

from shulkr.minecraft.version import Version


class TestVersion:
	def test_next_of_snapshot_is_the_release(self, versions):
		assert versions.snapshot.next == versions.release

	def test_next_of_release_is_none(self, versions):
		assert versions.release.next is None

	def test_release_does_not_equal_snapshot(self, versions):
		assert versions.release != versions.snapshot

	def test_snapshot_is_less_than_release(self, versions):
		assert versions.snapshot < versions.release

	def test_release_is_greater_than_snapshot(self, versions):
		assert versions.release > versions.snapshot

	def test_snapshot_to_release_returns_list_containing_snapshot_and_release(self, versions):
		assert versions.snapshot.to(versions.release) == [versions.snapshot, versions.release]

	def test_snapshot_to_snapshot_returns_list_containing_snapshot(self, versions):
		assert versions.snapshot.to(versions.snapshot) == [versions.snapshot]

	def test_snapshot_to_none_returns_list_containing_snapshot_and_release(self, versions):
		assert versions.snapshot.to(None) == [versions.snapshot, versions.release]

	def test_snapshot_to_release_excluding_snapshots_returns_list_containing_release(self, versions):
		assert versions.snapshot.to(versions.release, snapshots=False) == [versions.release]

	def test_release_to_snapshot_raises_version_error(self, versions):
		with pytest.raises(ValueError):
			versions.release.to(versions.snapshot)

	def test_pattern_with_no_range_operator_returns_list_containing_version(self, versions):
		assert Version.pattern('1.0.0') == [versions.release]

	def test_pattern_with_two_dots_returns_list_containing_release(self, versions):
		assert Version.pattern('..') == [versions.release]

	def test_pattern_with_three_dots_returns_list_containing_snapshot_and_release(self, versions):
		assert Version.pattern('...') == [versions.snapshot, versions.release]

	def test_pattern_with_release_two_dots_returns_list_containing_release(self, versions):
		assert Version.pattern('1.0.0..') == [versions.release]

	def test_pattern_with_release_two_dots_release_returns_list_containing_release(self, versions):
		assert Version.pattern('1.0.0..1.0.0') == [versions.release]

	def test_pattern_with_snapshot_three_dots_release_returns_list_containing_snapshot_and_release(self, versions):
		assert Version.pattern('abcdef...1.0.0') == [versions.snapshot, versions.release]

	def test_patterns_with_empty_list_returns_empty_list(self, versions):
		assert Version.patterns([]) == []

	def test_patterns_with_one_positive_id_returns_corresponding_version(self, versions):
		assert Version.patterns(['1.0.0']) == [versions.release]

	def test_patterns_with_two_positive_identical_ids_returns_one_version(self, versions):
		assert Version.patterns(['1.0.0', '1.0.0']) == [versions.release]

	def test_patterns_with_one_positive_id_and_the_same_negative_id_returns_empty_list(self, versions):
		assert Version.patterns(['1.0.0', '-1.0.0']) == []

	def test_patterns_with_one_positive_id_and_the_same_negative_id_and_the_same_positive_id_returns_one_version(self, versions):
		assert Version.patterns(['1.0.0', '-1.0.0', '1.0.0']) == [versions.release]
