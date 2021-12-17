import git
import pytest

import shulkr
from shulkr.minecraft.version import Version


def test_commit_version_stages_the_repos_src_directory(mocker):
	# Create a mock repo
	mocker.patch('git.Repo')
	repo = git.Repo()
	git_add = mocker.patch.object(repo, 'add')
	mocker.patch.object(repo.index, 'commit')

	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(repo, version, undo_renamed_vars=False, message_template='{}')

	# src must have been staged
	git_add.assert_called_once_with('src')


def test_commit_version_creates_a_commit(mocker):
	# Create a mock repo
	mocker.patch('git.Repo')
	repo = git.Repo()
	mocker.patch.object(repo, 'add')
	git_commit = mocker.patch.object(repo.index, 'commit')

	# Call commit_version
	version = Version('1.18.1', 0)
	shulkr.commit_version(repo, version, undo_renamed_vars=False, message_template='{}')

	# commit must have been called
	git_commit.assert_called_once()


def test_commit_version_replaces_all_brackets_with_the_version(mocker):
	# Create a mock repo
	mocker.patch('git.Repo')
	repo = git.Repo()
	mocker.patch.object(repo, 'add')
	git_commit = mocker.patch.object(repo.index, 'commit')

	# Call commit_version
	message_template = '{} {}'
	version = Version('1.18.1', 0)
	shulkr.commit_version(repo, version, undo_renamed_vars=False, message_template=message_template)

	# commit must have been called
	expected_message = message_template.replace('{}', str(version))
	git_commit.assert_called_once_with(expected_message)


def test_create_version_with_undo_renamed_vars_on_repo_with_no_commits_does_not_call_undo_renames(mocker):
	# Mock
	mocker.patch('git.Repo')
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	repo = git.Repo()

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(repo, version, undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_not_called()


def test_create_version_with_undo_renamed_vars_on_repo_with_one_commit_calls_undo_renames(mocker):
	# Mock
	mocker.patch('git.Commit')
	mocker.patch('git.Repo')
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.undo_renames')
	mocker.patch('shulkr.commit_version')

	repo = git.Repo()
	mocker.patch.object(repo, 'iter_commits', return_value=[git.Commit()])

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(repo, version, undo_renamed_vars=True, message_template=None, tag=False)

	# Assert that undo_renames was not called
	shulkr.undo_renames.assert_called_once()


def test_create_version_with_tag_false_does_not_call_tag_version(mocker):
	# Mock
	mocker.patch('git.Repo')
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Create a fake git repo
	repo = git.Repo()

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(repo, version, undo_renamed_vars=False, message_template='{}', tag=False)

	# tag_version must have been called
	shulkr.tag_version.assert_not_called()


def test_create_version_with_tag_true_calls_tag_version(mocker):
	# Mock
	mocker.patch('git.Repo')
	mocker.patch('shulkr.generate_sources')
	mocker.patch('shulkr.commit_version')
	mocker.patch('shulkr.tag_version')

	# Create a fake git repo
	repo = git.Repo()

	# Call create_version
	version = Version('1.18.1', 0)
	shulkr.create_version(repo, version, undo_renamed_vars=False, message_template='{}', tag=True)

	# tag_version must have been called
	shulkr.tag_version.assert_called_once_with(repo, version)
