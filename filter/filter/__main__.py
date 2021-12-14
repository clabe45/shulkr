import argparse
import sys
from typing import List

from git import Repo

from filter.filter import filter_patch
from filter.git import diff_commits


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='filter', description='Generate a filtered diff of Minecraft source code, keeping only semantic changes')
	parser.add_argument('repo_path', type=str, help='Path to the Minecraft git repo')
	parser.add_argument('commit1', type=str, help='First (earlier) commit to diff')
	parser.add_argument('commit2', type=str, help='Second (later) commit to diff')
	parser.add_argument('paths', type=str, nargs='*')

	return parser.parse_args()


def get_filtered_diff(repo_path: str, commit1: str, commit2: str, paths: List[str] = []) -> str:
	repo = Repo(repo_path)
	diff_index, patch = diff_commits(repo, commit1, commit2, paths)
	patch = filter_patch(
		patch,
		sys.stdout,
		diff_index,
		repo.commit(commit1),
		repo.commit(commit2)
	)

	return str(patch)


def main() -> None:
	args = parse_args()

	diff = get_filtered_diff(args.repo_path, args.commit1, args.commit2, args.paths)
	print(diff)

if __name__ == '__main__':
	main()
