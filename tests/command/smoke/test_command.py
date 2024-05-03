class TestCommand:
    def test_getattr_returns_git_output(self, git, repo):
        # Make one commit so git knows which branch is checked out
        git.commit(message="dummy commit", allow_empty=True)

        # Now, make sure the result of 'git status' is correct
        branch = git.rev_parse("HEAD", abbrev_ref=True)
        assert (
            git.status() == f"On branch {branch}\nnothing to commit, working tree clean"
        )

    def test_commit_messages_with_spaces_are_not_wrapped_with_quotes(self, git, repo):
        git.commit(message="dummy commit", allow_empty=True)

        assert git.log("--format=%B") == "dummy commit"
