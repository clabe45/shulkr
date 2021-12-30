import os
import shutil
import subprocess

from git import Repo

from .version import Version


def generate_sources(repo: Repo, version: Version) -> None:
	script_dir = os.path.dirname(__file__)
	decompiler_dir = os.path.realpath(
		os.path.join(script_dir, '..', 'DecompilerMC')
	)

	dest_src_dir = os.path.join(repo.working_tree_dir, 'src')
	if os.path.exists(dest_src_dir):
		shutil.rmtree(dest_src_dir)

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

		# Move the generated source code to the target repo
		shutil.move(
			os.path.join(decompiler_dir, 'src', str(version)),
			dest_src_dir
		)

	except BaseException as e:
		# Undo src/ deletion
		print('Resetting working tree')
		repo.git.restore('src')
		raise e

	finally:
		# Remove large generated files so they won't end up in the build!
		for subdir in ('mappings', 'src', 'tmp', 'versions'):
			path = os.path.join(decompiler_dir, subdir)
			if os.path.exists(path):
				shutil.rmtree(path)
