# Mint (Git)

> internal git wrapper

The goal of Mint is to provide a Pythonic interface to run git commands. We
were previously using gitpython, but we are now migrating to Mint because
gitpython's use of git's plumbing commands can lead to unexpected results. To
ease the migration process, Mint's API was designed to be very similar to that
of gitpython.

## Usage

Preparing the repo:
```python
# Use an existing repo
repo = Repo(PATH)

# Create an empty repo
repo = Repo.init(PATH)

# Clone a repo
repo = Repo.clone(REMOTE_URL, DESTINATION)
```

Using the repo:
```python
repo.git.commit('src', message='Some commit')  # or m='Some commit'
```

## Known Issues

- Quotes in `--key=value` style Git arguments are treated literally. At least on
  Linux, Git seems to ignore quotes some of the time (more investigation needed).
