import shulkr
from shulkr.minecraft.version import Version


def test_commit_version_stages_the_repos_src_directory(empty_repo):
	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=False, message_template='{}')

	# src must have been staged
	empty_repo.git.add.assert_called_once_with('client', 'server')


def test_commit_version_creates_a_commit(empty_repo):
	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=False, message_template='{}')

	# commit must have been called
	empty_repo.git.commit.assert_called_once()


def test_commit_version_replaces_all_brackets_with_the_version(empty_repo):
	# Call commit_version
	message_template = '{} {}'
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=False, message_template=message_template)

	# commit must have been called
	expected_message = message_template.replace('{}', str(version))
	empty_repo.git.commit.assert_called_once_with(message=expected_message)


def test_commit_version_with_existing_commits_and_undo_renamed_vars_adds_note_to_commit_message(nonempty_repo):
	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=True, message_template='{}')

	# commit must have been called
	expected_message = f'{version}\n\nRenamed variables reverted'
	nonempty_repo.git.commit.assert_called_once_with(message=expected_message)


def test_create_version_with_undo_renamed_vars_on_repo_with_no_commits_does_not_call_undo_renames(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_not_called()


def test_create_version_with_undo_renamed_vars_on_repo_with_one_commit_calls_undo_renames(mocker, nonempty_repo):
	# Mock
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_called_once()


def test_create_version_with_tag_false_does_not_call_tag_version(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, undo_renamed_vars=False, message_template='{}', tag=False)

	# tag_version must have been called
	shulkr.tag_version.assert_not_called()


def test_create_version_with_tag_true_calls_tag_version(mocker, empty_repo):
	# Mock
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version, undo_renamed_vars=False, message_template='{}', tag=True)

	# tag_version must have been called
	shulkr.tag_version.assert_called_once_with(version)
