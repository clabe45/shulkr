import os
import subprocess

from shulkr.minecraft.source import generate_sources


class SubprocessMock:
	def __init__(self, returncode=0, stderr=None):
		self.returncode = returncode
		self.stderr = stderr


def test_generate_sources_runs_decompiler(mocker, repo, versions, root_dir):
	subprocess_run = mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('shutil.move')
	mocker.patch('os.makedirs')

	generate_sources(repo, versions.snapshot)

	decompiler_dir = os.path.join(root_dir, 'shulkr', 'DecompilerMC')
	calls = [
		mocker.call(
			[
				'python3',
				'main.py',
				'--mcv',
				str(versions.snapshot),
				'-s',
				env,
				'-c',
				'-f',
				'-q'
			],
			stderr=subprocess.PIPE,
			cwd=decompiler_dir
		)
		for env in ('client', 'server')
	]
	subprocess_run.assert_has_calls(calls)


def test_generate_sources_moves_sources_to_repo(mocker, repo, versions, root_dir):
	repo_dir = 'foo'
	repo.working_tree_dir = repo_dir

	mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('os.makedirs')
	move = mocker.patch('shutil.move')

	generate_sources(repo, versions.snapshot)

	decompiler_dir = os.path.join(root_dir, 'shulkr', 'DecompilerMC')
	calls = [
		mocker.call(
			os.path.join(decompiler_dir, 'src', str(versions.snapshot), env),
			os.path.join(repo_dir, env, 'src')
		)
		for env in ('client', 'server')
	]
	move.assert_has_calls(calls)
