import os
from shutil import move, rmtree
import subprocess

from git import Repo

from .version import Version


def generate_sources(source_repo: str, version: Version) -> None:
	# 1. Generate source code there
	subprocess.run(['python3', 'main.py', '--mcv', str(version), '-c', '-f', '-q'], cwd='DecompilerMC')

	# 2. Move the generated source code to the target repo
	dest_src_dir = os.path.join(source_repo, 'src')
	if os.path.exists(dest_src_dir):
		rmtree(dest_src_dir)

	move(
		os.path.join('DecompilerMC', 'src'),
		source_repo
	)
