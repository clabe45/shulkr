import os

from command import Command


class Gradle(Command):
	def __init__(self, project_dir: str) -> None:
		exec = Gradle._executable(project_dir)
		super().__init__(exec, working_dir=project_dir)

	def __getattr__(self, name: str):
		super_func = super().__getattr__(name)

		def func(*args, **kwargs):
			return super_func(
				name,
				*args,
				# `--quiet` prevents the commands from being run interactively
				quiet=True,
				**kwargs
			)

		return func

	@staticmethod
	def _executable(project_dir: str) -> bool:
		"""
		Get the path to gradlew or gradle (if gradlew is not found)
		"""

		gradlew_exec = os.path.join(
			os.path.abspath(project_dir),
			'gradlew.bat' if os.name == 'nt' else 'gradlew'
		)
		if os.path.exists(gradlew_exec):
			return gradlew_exec

		return 'gradle'
