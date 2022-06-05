from unittest.mock import ANY

import pytest

import mint
from mint.command import GitCommand
from mint.repo import Repo


SUBPROCESS_ANY_ARGS = {
	'cwd': ANY,
	'shell': ANY,
	'check': ANY,
	'capture_output': ANY,
	'text': ANY,
}


@pytest.fixture(autouse=True)
def fs(mocker) -> None:
	mocker.patch('mint.command.subprocess.os.path.exists', return_value=True)
	mocker.patch('mint.command.subprocess.os.path.isfile', return_value=False)


@pytest.fixture(autouse=True)
def subprocess(mocker) -> None:
	mocker.patch('mint.command.subprocess')


@pytest.fixture
def repo() -> Repo:
	return Repo('foo')


@pytest.fixture
def git(repo: Repo) -> GitCommand:
	return GitCommand(repo.path)


class TestGitCommand:
	def test_getattr_calls_subprocess_with_cwd_set_to_repo_path(self, git, repo):
		git.status()

		subprocess_args = {
			**SUBPROCESS_ANY_ARGS,
			'cwd': repo.path
		}

		mint.command.subprocess.run.assert_called_once_with(
			ANY,
			**subprocess_args
		)

	def test_getattr_with_no_arguments_calls_corresponding_git_subcommand(self, git):
		git.status()

		mint.command.subprocess.run.assert_called_once_with(
			'git status',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_positional_argument_calls_corresponding_git_subcommand_concatenated_with_argument(self, git):
		git.status('src')

		mint.command.subprocess.run.assert_called_once_with(
			'git status src',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_nonboolean_keyword_argument_calls_corresponding_git_subcommand_concatenated_with_formatted_keyword_argument(self, git):
		git.log(n=3)

		mint.command.subprocess.run.assert_called_once_with(
			'git log -n 3',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_1_sets_the_corresponding_option_to_1(self, git):
		git.log(n=1)

		# It should not be 'git log -n' - it should be 'git log -n 1'
		mint.command.subprocess.run.assert_called_once_with(
			'git log -n 1',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_true_calls_corresponding_git_subcommand_concatenated_with_corresponding_flag(self, git):
		git.log(oneline=True)

		mint.command.subprocess.run.assert_called_once_with(
			'git log --oneline',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_false_calls_corresponding_git_subcommand_concatenated_without_corresponding_flag(self, git):
		git.log(oneline=False)

		mint.command.subprocess.run.assert_called_once_with(
			'git log',
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_positional_argument_and_one_keyword_argument_calls_git_with_the_keyword_argument_before_the_positional_argument(self, git):
		git.log('HEAD', oneline=True)

		mint.command.subprocess.run.assert_called_once_with(
			'git log --oneline HEAD',
			**SUBPROCESS_ANY_ARGS
		)
