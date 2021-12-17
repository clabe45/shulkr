from __future__ import annotations
import os.path
from typing import Optional

from git import Commit


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
