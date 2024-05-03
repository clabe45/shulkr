from minecraft.version import Version
import pytest

from shulkr import app


@pytest.fixture
def versions():
    return [Version(id="1.18", index=0), Version(id="1.19", index=1)]


@pytest.fixture(autouse=True)
def mock_all(mocker, versions):
    mocker.patch("shulkr.app.click")
    mocker.patch("shulkr.app.load_manifest")
    mocker.patch("shulkr.app.os")
    mocker.patch("shulkr.app.init_repo")
    mocker.patch("shulkr.app.is_compatible")
    mocker.patch("shulkr.app.init_config")
    mocker.patch("shulkr.app.ensure_gitignore_exists")
    mocker.patch("shulkr.app.Version.patterns", return_value=versions)
    mocker.patch("shulkr.app.get_latest_generated_version")
    mocker.patch("shulkr.app.create_version")


def test_run_loads_version_manifest():
    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.load_manifest.assert_called_once_with()


def test_run_calls_init_repo(mocker):
    app.os.path.join.return_value = "full/path/to/repo"

    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.init_repo.assert_called_once_with("full/path/to/repo")


def test_run_with_unsupported_repo_exits_with_error():
    app.is_compatible.return_value = False

    with pytest.raises(SystemExit, match="4"):
        app.run(
            versions=[],
            mappings="mappings",
            repo_path="path/to/repo",
            message_template="message",
            tags=True,
            undo_renamed_vars=True,
        )


def test_run_calls_init_config_when_init_repo_returns_false():
    app.init_repo.return_value = False
    app.os.path.join.return_value = "full/path/to/repo"

    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.init_config.assert_called_once_with(
        "full/path/to/repo", "mappings", "message", True, True
    )


def test_run_calls_init_config_when_init_repo_returns_true():
    app.init_repo.return_value = True
    app.os.path.join.return_value = "full/path/to/repo"

    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.init_config.assert_called_once_with(
        "full/path/to/repo", "mappings", "message", True, True
    )


def test_run_calls_ensure_gitignore_exists():
    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.ensure_gitignore_exists.assert_called_once_with()


def test_run_with_version_older_than_latest_version_in_repo_exits_with_error():
    app.get_latest_generated_version.return_value = Version(id="1.18", index=1)

    with pytest.raises(SystemExit, match="3"):
        app.run(
            versions=[Version(id="1.17", index=0)],
            mappings="mappings",
            repo_path="path/to/repo",
            message_template="message",
            tags=True,
            undo_renamed_vars=True,
        )


def test_run_with_multiple_versions_calls_create_version_for_each_version(
    mocker, versions
):
    app.run(
        versions=[],
        mappings="mappings",
        repo_path="path/to/repo",
        message_template="message",
        tags=True,
        undo_renamed_vars=True,
    )

    app.create_version.assert_has_calls([mocker.call(version) for version in versions])


def test_run_without_any_versions_exits():
    app.Version.patterns.return_value = []

    with pytest.raises(SystemExit, match="0"):
        app.run(
            versions=[],
            mappings="mappings",
            repo_path="path/to/repo",
            message_template="message",
            tags=True,
            undo_renamed_vars=True,
        )
