import os
import sys
from typing import List

import click
from minecraft.version import (
	NoSuchVersionError,
	Version,
	load_manifest
)

from shulkr.compatibility import is_compatible
from shulkr.config import init_config
from shulkr.gitignore import ensure_gitignore_exists
from shulkr.repo import init_repo
from shulkr.version import create_version, get_latest_generated_version


def run(
	versions: List[str],
	mappings: str,
	repo_path: str,
	message_template: str,
	tags: bool,
	undo_renamed_vars: bool
) -> None:

	load_manifest()

	full_repo_path = os.path.join(
		os.getcwd(),
		repo_path
	)

	init_output = not init_repo(full_repo_path)

	if not is_compatible():
		click.secho(
			'This repo is not compatible with the current version of shulkr - ' +
			'please create a new repo or downgrade shulkr.',
			err=True,
			fg='yellow'
		)
		sys.exit(4)

	init_output = not init_config(
		full_repo_path,
		mappings,
		message_template,
		tags,
		undo_renamed_vars
	) or init_output
	init_output = not ensure_gitignore_exists() or init_output

	# If we printed anything in the initialization step, print a newline
	if init_output:
		click.echo()

	try:
		resolved_versions = Version.patterns(
			versions,
			latest_in_repo=get_latest_generated_version()
		)

	except NoSuchVersionError as e:
		click.secho(e, err=True, fg='red')
		sys.exit(1)

	if len(resolved_versions) == 0:
		click.secho('No versions selected', err=True, color='yellow')
		sys.exit(3)

	for version_id in resolved_versions:
		create_version(version_id)
