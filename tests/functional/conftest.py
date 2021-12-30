import os
import shutil
import subprocess

import pytest


class GenerateSourceFixture:
	def __init__(self, repo_path: str) -> None:
		self.repo_path = repo_path


@pytest.fixture(scope="session")
def generate_1_18():
	script_dir = os.path.dirname(__file__)
	repo_path = os.path.join(script_dir, 'repo')

	p = subprocess.Popen(['pipenv', 'run', 'start', '--repo', repo_path, '1.18'])
	try:
		stdout, stderr = p.communicate()
	except KeyboardInterrupt:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

	if p.returncode != 0:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

		raise Exception(stderr)

	yield GenerateSourceFixture(repo_path)

	shutil.rmtree(repo_path)
