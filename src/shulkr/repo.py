from __future__ import annotations

import click

from mint.repo import NoSuchRepoError, Repo


def init_repo(repo_path: str) -> bool:
    """
    Load information about the current shulkr/git repo

    Must be called before get_repo()

    Args:
            repo_path (str): Path to the working tree of the repo

    Returns:
            bool: True if a repo was found, False if a new repo was created
            loaded.
    """

    global repo

    try:
        repo = Repo(repo_path)

        # The repo already exists
        return True

    except FileNotFoundError:
        click.echo("Initializing git")
        repo = Repo.init(repo_path)

    except NotADirectoryError:
        click.echo("Initializing git")
        repo = Repo.init(repo_path)

    except NoSuchRepoError:
        click.echo("Initializing git")
        repo = Repo.init(repo_path)

    # We created the repo
    return False


def get_repo() -> Repo:
    return repo


repo = None
