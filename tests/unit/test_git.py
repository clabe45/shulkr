import shulkr
from shulkr.minecraft.version import Version


def test_commit_version_with_yarn_mappings_stages_the_src_directory(empty_repo, yarn_mappings):
	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=False, message_template='{}')

	# src needs to have been staged
	empty_repo.git.add.assert_called_once_with('src')


def test_commit_version_with_mojang_mappings_stages_the_src_directory(empty_repo, mojang_mappings):
	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(version, undo_renamed_vars=False, message_template='{}')

	# client and server need to have been staged
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
