import os
import shutil
import subprocess
import tempfile
from typing import List

import pytest


class RunParams:
	def __init__(
		self,
		versions: List[str],
		repo_path: str,
		undo_renamed_vars: bool
	) -> None:

		self.versions = versions
		self.repo_path = repo_path
		self.undo_renamed_vars = undo_renamed_vars


def create_command(
	versions: List[str],
	mappings: str,
	repo_path: str,
	undo_renamed_vars: bool
) -> List[str]:

	command = ['pipenv', 'run', 'start', '-p', repo_path, '--mappings', mappings]
	if undo_renamed_vars:
		command.append('-u')

	command.extend(versions)

	return command


def _run(versions: List[str], mappings: str, undo_renamed_vars: bool) -> None:
	with tempfile.TemporaryDirectory(prefix='shulkr') as repo_path:
		try:
			command = create_command(versions, mappings, repo_path, undo_renamed_vars)
			p = subprocess.run(command, stderr=subprocess.PIPE)

		except KeyboardInterrupt as e:
			if os.path.exists(repo_path):
				shutil.rmtree(repo_path)

			raise e

		if p.returncode != 0:
			if os.path.exists(repo_path):
				shutil.rmtree(repo_path)

			raise Exception(p.stderr.decode())

		yield RunParams(versions, repo_path, undo_renamed_vars)


@pytest.fixture(
	scope='session',
	params=[
		# Testing every combination of mappings to undo_variable_renames will
		# take too long, so just mix and match
		(['1.17.1', '1.18'], 'mojang', False),
	]
)
def run_mojang(request):
	versions, mappings, undo_variable_renames = request.param
	yield from _run(versions, mappings, undo_variable_renames)


@pytest.fixture(
	scope='session',
	params=[
		# Testing every combination of mappings to undo_variable_renames will
		# take too long, so just mix and match
		(['1.17.1', '1.18'], 'yarn', True),
	]
)
def run_yarn(request):
	versions, mappings, undo_variable_renames = request.param
	yield from _run(versions, mappings, undo_variable_renames)
