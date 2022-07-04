from unittest.mock import MagicMock

from minecraft.version import Version
import pytest

from shulkr import app


@pytest.fixture
def versions():
	return [
		Version(id='1.18', index=0),
		Version(id='1.19', index=1)
	]


@pytest.fixture
def mock_all(mocker, versions):
	mocker.patch('shulkr.app.load_manifest')
	mocker.patch('shulkr.app.sys')
	mocker.patch('shulkr.app.parse_args')
	mocker.patch('shulkr.app.os')
	mocker.patch('shulkr.app.init_repo')
	mocker.patch('shulkr.app.is_compatible')
	mocker.patch('shulkr.app.init_config')
	mocker.patch('shulkr.app.ensure_gitignore_exists')
	mocker.patch('shulkr.app.Version.patterns', return_value=versions)
	mocker.patch('shulkr.app.get_latest_generated_version')
	mocker.patch('shulkr.app.create_version')


def test_run_loads_version_manifest(mock_all):
	app.run()

	app.load_manifest.assert_called_once_with()


def test_run_calls_parse_args(mock_all, mocker):
	mocker.patch('shulkr.app.sys.argv', ['shulkr', '--repo', 'path/to/repo'])

	app.run()

	app.parse_args.assert_called_once_with(['--repo', 'path/to/repo'])


def test_run_calls_init_repo(mocker, mock_all):
	app.os.path.join.return_value = 'full/path/to/repo'

	app.run()

	app.init_repo.assert_called_once_with('full/path/to/repo')


def test_run_with_unsupported_repo_exits_with_error(mock_all):
	app.is_compatible.return_value = False

	app.run()

	app.sys.exit.assert_called_once_with(4)


def test_run_calls_init_config(mock_all):
	app.parse_args.return_value = MagicMock(
		mappings='mappings',
		message='message',
		tag=True,
		undo_renamed_vars=True
	)
	app.os.path.join.return_value = 'full/path/to/repo'

	app.run()

	app.init_config.assert_called_once_with(
		'full/path/to/repo',
		'mappings',
		'message',
		True,
		True
	)


def test_run_calls_ensure_gitignore_exists(mock_all):
	app.run()

	app.ensure_gitignore_exists.assert_called_once_with()


def test_run_with_multiple_versions_calls_create_version_for_each_version(mocker, mock_all, versions):
	app.run()

	app.create_version.assert_has_calls([
		mocker.call(version) for version in versions
	])


def test_run_without_any_versions_exits_with_error(mock_all):
	app.Version.patterns.return_value = []

	app.run()

	app.sys.exit.assert_called_once_with(3)
