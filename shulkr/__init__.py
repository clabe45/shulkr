import os.path
import sys

from git import BadName, InvalidGitRepositoryError, Repo

from shulkr.git import get_blob
from shulkr.java import JavaAnalyzationError, get_renamed_variables, undo_variable_renames
from shulkr.minecraft.source import generate_sources
from shulkr.minecraft.version import Version


def undo_renames(repo: Repo) -> None:
	commit1 = repo.commit('HEAD')
	commit2 = None  # working tree
	diff_index = commit1.diff(commit2)

	# For each file changed (in reverse, with indices, so we can remove elements
	# in the for loop)
	for diff in diff_index:
		# Only process modified files (no new, deleted, ... files)
		if diff.change_type != 'M':
			continue

		# Only process Java files; leave everything else unchanged
		if not diff.a_path.endswith('.java'):
			continue

		source = get_blob(commit1, diff.a_path, repo_path)
		target = get_blob(commit2, diff.b_path, repo_path)

		try:
			renamed_variables = get_renamed_variables(source, target)
		except JavaAnalyzationError as e:
			raise Exception(f'{e} [{diff.a_path} -> {diff.b_path}]')

		if renamed_variables is not None:
			updated_target = undo_variable_renames(target, renamed_variables)
			with open(os.path.join(repo_path, diff.a_path), 'w') as f:
				f.write(updated_target)

			print(f'Updated {diff.a_path}')


def commit_version(repo: Repo, version: Version, undo_renamed_vars: bool, message_template: str) -> None:
	commit_msg = message_template.strip().format(str(version))
	if undo_renamed_vars and len(repo.iter_commits()) > 0:
		commit_msg += '\n\nRenamed variables reverted'

	repo.add('src')
	repo.index.commit(commit_msg)


def tag_version(repo: Repo, version: Version) -> None:
	repo.create_tag(str(version))


def create_version(repo: Repo, version: Version, undo_renamed_vars: bool, message_template: str, tag: bool) -> None:
	# 1. Generate source code for the current version
	print(f'Generating sources for Minecraft {version}')
	generate_sources(repo, version)

	# 2. If there are any previous versions, undo the renamed variables
	if undo_renamed_vars and len(repo.iter_commits()) > 0:
		print('Undoing renamed variables')
		undo_renames(repo)

	# 3. Commit the new version to git
	print('Committing to git')
	commit_version(repo, version, undo_renamed_vars, message_template)

	# 4. Tag
	if tag:
		tag_version(repo, version)
