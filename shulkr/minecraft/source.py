import os
import shutil
import subprocess

from git import Repo

from ..git import head_has_commits
from .version import Version


def generate_sources(repo: Repo, version: Version) -> None:
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
		if head_has_commits(repo):
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
