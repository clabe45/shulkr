from subprocess import CalledProcessError
from unittest.mock import ANY

import pytest

import command
from command import Command, CommandError


SUBPROCESS_ANY_ARGS = {
	'cwd': ANY,
	'check': ANY,
	'capture_output': ANY,
	'text': ANY,
}


class GitError(CommandError):
	pass


@pytest.fixture(autouse=True)
def processes(mocker) -> None:
	mocker.patch('command.subprocess.run')
	mocker.patch('command.shutil.which', return_value=True)


@pytest.fixture
def git() -> Command:
	return Command('git', working_dir='/foo/bar', error=GitError)


class TestGitCommand:
	def test_getattr_calls_subprocess_with_cwd_set_to_repo_path(self, git):
		git.status()

		subprocess_args = {
			**SUBPROCESS_ANY_ARGS,
			'cwd': '/foo/bar'
		}

		command.subprocess.run.assert_called_once_with(
			ANY,
			**subprocess_args
		)

	def test_getattr_with_no_arguments_calls_corresponding_git_subcommand(self, git):
		git.status()

		command.subprocess.run.assert_called_once_with(
			['git', 'status'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_positional_argument_calls_corresponding_git_subcommand_concatenated_with_argument(self, git):
		git.status('src')

		command.subprocess.run.assert_called_once_with(
			['git', 'status', 'src'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_nonboolean_keyword_argument_calls_corresponding_git_subcommand_concatenated_with_formatted_keyword_argument(self, git):
		git.log(n=3)

		command.subprocess.run.assert_called_once_with(
			['git', 'log', '-n', '3'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_1_sets_the_corresponding_option_to_1(self, git):
		git.log(n=1)

		# It should not be 'git log -n' - it should be 'git log -n 1'
		command.subprocess.run.assert_called_once_with(
			['git', 'log', '-n', '1'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_true_calls_corresponding_git_subcommand_concatenated_with_corresponding_flag(self, git):
		git.log(oneline=True)

		command.subprocess.run.assert_called_once_with(
			['git', 'log', '--oneline'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_keyword_argument_set_to_false_calls_corresponding_git_subcommand_concatenated_without_corresponding_flag(self, git):
		git.log(oneline=False)

		command.subprocess.run.assert_called_once_with(
			['git', 'log'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_with_one_positional_argument_and_one_keyword_argument_calls_git_with_the_keyword_argument_before_the_positional_argument(self, git):
		git.log('HEAD', oneline=True)

		command.subprocess.run.assert_called_once_with(
			['git', 'log', '--oneline', 'HEAD'],
			**SUBPROCESS_ANY_ARGS
		)

	def test_getattr_raises_correct_error_when_subprocess_raises_an_error(self, git):
		command.subprocess.run.side_effect = CalledProcessError(
			1,
			'git',
			'some error message'
		)

		with pytest.raises(GitError):
			git.status()
