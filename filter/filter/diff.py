from __future__ import annotations
from typing import List, Tuple, Union

from git import Diff, DiffIndex, Repo
from unidiff import Hunk, PatchedFile, PatchSet


def diff_commits(repo_path: str, commit1: str, commit2: str) -> str:
	repo = Repo(repo_path)
	return repo.git.diff(commit1, commit2, color='never')


def include_hunk(hunk: Hunk) -> bool:
	return True


def filter_patch(patch: str) -> str:
	patch_set = PatchSet(patch)

	for i in range(len(patch_set) - 1, -1, -1):
		patched_file = patch_set[i]

		for j in range(len(patched_file) - 1, -1, -1):
			hunk = patched_file[j]
			if not include_hunk(hunk):
				patched_file.pop(j)

		if len(patched_file) == 0:
			patch_set.pop(i)

	return str(patch_set)
