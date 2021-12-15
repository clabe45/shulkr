import argparse
import os.path
import sys

from git import BadName, InvalidGitRepositoryError, Repo

from filter.git import get_blob
from filter.java import JavaAnalyzationError, get_renamed_variables, undo_variable_renames
from filter.minecraft import generate_sources


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='filter', description='Generate a filtered diff of Minecraft source code, keeping only semantic changes')
	parser.add_argument('--repo', '-r', type=str, required=True, help='Path to the Minecraft repo')
	parser.add_argument('--undo-renamed-vars', '-u', dest='undo_renamed_vars', action='store_true', help='Revert local variables that were renamed in the new version')
	parser.add_argument('version', nargs='+', type=str, help='List of mapping versions')
	parser.set_defaults(undo_renamed_vars=False)

	return parser.parse_args()


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


def commit_version(repo: Repo, minecraft_version: str, undo_renamed_vars: bool) -> None:
	commit_msg = f'version {minecraft_version}'
	if undo_renamed_vars and len(repo.iter_commits()) > 0:
		commit_msg += '\n\nRenamed variables reverted'

	repo.git.add('src')
	repo.git.commit('-m', commit_msg)


def create_version(repo: Repo, version: str, undo_renamed_vars: bool) -> None:
	# 1. Generate source code for the current version
	print(f'Generating sources for Minecraft {version}')
	generate_sources(repo.working_tree_dir, version)

	# 2. If there are any previous versions, undo the renamed variables
	if undo_renamed_vars and len(repo.iter_commits()) > 0:
		print(f'Undoing renamed variables for Minecraft {version}')
		undo_renames(repo)

	# 3. Commit the new version to git
	print(f'Committing Minecraft {version} to git')
	commit_version(repo, version, undo_renamed_vars)
