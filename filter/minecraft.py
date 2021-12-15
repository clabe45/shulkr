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


def _clear_loom_cache() -> None:
	if os.path.exists(LOOM_CACHE):
		rmtree(LOOM_CACHE)


def _replace_in_file(path: str, pattern: str, replacement: str) -> None:
	with open(path, 'r') as f:
		updated = re.sub(pattern, replacement, f.read())

	with open(path, 'w') as f:
		f.write(updated)


def generate_sources(source_repo: str, minecraft_version: str) -> None:
	_clear_loom_cache()

	# 1. Checkout minecraft version in MCP repo
	repo = Repo('MCP-Reborn')
	orig_head = repo.head
	for commit in repo.iter_commits():
		if commit.message.startswith(f'Updated to {minecraft_version}') \
		or commit.message.startswith(f'Update to {minecraft_version}'):
			repo.git.checkout(commit)
			break

	else:
		raise MinecraftVersionNotFoundError(minecraft_version)

	# 2. Generate source code there
	subprocess.run(['gradle', 'setup'], cwd='MCP-Reborn')

	# 3. Move the generated source code to the target repo
	move(
		os.path.join('MCP-Reborn', 'src'),
		os.path.join(source_repo)
	)

	# 4. Checkout original commit
	repo.git.checkout(orig_head)
