from mint.command import GitCommand
import pytest


@pytest.fixture
def git(repo):
	return GitCommand(repo.path)


class TestCommand:
	def test_getattr_returns_git_output(self, git):
		# Make one commit so git knows which branch is checked out
		git.commit(message='dummy commit', allow_empty=True)

		# Now, make sure the result of 'git status' is correct
		branch = git.rev_parse('HEAD', abbrev_ref=True)
		assert git.status() == f'On branch {branch}\nnothing to commit, working tree clean'
