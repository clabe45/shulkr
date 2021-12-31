import os
import shutil
import subprocess
from typing import List

import pytest

from shulkr.minecraft.version import Version, load_manifest


class RunParams:
	def __init__(self, repo_path: str, versions: List[Version]) -> None:
		self.repo_path = repo_path
		self.versions = versions


@pytest.fixture(scope='session', params=[['1.18', '1.18.1']])
def run(request):
	version_names = request.param
	script_dir = os.path.dirname(__file__)
	repo_path = os.path.join(script_dir, 'repo')

	p = subprocess.Popen(['pipenv', 'run', 'start', '--repo', repo_path] + version_names)
	try:
		stdout, stderr = p.communicate()
	except KeyboardInterrupt:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

	if p.returncode != 0:
		if os.path.exists(repo_path):
			shutil.rmtree(repo_path)

		raise Exception(stderr)

	load_manifest()
	versions = [Version.of(name) for name in version_names]
	yield RunParams(repo_path, versions)

	shutil.rmtree(repo_path)
