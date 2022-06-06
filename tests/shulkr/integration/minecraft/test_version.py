from mint.repo import Repo
from minecraft.version import Version

from shulkr.version import get_latest_generated_version


def test_get_latest_generated_version_with_repo_with_two_versions_returns_newer_version(repo: Repo):
	# Add two tagged commits (Minecraft versions)
	repo.git.commit(message='1.17', allow_empty=True)
	repo.git.tag('1.17')

	repo.git.commit(message='1.18', allow_empty=True)
	repo.git.tag('1.18')

	# The latest generated version from HEAD should be 1.18
	assert get_latest_generated_version() == Version.of('1.18')


def test_get_latest_generated_version_with_repo_with_two_versions_after_checking_out_older_version_returns_newer_version(repo: Repo):
	# Add two tagged commits (Minecraft versions)
	repo.git.commit(message='1.17', allow_empty=True)
	repo.git.tag('1.17')

	repo.git.commit(message='1.18', allow_empty=True)
	repo.git.tag('1.18')

	# Get the name of the current (only) branch
	orig_branch = repo.git.rev_parse('HEAD', abbrev_ref=True)

	# Now, check out 1.17 (this used to cause get_latest_generated_version to
	# return 1.17 instead of 1.18)
	repo.git.checkout('1.17')

	# Return to 1.18, without checking it out directly (important)
	repo.git.checkout(orig_branch)

	# The latest generated version from HEAD should be 1.18
	assert get_latest_generated_version() == Version.of('1.18')
