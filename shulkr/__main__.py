import os
import sys

from git import InvalidGitRepositoryError, Repo

from shulkr import parse_args, create_version
from shulkr.minecraft.version import NoSuchVersionError, Version, load_manifest


def main_uncaught() -> None:
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
		print(f'Creating {repo_path}')
		os.mkdir(repo_path)

	try:
		repo = Repo(repo_path)
	except InvalidGitRepositoryError:
		print('Initializing git')
		repo = Repo.init(repo_path)

	for version_id in versions:
		create_version(
			repo,
			version_id,
			args.undo_renamed_vars,
			args.message
		)


def main() -> None:
	try:
		main_uncaught()
	except KeyboardInterrupt:
		print('Aborted!', file=sys.stderr)


if __name__ == '__main__':
	main()
