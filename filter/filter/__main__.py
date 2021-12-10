import argparse

from filter.diff import diff_commits, filter_patch


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='filter', description='Generate a filtered diff of Minecraft source code, keeping only semantic changes')
	parser.add_argument('repo_path', type=str, help='Path to the Minecraft git repo')
	parser.add_argument('commit1', type=str, help='First (earlier) commit to diff')
	parser.add_argument('commit2', type=str, help='Second (later) commit to diff')

	return parser.parse_args()


def main() -> None:
	args = parse_args()

	patch = diff_commits(args.repo_path, args.commit1, args.commit2)
	patch = filter_patch(patch)
	print(patch)


if __name__ == '__main__':
	main()
