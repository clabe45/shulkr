import os
import sys

from shulkr.arguments import parse_args
from shulkr.config import get_config, init_config
from shulkr.git import (
	commit_version,
	create_gitignore,
	head_has_versions,
	tag_version
)
from shulkr.java import undo_renames
from shulkr.minecraft.source import generate_sources
from shulkr.minecraft.version import (
	NoSuchVersionError,
	Version,
	load_manifest
)


def create_version(
	version: Version,
	mappings: str,
	undo_renamed_vars: bool,
	message_template: str,
	tag: bool
) -> None:

	# 1. Generate source code for the current version
	print(f'\nGenerating sources for Minecraft {version}')

	mappings = get_config().mappings
	generate_sources(version, mappings)

	# 2. If there are any previous versions, undo the renamed variables
	if undo_renamed_vars and head_has_versions():
		print('Undoing renamed variables')
		undo_renames()

	# 3. Commit the new version to git
	print('Committing to git')
	commit_version(version, undo_renamed_vars, message_template)

	# 4. Tag
	if tag:
		tag_version(version)


def main_uncaught() -> None:
	load_manifest()

	args = parse_args(sys.argv[1:])

	repo_path = os.path.join(
		os.getcwd(),
		args.repo
	)
	init_config(repo_path=repo_path, mappings=args.mappings)

	try:
		versions = Version.patterns(args.version)
	except NoSuchVersionError as e:
		print(e, file=sys.stderr)
		sys.exit(1)

	if len(versions) == 0:
		print('No versions selected', file=sys.stderr)
		sys.exit(3)

	gitignore = os.path.join(repo_path, '.gitignore')
	if not os.path.isfile(gitignore):
		create_gitignore()

	for version_id in versions:
		create_version(
			version_id,
			args.mappings,
			args.undo_renamed_vars,
			args.message,
			args.tag
		)


def main() -> None:
	try:
		main_uncaught()

	except ValueError as e:
		print(e, file=sys.stderr)
		sys.exit(2)

	except KeyboardInterrupt:
		print('Aborted!', file=sys.stderr)
