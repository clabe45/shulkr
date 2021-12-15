import filter

import git
import pytest


def test_create_version_with_undo_renamed_vars_on_repo_with_no_commits_does_not_call_undo_renames(mocker):
	# Mock
	mocker.patch('git.Repo')
	mocker.patch('filter.generate_sources')
	mocker.patch('filter.undo_renames')
	mocker.patch('filter.commit_version')

	repo = git.Repo()
	mocker.patch.object(repo, 'bare', return_value=False)

	# Call create_version
	filter.create_version(repo, '1.18.1', undo_renamed_vars=True)

	# Assert that undo_renames was not called
	filter.undo_renames.assert_not_called()


def test_create_version_with_undo_renamed_vars_on_repo_with_one_commit_calls_undo_renames(mocker):
	# Mock
	mocker.patch('git.Commit')
	mocker.patch('git.Repo')

	mocker.patch('filter.generate_sources')
	mocker.patch('filter.undo_renames')
	mocker.patch('filter.commit_version')

	repo = git.Repo()
	mocker.patch.object(repo, 'bare', return_value=False)
	mocker.patch.object(repo, 'iter_commits', return_value=[git.Commit()])

	# Call create_version
	filter.create_version(repo, '1.18.1', undo_renamed_vars=True)

	# Assert that undo_renames was not called
	filter.undo_renames.assert_called_once()
