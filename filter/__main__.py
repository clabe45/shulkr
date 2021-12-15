import os

from git import Repo

from filter import parse_args, create_version


def main() -> None:
	args = parse_args()

	repo_path = os.path.join(
		os.getcwd(),
		args.repo
	)

	if not os.path.exists(repo_path):
		print('Creating a new Minecraft repo')
		os.mkdir(repo_path)

	try:
		repo = Repo(repo_path)
	except InvalidGitRepositoryError:
		repo = Repo.init(repo_path)

	for minecraft_version in args.version:
		create_version(repo, minecraft_version, args.undo_renamed_vars)


if __name__ == '__main__':
	main()
