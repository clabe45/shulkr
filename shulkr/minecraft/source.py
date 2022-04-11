import os
import shutil
import subprocess

from git import Repo

from shulkr.git import get_repo, head_has_commits
from .version import Version


YARN_REMOTE_URL = 'https://github.com/FabricMC/yarn.git'


def detect_mappings() -> str:
	repo = get_repo()

	subdirectories = set([tree.name for tree in repo.head.commit.tree.trees])
	print(subdirectories)
	if subdirectories == set(['client', 'server']):
		# DecompilerMC does not support merged sources
		return 'mojang'

	if subdirectories == set(['src']):
		# Merged sources
		return 'yarn'

	raise Exception('Unable to detect mappings from previous commit')


def _generate_sources_with_yarn(version: Version) -> None:
	repo = get_repo()

	decompiler_dir = os.path.realpath(
		os.path.join(repo.working_tree_dir, '.yarn')
	)

	if os.path.exists(
		os.path.join(decompiler_dir, '.git')
	):
		# Used cached yarn repo
		decompiler_repo = Repo(decompiler_dir)
	else:
		# Clone the yarn repo
		print(f'- Cloning {YARN_REMOTE_URL} into {decompiler_dir}')
		decompiler_repo = Repo.clone_from(YARN_REMOTE_URL, decompiler_dir)

	print(f'- Updating mappings to Minecraft {version}')

	# Get latest versions from remote
	decompiler_repo.git.fetch('--prune')

	decompiler_repo.git.reset('--hard', 'HEAD')
	decompiler_repo.git.clean('-fd')

	# Checkout version branch
	decompiler_repo.git.checkout(f'origin/{version}')

	print('- Running decompiler')

	try:
		# Generate source code
		p = subprocess.run(
			['./gradlew', 'decompileCFR'],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.PIPE,
			cwd=decompiler_dir
		)
		if p.returncode != 0:
			raise Exception(p.stderr.decode())

		# Output directory
		dest_src_dir = os.path.join(repo.working_tree_dir, 'src')

		# Remove existing top-level destination directory
		if os.path.exists(dest_src_dir):
			shutil.rmtree(dest_src_dir)

		# Move the generated source code to $repo_dir/src
		shutil.move(
			os.path.join(decompiler_dir, 'namedSrc'),
			dest_src_dir
		)

	except BaseException as e:
		# Undo src/ deletions
		if head_has_commits():
			repo.git.restore('src')
		else:
			path = os.path.join(repo.working_tree_dir, 'src')
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

	script_dir = os.path.dirname(__file__)
	decompiler_dir = os.path.realpath(
		os.path.join(script_dir, '..', 'DecompilerMC')
	)

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
				cwd=decompiler_dir
			)
			if p.returncode != 0:
				raise Exception(p.stderr.decode())

			# Top-level destination directory ($repo/client or $repo/server)
			dest_dir = os.path.join(repo.working_tree_dir, env)
			dest_src_dir = os.path.join(dest_dir, 'src')

			# Remove existing top-level destination directory
			if os.path.exists(dest_src_dir):
				shutil.rmtree(dest_src_dir)

			# Make top-level destination directory
			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)

			# Move the generated source code to $dest_dir/src
			shutil.move(
				os.path.join(decompiler_dir, 'src', str(version), env),
				dest_src_dir
			)

	except BaseException as e:
		# Undo src/ deletions
		if head_has_commits():
			repo.git.restore('client', 'server')
		else:
			for env in ('client', 'server'):
				path = os.path.join(repo.working_tree_dir, env, 'src')
				if os.path.exists(path):
					shutil.rmtree(path)

		raise e

	finally:
		# Remove large generated files so they won't end up in the build!
		for subdir in ('mappings', 'src', 'tmp', 'versions'):
			path = os.path.join(decompiler_dir, subdir)
			if os.path.exists(path):
				shutil.rmtree(path)


def generate_sources(version: Version, mappings: str) -> None:
	if mappings == 'mojang':
		_generate_sources_with_mojang(version)

	elif mappings == 'yarn':
		_generate_sources_with_yarn(version)

	else:
		raise ValueError(f"Invalid mapping type '{mappings}'")
