import argparse
import os.path
import sys
from typing import List

from git import Repo

from filter.git import get_blob
from filter.java import JavaAnalyzationError, get_renamed_variables, undo_variable_renames

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='filter', description='Generate a filtered diff of Minecraft source code, keeping only semantic changes')
	parser.add_argument('repo_path', type=str, help='Path to the Minecraft git repo')

	return parser.parse_args()


def undo_renames(repo_path: str) -> None:
	repo = Repo(repo_path)
	try:
		next(repo.iter_commits('HEAD'))
	except StopIteration:
		raise Exception('No commits on current branch')

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


def main() -> None:
	args = parse_args()

	diff = undo_renames(args.repo_path)

if __name__ == '__main__':
	main()
