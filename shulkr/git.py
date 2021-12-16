from __future__ import annotations
import os.path
import sys
from typing import Dict, List, Optional, Tuple, Union

from git import Commit, Diff, DiffIndex, Repo

from shulkr.java import get_renamed_variables


def get_blob(commit: Optional[Commit], path: str, repo_path: str) -> bytes:
	if commit is None:
		p = os.path.join(repo_path, path)
		with open(p, 'r') as f:
			return f.read()

	parts = path.split('/')
	curr = commit.tree

	while len(parts) > 0:
		name = parts.pop(0)
		curr = curr[name]

	return curr.data_stream.read().decode()
