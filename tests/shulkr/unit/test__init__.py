from unittest.mock import MagicMock

from minecraft.version import Version
import pytest

import shulkr


@pytest.fixture
def versions():
	return [
		Version(id='1.18', index=0),
		Version(id='1.19', index=1)
	]


@pytest.fixture
def mock_all(mocker, versions):
	mocker.patch('shulkr.load_manifest')
	mocker.patch('shulkr.sys')
	mocker.patch('shulkr.parse_args')
	mocker.patch('shulkr.os')
	mocker.patch('shulkr.init_repo')
	mocker.patch('shulkr.is_compatible')
	mocker.patch('shulkr.init_config')
	mocker.patch('shulkr.ensure_gitignore_exists')
	mocker.patch('shulkr.Version.patterns', return_value=versions)
	mocker.patch('shulkr.get_latest_generated_version')
	mocker.patch('shulkr.create_version')


def test_main_uncaught_loads_version_manifest(mock_all):
	shulkr.main_uncaught()

	shulkr.load_manifest.assert_called_once_with()


def test_main_uncaught_calls_parse_args(mock_all, mocker):
	mocker.patch('shulkr.sys.argv', ['shulkr', '--repo', 'path/to/repo'])

	shulkr.main_uncaught()

	shulkr.parse_args.assert_called_once_with(['--repo', 'path/to/repo'])


def test_main_uncaught_calls_init_repo(mocker, mock_all):
	shulkr.os.path.join.return_value = 'full/path/to/repo'

	shulkr.main_uncaught()

	shulkr.init_repo.assert_called_once_with('full/path/to/repo')


def test_main_uncaught_with_unsupported_repo_exits_with_error(mock_all):
	shulkr.is_compatible.return_value = False

	shulkr.main_uncaught()

	shulkr.sys.exit.assert_called_once_with(4)


def test_main_uncaught_calls_init_config(mock_all):
	shulkr.parse_args.return_value = MagicMock(
		mappings='mappings',
		message='message',
		tag=True,
		undo_renamed_vars=True
	)
	shulkr.os.path.join.return_value = 'full/path/to/repo'

	shulkr.main_uncaught()

	shulkr.init_config.assert_called_once_with(
		'full/path/to/repo',
		'mappings',
		'message',
		True,
		True
	)


def test_main_uncaught_calls_ensure_gitignore_exists(mock_all):
	shulkr.main_uncaught()

	shulkr.ensure_gitignore_exists.assert_called_once_with()


def test_main_uncaught_with_multiple_versions_calls_create_version_for_each_version(mocker, mock_all, versions):
	shulkr.main_uncaught()

	shulkr.create_version.assert_has_calls([
		mocker.call(version) for version in versions
	])


def test_main_uncaught_without_any_versions_exits_with_error(mock_all):
	shulkr.Version.patterns.return_value = []

	shulkr.main_uncaught()

	shulkr.sys.exit.assert_called_once_with(3)
