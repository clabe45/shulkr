import os

from git import Repo

from filter import parse_args, create_version


def main() -> None:
	args = parse_args()

	if not os.path.exists(args.repo):
		print('Creating a new Minecraft repo')
		os.mkdir(args.repo)

	try:
		repo = Repo(args.repo)
	except InvalidGitRepositoryError:
		repo = Repo.init(args.repo)

	for minecraft_version in args.version:
		create_version(repo, minecraft_version, args.undo_renamed_vars)


if __name__ == '__main__':
	main()
