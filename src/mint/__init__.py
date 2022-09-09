"""
Internal git wrapper for Python

The goal of Mint is to provide a Pythonic interface to run git commands. We
were previously using gitpython, but we are now migrating to Mint because
gitpython's use of git's plumbing commands can lead to unexpected results. To
ease the migration process, Mint's API was designed to be very similar to that
of gitpython.
"""
