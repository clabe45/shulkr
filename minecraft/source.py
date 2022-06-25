import os
import shutil
import subprocess

from mint.repo import Repo

from minecraft.version import Version


DECOMPILER_MC_REMOTE_URL = 'https://github.com/hube12/DecompilerMC.git'
YARN_REMOTE_URL = 'https://github.com/FabricMC/yarn.git'


def _setup_decompiler(local_dir: str, remote_url: str) -> Repo:
	if os.path.exists(
		os.path.join(local_dir, '.git')
	):
		# Used cached yarn repo
		return Repo(local_dir)
	else:
		# Clone the yarn repo
		print(f'- Cloning {remote_url} into {local_dir}')
		return Repo.clone(remote_url, local_dir)


def _generate_sources_with_yarn(version: Version, path: str) -> None:
	decompiler_path = os.path.join(path, '.yarn')
	decompiler_repo = _setup_decompiler(decompiler_path, YARN_REMOTE_URL)

	print(f'- Updating mappings to Minecraft {version}')

	# Get latest versions from remote
	decompiler_repo.git.fetch(prune=True)

	decompiler_repo.git.reset('HEAD', hard=True)
	decompiler_repo.git.clean(force=True, d=True)

	# Checkout version branch
	decompiler_repo.git.checkout(f'origin/{version}')

	print('- Running decompiler')

	# Generate source code
	p = subprocess.run(
		['./gradlew', 'decompileCFR'],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		cwd=decompiler_repo.path
	)
	if p.returncode != 0:
		raise Exception(p.stderr.decode())

	src_path = os.path.join(path, 'src')

	# Remove existing top-level destination directory
	if os.path.exists(src_path):
		shutil.rmtree(src_path)

	# Move the generated source code to $repo_dir/src
	shutil.move(
		os.path.join(decompiler_repo.path, 'namedSrc'),
		src_path
	)


def _generate_sources_with_mojang(version: Version, path: str) -> None:
	"""
	Decompiles a version of the Minecraft client with DecompilerMC (which uses
	Mojang's official mappings)

	Args:
		version (Version):

	Raises:
		Exception: If DecompilerMC fails
	"""

	decompiler_path = os.path.join(path, '.DecompilerMC')
	decompiler_repo = _setup_decompiler(decompiler_path, DECOMPILER_MC_REMOTE_URL)

	# Decompile client
	p = subprocess.run(
		[
			'python3',
			'main.py',
			'--mcv',
			str(version),
			'-s',
			'client',
			'-c',
			'-f',
			'-q'
		],
		stderr=subprocess.PIPE,
		cwd=decompiler_repo.path
	)
	if p.returncode != 0:
		raise Exception(p.stderr.decode())

	# Sources directory
	dest_src_dir = os.path.join(path, 'src')

	# Remove existing top-level destination directory
	if os.path.exists(dest_src_dir):
		shutil.rmtree(dest_src_dir)

	# Move the generated source code to $dest_dir/src
	shutil.move(
		os.path.join(decompiler_repo.path, 'src', str(version), 'client'),
		dest_src_dir
	)


def generate_sources(version: Version, mappings: str, path: str) -> None:
	if mappings == 'mojang':
		_generate_sources_with_mojang(version, path)

	elif mappings == 'yarn':
		_generate_sources_with_yarn(version, path)

	else:
		raise ValueError(f"Invalid mapping type '{mappings}'")
