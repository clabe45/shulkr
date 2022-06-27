import os
import sys

from minecraft.version import (
	NoSuchVersionError,
	Version,
	load_manifest
)

from shulkr.arguments import parse_args
from shulkr.compatibility import is_compatible
from shulkr.config import init_config
from shulkr.gitignore import ensure_gitignore_exists
from shulkr.repo import init_repo
from shulkr.version import create_version, get_latest_generated_version


def main_uncaught() -> None:
	load_manifest()

	args = parse_args(sys.argv[1:])

	repo_path = os.path.join(
		os.getcwd(),
		args.repo
	)

	init_repo(repo_path)

	if not is_compatible():
		print(
			'This repo is not compatible with the current version of shulkr - ' +
			'please create a new repo or downgrade shulkr.',
			file=sys.stderr
		)
		sys.exit(4)

	init_config(
		repo_path,
		args.mappings,
		args.message,
		args.tag,
		args.undo_renamed_vars
	)
	ensure_gitignore_exists()

	try:
		versions = Version.patterns(
			args.version,
			latest_in_repo=get_latest_generated_version()
		)

	except NoSuchVersionError as e:
		print(e, file=sys.stderr)
		sys.exit(1)

	if len(versions) == 0:
		print('No versions selected', file=sys.stderr)
		sys.exit(3)

	for version_id in versions:
		create_version(version_id)


def main() -> None:
	try:
		main_uncaught()

	except ValueError as e:
		print(e, file=sys.stderr)
		sys.exit(2)

	except KeyboardInterrupt:
		print('Aborted!', file=sys.stderr)
