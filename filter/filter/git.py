from __future__ import annotations
import os.path
import sys
from typing import Dict, List, Tuple, Union

from git import Commit, Diff, DiffIndex, Repo

from filter.java import get_renamed_variables


def diff_commits(repo: Repo, commit1: str, commit2: str, paths: List[str] = []) -> Tuple[str, DiffIndex]:
	return (
		repo.commit(commit1).diff(commit2, paths),
		repo.git.diff(commit1, commit2, paths, color='never')
	)


def get_blob(commit: Commit, path: str) -> bytes:
	parts = path.split('/')
	curr = commit.tree

	while len(parts) > 0:
		name = parts.pop(0)
		curr = curr[name]

	return curr.data_stream.read().decode()
