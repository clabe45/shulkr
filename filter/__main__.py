import os
import sys

from git import Repo

from filter import parse_args, create_version
from filter.minecraft.version import NoSuchVersionError, Version, load_manifest


def main() -> None:
	load_manifest()

	args = parse_args()

	repo_path = os.path.join(
		os.getcwd(),
		args.repo
	)

	try:
		ranges = [Version.pattern(p) for p in args.version]
		versions = [version for range in ranges for version in range]
		versions.sort()
	except NoSuchVersionError as e:
		print(e, file=sys.stderr)
		sys.exit(1)

	if not os.path.exists(repo_path):
		print('Creating a new Minecraft repo')
		os.mkdir(repo_path)

	try:
		repo = Repo(repo_path)
	except InvalidGitRepositoryError:
		repo = Repo.init(repo_path)

	for version_id in versions:
		create_version(
			repo,
			version_id,
			args.undo_renamed_vars,
			args.message
		)


if __name__ == '__main__':
	main()
