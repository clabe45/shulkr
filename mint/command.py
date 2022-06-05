import os
import subprocess
from typing import Any, Dict, List


class GitCommandError(Exception):
	def __init__(self, command: str, stderr: str, *args: object) -> None:
		super().__init__(*args)

		self.command = command
		self.stderr = stderr

	def __str__(self) -> str:
		return f'{self.command}:\n{self.stderr}'


class GitCommand:
	"""
	Context for running git commands

	Sample usage:
		git = GitCommand(PATH_TO_REPO)
		if not git.status(porcelain=True):
			git.commit(message='empty commit', allow_empty=True)

	Currently, options that require an '=' between the key and the value must be
	supplied as positional arguments:
		git.log('--format="%B"')
	"""

	def __init__(self, path: str = None) -> None:
		if path is None:
			path = os.getcwd()

		self._path = path

	def _run_command(self, command: List[str]) -> str:
		try:
			proc = subprocess.run(
				' '.join(command),
				cwd=self._path,
				shell=True,
				check=True,
				capture_output=True,
				text=True
			)

			return proc.stdout.strip()

		except subprocess.CalledProcessError as e:
			raise GitCommandError(
				' '.join(command),
				e.stderr
			)

	def __getattr__(self, name: str):
		"""
		Return the specified git subcommand as a function

		Args:
			name (str): Name of the subcommand
		"""

		def func(*args, **kwargs):
			subcommand = name.replace('_', '-')

			command = GitCommand._raw_command(
				subcommand,
				args,
				kwargs
			)
			return self._run_command(command)

		return func

	@staticmethod
	def _format_value(value: Any):
		if not isinstance(value, str):
			value = str(value)

		if ' ' in value:
			escaped_value = value.replace("'", "\\'")
			return f"'{escaped_value}'"
		else:
			return value

	@staticmethod
	def _format_option(key: str, value: Any) -> List[str]:
		option = key.replace('_', '-')
		prefix = '-' if len(option) == 1 else '--'

		if value is True:
			return [f'{prefix}{option}']

		elif value is False:
			return []

		else:
			# Non-boolean value
			return [f'{prefix}{option}', GitCommand._format_value(value)]

	@staticmethod
	def _raw_command(
		subcommand: str,
		args: List[Any],
		kwargs: Dict[str, Any]
	) -> List[str]:

		options = [
			token for key, value in kwargs.items()
			for token in GitCommand._format_option(key, value)
		]
		args = [GitCommand._format_value(arg) for arg in args]
		return ['git', subcommand, *options, *args]
