import os

import click

from shulkr.repo import get_repo


def _gitignore_path() -> str:
    repo = get_repo()

    return os.path.join(repo.path, ".gitignore")


def _create_gitignore() -> None:
    click.echo("Creating gitignore")

    repo = get_repo()

    with open(_gitignore_path(), "w+") as gitignore:
        to_ignore = ["yarn", "DecompilerMC"]
        gitignore.write("\n".join(to_ignore) + "\n")

    repo.git.add(".gitignore")
    repo.git.commit(message="add .gitignore")


def ensure_gitignore_exists() -> bool:
    """
    Create and commit a .gitignore file if one does not exist

    Returns:
            bool: True if a .gitignore file was found. False if one was created.
    """

    if not os.path.isfile(_gitignore_path()):
        _create_gitignore()
        return False

    else:
        return True
