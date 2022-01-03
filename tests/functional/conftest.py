import os
import shutil
import subprocess
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
	repo_path: str,
	undo_renamed_vars: bool
) -> List[str]:

	command = ['pipenv', 'run', 'start', '-p', repo_path]
	if undo_renamed_vars:
		command.append('-u')

	command.extend(versions)

	return command


def _run(versions: List[str], undo_renamed_vars: bool) -> None:
	script_dir = os.path.dirname(__file__)
	repo_path = os.path.join(script_dir, 'repo')

	try:
		command = create_command(versions, repo_path, undo_renamed_vars)
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

	shutil.rmtree(repo_path)


@pytest.fixture(
	scope='session',
	params=[
		(['1.17.1', '1.18'], False),
		(['1.17.1', '1.18'], True)
	]
)
def run(request):
	versions, undo_variable_renames = request.param
	yield from _run(versions, undo_variable_renames)
