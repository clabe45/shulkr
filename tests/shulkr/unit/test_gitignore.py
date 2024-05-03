import os

from shulkr.gitignore import ensure_gitignore_exists


def test_ensure_gitignore_exists_opens_gitignore_for_writing_if_it_does_not_exist(
    mocker, empty_repo
):
    mocker.patch("shulkr.gitignore.click")
    mocker.patch("shulkr.gitignore.os.path.isfile", return_value=False)
    open_ = mocker.patch("shulkr.gitignore.open")

    ensure_gitignore_exists()

    gitignore_path = os.path.join(empty_repo.path, ".gitignore")
    open_.assert_called_once_with(gitignore_path, "w+")


def test_ensure_gitignore_exists_does_not_open_gitignore_if_it_does_exist(
    mocker, empty_repo
):
    mocker.patch("shulkr.gitignore.click")
    mocker.patch("shulkr.gitignore.os.path.isfile", return_value=True)
    open_ = mocker.patch("shulkr.gitignore.open")

    ensure_gitignore_exists()

    open_.assert_not_called()


def test_ensure_gitignore_exists_returns_false_if_it_does_not_exist(mocker, empty_repo):
    mocker.patch("shulkr.gitignore.click")
    mocker.patch("shulkr.gitignore.os.path.isfile", return_value=False)
    mocker.patch("shulkr.gitignore.open")

    assert not ensure_gitignore_exists()


def test_ensure_gitignore_exists_returns_true_if_it_does_exist(mocker, empty_repo):
    mocker.patch("shulkr.gitignore.click")
    mocker.patch("shulkr.gitignore.os.path.isfile", return_value=True)
    mocker.patch("shulkr.gitignore.open")

    assert ensure_gitignore_exists()
