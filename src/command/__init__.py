import os
import shutil
import subprocess
from typing import Any, Dict, List


class BaseCommandError(Exception):
	"""
	Base class for all command errors
	"""


class CommandError(BaseCommandError):
	"""
	Error raised when a command fails
	"""

	def __init__(self, command: str, stderr: str, *args: object) -> None:
		super().__init__(*args)

		self.command = command
		self.stderr = stderr

	def __str__(self) -> str:
		return f'{self.command}:\n{self.stderr}'


class CommandNotFoundError(BaseCommandError):
	"""
	Error raised when a command is not found
	"""

	def __init__(self, command: str, *args: object) -> None:
		super().__init__(*args)

		self.command = command

	def __str__(self) -> str:
		return f'Command not found: {self.command}'


class Command:
	"""
	Context for running git commands

	Sample usage:
		git = GitCommand(PATH_TO_REPO)
		if not git.status(porcelain=True):
			git.commit(message='empty commit', allow_empty=True)

	Currently, options that require an '=' between the key and the value must be
	supplied as positional arguments:
		git.log('--format=%B')
	"""

	def __init__(
		self,
		executabale: str,
		working_dir: str = None,
		error=CommandError
	) -> None:
		"""
		Args:
			executabale (str): Name of the executable
			working_dir (str): Path to the working directory
			error (Exception): Error to raise when a command fails
		"""

		if not shutil.which(executabale):
			raise CommandNotFoundError(executabale)

		self._executable = executabale

		if working_dir is None:
			working_dir = os.getcwd()

		self._working_dir = working_dir

		self._error = error

	def _run_command(self, command: List[str]) -> str:
		"""
		Run the specified command

		Args:
			command (List[str]): Command to run

		Returns:
			str: Output of the command
		"""

		try:
			proc = subprocess.run(
				command,
				cwd=self._working_dir,
				check=True,
				capture_output=True,
				text=True
			)

			return proc.stdout.strip()

		except subprocess.CalledProcessError as e:
			# Convert the error to to the user-specified error type
			raise self._error(command, e.stderr) from e

	def __getattr__(self, name: str):
		"""
		Return the specified git subcommand as a function

		Args:
			name (str): Name of the subcommand
		"""

		def func(*args, **kwargs):
			subcommand = name.replace('_', '-')

			command = self._raw_command(
				subcommand,
				args,
				kwargs
			)
			return self._run_command(command)

		return func

	@staticmethod
	def _format_option(key: str, value: Any) -> List[str]:
		"""
		Format the specified option

		Args:
			key (str): Name of the option
			value (Any): Value of the option

		Returns:
			List[str]: Formatted option
		"""

		option = key.replace('_', '-')
		prefix = '-' if len(option) == 1 else '--'

		if value is True:
			return [f'{prefix}{option}']

		elif value is False:
			return []

		else:
			# Non-boolean value
			return [f'{prefix}{option}', str(value)]

	def _raw_command(
		self,
		subcommand: str,
		args: List[Any],
		kwargs: Dict[str, Any]
	) -> List[str]:
		"""
		Format the specified command

		Args:
			subcommand (str): Name of the subcommand
			args (List[Any]): Positional arguments
			kwargs (Dict[str, Any]): Keyword arguments

		Returns:
			List[str]: Formatted command
		"""

		options = [
			token for key, value in kwargs.items()
			for token in Command._format_option(key, value)
		]
		args = [str(arg) for arg in args]
		return [self._executable, subcommand, *options, *args]
