import os
import shutil
import subprocess
from typing import List

import pytest


class RunParams:
	def __init__(self, repo_path: str, versions: List[str]) -> None:
		self.repo_path = repo_path
		self.versions = versions


def _run(versions: List[str]):
	script_dir = os.path.dirname(__file__)
	repo_path = os.path.join(script_dir, 'repo')

	try:
		p = subprocess.run(
			['pipenv', 'run', 'start', '--repo', repo_path] + versions,
			stderr=subprocess.PIPE
		)

	except KeyboardInterrupt as e:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

		raise e

	if p.returncode != 0:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

		raise Exception(p.stderr.decode())

	yield RunParams(repo_path, versions)

	shutil.rmtree(repo_path)


@pytest.fixture(scope='session', params=[['1.18', '1.18.1']])
def run(request):
	yield from _run(request.param)
