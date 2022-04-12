import os
import subprocess

from shulkr.minecraft.source import detect_mappings, generate_sources


class GitTree:
	def __init__(self, name: str = None) -> None:
		self.name = name


class SubprocessMock:
	def __init__(self, returncode=0, stderr=None):
		self.returncode = returncode
		self.stderr = stderr


def test_detect_mappings_with_yarn_commit_returns_yarn(mocker, nonempty_repo):
	mocker.patch.object(nonempty_repo.head.commit.tree, 'trees', [GitTree('src')])

	assert detect_mappings() == 'yarn'


def test_detect_mappings_with_mojang_commit_returns_mojang(mocker, nonempty_repo):
	mocker.patch.object(nonempty_repo.head.commit.tree, 'trees', [GitTree('client'), GitTree('server')])

	assert detect_mappings() == 'mojang'


def test_generate_sources_with_yarn_runs_decompiler(mocker, empty_repo, versions, root_dir):
	subprocess_run = mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('shutil.move')
	mocker.patch('os.makedirs')

	generate_sources(versions.snapshot, 'yarn')

	decompiler_dir = os.path.join(empty_repo.working_tree_dir, '.yarn')
	subprocess_run.assert_called_once_with(
		['./gradlew', 'decompileCFR'],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		cwd=decompiler_dir
	)


def test_generate_sources_with_yarn_moves_sources_to_repo(mocker, empty_repo, versions):
	mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('os.makedirs')
	move = mocker.patch('shutil.move')

	generate_sources(versions.snapshot, 'yarn')

	decompiler_dir = os.path.join(empty_repo.working_tree_dir, '.yarn')
	move.assert_called_once_with(
		os.path.join(decompiler_dir, 'namedSrc'),
		os.path.join(empty_repo.working_tree_dir, 'src')
	)


def test_generate_sources_with_mojang_runs_decompiler(mocker, empty_repo, versions, root_dir):
	subprocess_run = mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('shutil.move')
	mocker.patch('os.makedirs')

	generate_sources(versions.snapshot, 'mojang')

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


def test_generate_sources_with_mojang_moves_sources_to_repo(mocker, empty_repo, versions, root_dir):
	mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('os.makedirs')
	move = mocker.patch('shutil.move')

	generate_sources(versions.snapshot, 'mojang')

	decompiler_dir = os.path.join(root_dir, 'shulkr', 'DecompilerMC')
	calls = [
		mocker.call(
			os.path.join(decompiler_dir, 'src', str(versions.snapshot), env),
			os.path.join(empty_repo.working_tree_dir, env, 'src')
		)
		for env in ('client', 'server')
	]
	move.assert_has_calls(calls)
