import difflib
from typing import Dict, List, Tuple, Union

from git import Commit, DiffIndex
from unidiff import Hunk, PatchedFile, PatchSet

from filter.git import get_blob
from filter.java import JavaAnalyzationError, get_renamed_variables


def filter_hunk(diff: str, renamed_variables: Dict[str, str]) -> str:

	return diff


def filter_patch(patch: str, diff_index: DiffIndex, commit1: Commit, commit2: Commit) -> str:
	patch_set = PatchSet(patch)

	filtered_patches = []
	# For each file changed (in reverse, with indices, so we can remove elements
	# in the for loop)
	for i in range(len(patch_set) - 1, -1, -1):
		patched_file = patch_set[i]
		diff = diff_index[i]

		# Only process modified files (no new, deleted, ... files)
		if diff.change_type != 'M':
			continue

		# Only process Java files; leave everything else unchanged
		if not patched_file.source_file.endswith('.java'):
			filtered_patches.append(str(patched_file))
			continue

		source = get_blob(commit1, diff.a_path)
		target = get_blob(commit2, diff.b_path)

		try:
			renamed_variables = get_renamed_variables(source, target)
		except JavaAnalyzationError as e:
			raise Exception(f'{e} [{diff.a_path} -> {diff.b_path}]')

		# print(renamed_variables)
		if renamed_variables is not None:
			# For each hunk in this file diff
			for path, v in renamed_variables:
				for old, new in v:
					source = source.replace(old, new)

		filtered_patch_lines = difflib.unified_diff(source.split('\n'), target.split('\n'))
		filtered_patch = '\n'.join(filtered_patch_lines)
		if len(filtered_patch) == 0:
			# No semantic changes
			continue

		header = '\n'.join(str(patched_file).split('\n')[:5])
		filtered_patches.append(header + '\n' + filtered_patch)

	return ''.join(filtered_patches)

