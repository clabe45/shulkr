import os
import sys

from shulkr import create_version
from shulkr.config import get_config
from shulkr.arguments import parse_args
from shulkr.minecraft.version import NoSuchVersionError, Version, load_manifest


def main_uncaught() -> None:
	load_manifest()

	args = parse_args(sys.argv[1:])

	config = get_config()

	config.repo_path = os.path.join(
		os.getcwd(),
		args.repo
	)

	try:
		versions = Version.patterns(args.version)
	except NoSuchVersionError as e:
		print(e, file=sys.stderr)
		sys.exit(1)
	except ValueError as e:
		print(e, file=sys.stderr)
		sys.exit(2)

	if len(versions) == 0:
		print('No versions selected', file=sys.stderr)
		sys.exit(3)

	if not os.path.exists(config.repo_path):
		print(f'Creating {config.repo_path}')
		os.mkdir(config.repo_path)

	for version_id in versions:
		create_version(
			version_id,
			args.undo_renamed_vars,
			args.message,
			args.tag
		)


def main() -> None:
	try:
		main_uncaught()
	except KeyboardInterrupt:
		print('Aborted!', file=sys.stderr)


if __name__ == '__main__':
	main()
