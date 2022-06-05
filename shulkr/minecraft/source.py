import os
import shutil
import subprocess

from mint.repo import Repo

from shulkr.git import get_repo, head_has_versions
from .version import Version


DECOMPILER_MC_REMOTE_URL = 'https://github.com/hube12/DecompilerMC.git'
YARN_REMOTE_URL = 'https://github.com/FabricMC/yarn.git'


def detect_mappings() -> str:
	repo = get_repo()

	subdirectories = set([tree.name for tree in repo.head.commit.tree.trees])
	if subdirectories == set(['client', 'server']):
		# DecompilerMC does not support merged sources
		return 'mojang'

	if subdirectories == set(['src']):
		# Merged sources
		return 'yarn'

	raise Exception('Unable to detect mappings from previous commit')


def _setup_decompiler(local_dir: str, remote_url: str) -> Repo:
	repo = get_repo()

	decompiler_dir = os.path.realpath(
		os.path.join(repo.path, local_dir)
	)

	if os.path.exists(
		os.path.join(decompiler_dir, '.git')
	):
		# Used cached yarn repo
		return Repo(decompiler_dir)
	else:
		# Clone the yarn repo
		print(f'- Cloning {remote_url} into {decompiler_dir}')
		return Repo.clone(remote_url, decompiler_dir)


def _generate_sources_with_yarn(version: Version) -> None:
	repo = get_repo()

	decompiler_repo = _setup_decompiler('.yarn', YARN_REMOTE_URL)

	print(f'- Updating mappings to Minecraft {version}')

	# Get latest versions from remote
	decompiler_repo.git.fetch(prune=True)

	decompiler_repo.git.reset('HEAD', hard=True)
	decompiler_repo.git.clean(force=True, d=True)

	# Checkout version branch
	decompiler_repo.git.checkout(f'origin/{version}')

	print('- Running decompiler')

	try:
		# Generate source code
		p = subprocess.run(
			['./gradlew', 'decompileCFR'],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.PIPE,
			cwd=decompiler_repo.path
		)
		if p.returncode != 0:
			raise Exception(p.stderr.decode())

		# Output directory
		dest_src_dir = os.path.join(repo.path, 'src')

		# Remove existing top-level destination directory
		if os.path.exists(dest_src_dir):
			shutil.rmtree(dest_src_dir)

		# Move the generated source code to $repo_dir/src
		shutil.move(
			os.path.join(decompiler_repo.path, 'namedSrc'),
			dest_src_dir
		)

	except BaseException as e:
		# Undo src/ deletions
		if head_has_versions():
			repo.git.restore('src')
		else:
			path = os.path.join(repo.path, 'src')
			if os.path.exists(path):
				shutil.rmtree(path)

		raise e


def _generate_sources_with_mojang(version: Version) -> None:
	"""
	Generate sources with DecompilerMC, which uses Mojang's official mappings

	Args:
		version (Version):

	Raises:
		Exception: If DecompilerMC fails
	"""

	repo = get_repo()

	decompiler_repo = _setup_decompiler('.DecompilerMC', DECOMPILER_MC_REMOTE_URL)

	try:
		for env in ('client', 'server'):
			# Generate source code
			p = subprocess.run(
				[
					'python3',
					'main.py',
					'--mcv',
					str(version),
					'-s',
					env,
					'-c',
					'-f',
					'-q'
				],
				stderr=subprocess.PIPE,
				cwd=decompiler_repo.path
			)
			if p.returncode != 0:
				raise Exception(p.stderr.decode())

			# Top-level destination directory ($repo/client or $repo/server)
			dest_dir = os.path.join(repo.path, env)
			dest_src_dir = os.path.join(dest_dir, 'src')

			# Remove existing top-level destination directory
			if os.path.exists(dest_src_dir):
				shutil.rmtree(dest_src_dir)

			# Make top-level destination directory
			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)

			# Move the generated source code to $dest_dir/src
			shutil.move(
				os.path.join(decompiler_repo.path, 'src', str(version), env),
				dest_src_dir
			)

	except BaseException as e:
		# Undo src/ deletions
		if head_has_versions():
			repo.git.restore('client', 'server')
		else:
			for env in ('client', 'server'):
				path = os.path.join(repo.path, env, 'src')
				if os.path.exists(path):
					shutil.rmtree(path)

		raise e


def generate_sources(version: Version, mappings: str) -> None:
	if mappings == 'mojang':
		_generate_sources_with_mojang(version)

	elif mappings == 'yarn':
		_generate_sources_with_yarn(version)

	else:
		raise ValueError(f"Invalid mapping type '{mappings}'")
