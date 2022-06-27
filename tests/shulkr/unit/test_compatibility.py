import pytest

import shulkr
from shulkr.compatibility import is_compatible


@pytest.fixture(autouse=True)
def mock_all(mocker):
	mocker.patch('shulkr.compatibility.config_exists')


def test_is_compatible_with_no_config_and_empty_repo_returns_true(empty_repo):
	shulkr.compatibility.config_exists.return_value = False
	assert is_compatible()


def test_is_compatible_with_no_config_and_nonempty_repo_returns_false(nonempty_repo):
	shulkr.compatibility.config_exists.return_value = False
	assert not is_compatible()


def test_is_compatible_with_config_and_nonempty_repo_returns_true(nonempty_repo):
	shulkr.compatibility.config_exists.return_value = True
	assert is_compatible()
