from shulkr.config import get_config

from shulkr.git import commit_version, head_has_versions, tag_version
from shulkr.java import undo_renames
from shulkr.minecraft.source import generate_sources
from shulkr.minecraft.version import Version


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
