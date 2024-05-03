import sys
from typing import List

import click

from shulkr.app import run


@click.command(
    name="shulkr", help="Generate multiple versions of the Minecraft source code"
)
@click.help_option("-h", "--help", is_flag=True, help="Show this message and exit")
@click.option(
    "--mappings",
    "-p",
    type=click.Choice(["yarn", "mojang"]),
    default="yarn",
    help="Mappings for deobfuscation (defaults to 'yarn')",
)
@click.option(
    "--repo",
    "-p",
    type=click.Path(),
    default=".",
    help="Path to the Minecraft repo (defaults to the current working directory)",
)
@click.option(
    "--message",
    "-m",
    type=str,
    default="version {}",
    help="Commit message template (defaults to 'version {}')",
)
@click.option("--no-tags", "-T", is_flag=True, help="Do not tag commits")
@click.option(
    "--undo-renamed-vars",
    "-u",
    is_flag=True,
    help=(
        "Revert local variables that were renamed in new versions to their "
        "original names (experimental)"
    ),
)
@click.argument("versions", nargs=-1, type=click.STRING)
def cli(
    versions: List[str],
    mappings: str,
    repo: str,
    message: str,
    no_tags: bool,
    undo_renamed_vars: bool,
) -> None:

    tags = not no_tags
    try:
        run(versions, mappings, repo, message, tags, undo_renamed_vars)

    except ValueError as e:
        click.secho(e, err=True, fg="red")
        sys.exit(2)

    except KeyboardInterrupt:
        click.echo("Aborted!", err=True)
