from minecraft.version import Version

import shulkr
from shulkr.config import Config
from shulkr.version import get_latest_generated_version


def test_create_version_calls_generate_sources_with_mappings_from_config_and_correct_version(mocker, config: Config, empty_repo):
	# Set mappings in config
	config.mappings = 'foo'

	# Mock
	mocker.patch('shulkr.version.generate_sources')

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# generate_sources() should have been called with the correct arguments
	shulkr.version.generate_sources.assert_called_once_with(version, 'foo', empty_repo.path)


def test_create_version_with_undo_renamed_vars_on_repo_with_no_commits_does_not_call_undo_renames(mocker, config, empty_repo):
	# Mock
	# mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.version.generate_sources')
	mocker.patch('shulkr.version.undo_renames')

	# Call create_version
	config.undo_renamed_vars = True
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# Assert that undo_renames was not called
	shulkr.version.undo_renames.assert_not_called()


def test_create_version_with_undo_renamed_vars_on_repo_with_one_commit_calls_undo_renames(mocker, config, nonempty_repo):
	# Mock
	# mocker.patch('shulkr.open', create=True)
	mocker.patch('shulkr.version.generate_sources')
	mocker.patch('shulkr.version.undo_renames')

	# Call create_version
	config.undo_renamed_vars = True
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# Assert that undo_renames was not called
	shulkr.version.undo_renames.assert_called_once()


def test_create_version_with_yarn_mappings_stages_the_src_directory(mocker, config, empty_repo, yarn_mappings):
	mocker.patch('shulkr.version.generate_sources')

	# Call _commit_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# src needs to have been staged
	empty_repo.git.add.assert_called_once_with('src')


def test_create_version_with_mojang_mappings_stages_the_src_directory(mocker, config, empty_repo, mojang_mappings):
	mocker.patch('shulkr.version.generate_sources')

	# Call _commit_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# client and server need to have been staged
	empty_repo.git.add.assert_called_once_with('src')


def test_create_version_creates_a_commit(mocker, config, empty_repo):
	mocker.patch('shulkr.version.generate_sources')

	# Call _commit_version
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# commit must have been called
	empty_repo.git.commit.assert_called_once()


def test_create_version_replaces_all_brackets_with_the_version(mocker, config, empty_repo):
	mocker.patch('shulkr.version.generate_sources')

	# Call _commit_version
	config.message_template = '{} {}'
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# commit must have been called
	expected_message = config.message_template.replace('{}', str(version))
	empty_repo.git.commit.assert_called_once_with(message=expected_message)


def test_create_version_with_existing_commits_and_undo_renamed_vars_adds_note_to_commit_message(mocker, config, nonempty_repo):
	mocker.patch('shulkr.version.generate_sources')

	# Call _commit_version
	config.undo_renamed_vars = True
	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	# commit must have been called
	expected_message = f'{version}\n\nRenamed variables reverted'
	nonempty_repo.git.commit.assert_called_once_with(message=expected_message)


def test_create_version_with_tag_calls_git_tag(mocker, config, nonempty_repo):
	mocker.patch('shulkr.version.generate_sources')

	version = Version('1.18.1', 0)
	shulkr.create_version(version)

	nonempty_repo.git.tag.assert_called_once_with(version)


def test_get_latest_generated_version_with_repo_with_one_version_returns_version(mocker, nonempty_repo):
	mocker.patch('shulkr.version.Version.of')

	# nonempty_repo contains one commit (the snapshot)
	get_latest_generated_version()

	shulkr.version.Version.of.assert_called_once_with('abcdef')
