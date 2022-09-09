import os
from typing import Optional

import git


def get_blob(repo: git.Repo, commit: Optional[git.Commit], path: str) -> bytes:
	if commit is None:
		p = os.path.join(repo.working_tree_dir, path)
		with open(p, 'r') as f:
			return f.read()

	parts = path.split('/')
	curr = commit.tree

	while len(parts) > 0:
		name = parts.pop(0)
		curr = curr[name]

	return curr.data_stream.read().decode()
