import os
from shutil import move, rmtree
import subprocess

from git import Repo

from .version import Version


def generate_sources(source_repo: str, version: Version) -> None:
	script_dir = os.path.dirname(__file__)
	decompiler_dir = os.path.join(script_dir, '..', 'DecompilerMC')

	# 1. Generate source code there
	subprocess.run(['python3', 'main.py', '--mcv', str(version), '-c', '-f', '-q'], cwd=decompiler_dir)

	# 2. Move the generated source code to the target repo
	dest_src_dir = os.path.join(source_repo, 'src')
	if os.path.exists(dest_src_dir):
		rmtree(dest_src_dir)

	move(
		os.path.join(decompiler_dir, 'src'),
		source_repo
	)
