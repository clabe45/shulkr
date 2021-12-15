import os
import re
from shutil import rmtree
import subprocess
import zipfile


LOOM_CACHE = os.path.expanduser('~/.gradle/caches/fabric-loom')


def _clear_loom_cache() -> None:
	if os.path.exists(LOOM_CACHE):
		rmtree(LOOM_CACHE)


def _replace_in_file(path: str, pattern: str, replacement: str) -> None:
	with open(path, 'r') as f:
		updated = re.sub(pattern, replacement, f.read())

	with open(path, 'w') as f:
		f.write(updated)


def generate_sources(source_repo: str, mapping_version: str) -> None:
	_clear_loom_cache()

	end = mapping_version.index('+')
	minecraft_version = mapping_version[:end]

	# 1. Configure gradle, specifying which version to generate
	gradle_props = os.path.join('fabric-example-mod', 'gradle.properties')
	_replace_in_file(gradle_props, r'minecraft_version=.*\n', f'minecraft_version={minecraft_version}\n')
	_replace_in_file(gradle_props, r'yarn_mappings=.*\n', f'yarn_mappings={mapping_version}\n')

	# 2. Generate source code
	subprocess.run(['gradle', 'genSources'], cwd='fabric-example-mod')

	# 3. Extract source code
	jar_path = os.path.join(
		LOOM_CACHE,
		minecraft_version,
		'minecraft-merged.jar'
	)

	with zipfile.ZipFile(jar_path) as zip:
		src_dir = os.path.join(source_repo, 'src')
		zip.extractall(src_dir)
