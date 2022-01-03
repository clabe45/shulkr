import argparse
from typing import List


def parse_args(args: List[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		prog='shulkr',
		description='Generate multiple versions of the Minecraft source code'
	)

	parser.add_argument(
		'--repo',
		'-p',
		type=str,
		default='.',
		help='Path to the Minecraft repo (defaults to the current working directory)'
	)

	parser.add_argument(
		'--message',
		'-m',
		type=str,
		default='version {}',
		help="Commit message template (defaults to 'version {}')"
	)

	parser.add_argument(
		'--no-tags',
		'-T',
		dest='tag',
		action='store_false',
		help='Do not tag commits'
	)

	parser.add_argument(
		'--undo-renamed-vars',
		'-u',
		dest='undo_renamed_vars',
		action='store_true',
		help=(
			'Revert local variables that were renamed in new versions to their '
			'original names (experimental)'
		)
	)

	parser.add_argument(
		'version',
		nargs='+',
		type=str,
		help='List of versions to decompile'
	)

	parser.set_defaults(tag=True, undo_renamed_vars=False)

	return parser.parse_args(args)
