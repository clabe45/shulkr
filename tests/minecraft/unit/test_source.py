import os
import subprocess

from mint.repo import Repo
import pytest

from minecraft.source import generate_sources


class GitTree:
	def __init__(self, name: str = None) -> None:
		self.name = name


class SubprocessMock:
	def __init__(self, returncode=0, stderr=None):
		self.returncode = returncode
		self.stderr = stderr


def create_repo(path: str, mocker):
	def null_fn(*args, **kwargs):
		return None

	repo = mocker.create_autospec(Repo(None, check_path=False))
	repo.path = path

	repo.git.checkout = null_fn
	repo.git.clean = null_fn
	repo.git.fetch = null_fn
	repo.git.reset = null_fn

	return repo


@pytest.fixture
def yarn_repo(mocker):
	repo = create_repo('foo/.yarn', mocker)
	mocker.patch('minecraft.source.Repo.clone', return_value=repo)
	yield repo


@pytest.fixture
def decompiler_mc_repo(mocker):
	repo = create_repo('foo/.DecompilerMC', mocker)
	mocker.patch('minecraft.source.Repo.clone', return_value=repo)
	yield repo


def test_generate_sources_with_yarn_runs_decompiler(mocker, versions, yarn_repo):
	root_path = 'foo'
	decompiler_dir = os.path.join(root_path, '.DecompilerMC')

	subprocess_run = mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('shutil.move')
	mocker.patch('os.makedirs')

	generate_sources(versions.snapshot, 'yarn', root_path, root_path)

	decompiler_dir = os.path.join(root_path, '.yarn')
	subprocess_run.assert_called_once_with(
		['./gradlew', 'decompileCFR'],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		cwd=decompiler_dir
	)


def test_generate_sources_with_yarn_moves_sources_to_repo(mocker, versions, yarn_repo):
	root_path = 'foo'
	decompiler_dir = os.path.join(root_path, '.DecompilerMC')

	mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('os.makedirs')
	move = mocker.patch('shutil.move')

	generate_sources(versions.snapshot, 'yarn', root_path, root_path)

	decompiler_dir = os.path.join(root_path, '.yarn')
	move.assert_called_once_with(
		os.path.join(decompiler_dir, 'namedSrc'),
		os.path.join(root_path, 'src')
	)


def test_generate_sources_with_mojang_runs_decompiler(mocker, versions, decompiler_mc_repo):
	root_path = 'foo'
	decompiler_dir = os.path.join(root_path, '.DecompilerMC')

	subprocess_run = mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('shutil.move')
	mocker.patch('os.makedirs')

	generate_sources(versions.snapshot, 'mojang', root_path, root_path)

	decompiler_dir = os.path.join(root_path, '.DecompilerMC')
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


def test_generate_sources_with_mojang_moves_sources_to_repo(mocker, versions, decompiler_mc_repo):
	root_path = 'foo'
	decompiler_dir = os.path.join(root_path, '.DecompilerMC')

	mocker.patch(
		'subprocess.run',
		return_value=SubprocessMock()
	)
	mocker.patch('shutil.rmtree')
	mocker.patch('os.makedirs')
	move = mocker.patch('shutil.move')

	generate_sources(versions.snapshot, 'mojang', root_path, root_path)

	calls = [
		mocker.call(
			os.path.join(decompiler_dir, 'src', str(versions.snapshot), env),
			os.path.join(root_path, env, 'src')
		)
		for env in ('client', 'server')
	]
	move.assert_has_calls(calls)
