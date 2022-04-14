import shulkr
from shulkr.minecraft.version import Version


def test_create_version_with_undo_renamed_vars_on_repo_with_no_commits_does_not_call_undo_renames(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, mappings='yarn', undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_not_called()


def test_create_version_with_undo_renamed_vars_on_repo_with_one_commit_calls_undo_renames(mocker, nonempty_repo):
	# Mock
	mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, mappings='yarn', undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_called_once()


def test_create_version_with_tag_false_does_not_call_tag_version(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, mappings='yarn', undo_renamed_vars=False, message_template='{}', tag=False)

	# tag_version must have been called
	shulkr.tag_version.assert_not_called()


def test_create_version_with_tag_true_calls_tag_version(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, mappings='yarn', undo_renamed_vars=False, message_template='{}', tag=True)

	# tag_version must have been called
	shulkr.tag_version.assert_called_once_with(version)
