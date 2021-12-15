import os
import re
from shutil import move, rmtree
import subprocess

from git import Repo


LOOM_CACHE = os.path.expanduser('~/.gradle/caches/fabric-loom')


class MinecraftError(Exception):
	pass


class MinecraftVersionNotFoundError(MinecraftError):
	pass


def get_manifest():
	global manifest
	if manifest is None:
		raw = json.load()
		manifest = Manifest.parse(raw)


def versions_between(a: Version, b: Version, include_snapshots=True) -> List[Version]:



def generate_sources(source_repo: str, minecraft_version: str) -> None:
	# 1. Generate source code there
	subprocess.run(['python3', 'main.py', '--mcv', minecraft_version, '-c', '-f', '-q'], cwd='DecompilerMC')

	# 2. Move the generated source code to the target repo
	dest_src_dir = os.path.join(source_repo, 'src')
	if os.path.exists(dest_src_dir):
		rmtree(dest_src_dir)

	move(
		os.path.join('DecompilerMC', 'src'),
		source_repo
	)

manifest = None
