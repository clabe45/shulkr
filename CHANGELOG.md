# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- `..X` now starts with the next release (not including snapshots).
- `..X` and `...X` raising an exception if the repo is up-to-date.

## [0.4.1] - 2022-04-13
### Fixed
- Next version not being detected correctly.
- `NoSuchPathError` when creating a repo without a mapping specified.
- `GitCommandError` when using a brand-new repo without a mapping specified.

## [0.4.0] - 2022-04-12
### Added
- Support for [Yarn](https://github.com/FabricMC/yarn) mappings.
- Can now be invoked in different repos at the same time.

### Changed
- Omitting the first version in a range pattern defaults to the version after the latest commit.

## [0.3.3] - 2021-01-03
### Fixed
- Deleted files not being committed
- `--undo-renamed-vars` causing error in commit step

## [0.3.2] - 2021-12-31
### Fixed
- Not all files being added to commits
- `File exists` error when decompiling the second version
- `--undo-renamed-vars` causing error

## [0.3.1] - 2021-12-30
### Changed
- `client` and `server` are no longer deleted before each version
- Reword some argument descriptions in the help page

## [0.3.0] - 2021-12-30
### Added
- Each commit is now tagged with its Minecraft version

### Changed
- Restructure source roots for easier project organization in IDEs
  - `src/client` &rarr; `client/src`
  - `src/server` &rarr; `server/src`

### Fixed
- Issue with commit message substition

## [0.2.0] - 2021-12-16
### Added
- Negative version patterns

## [0.1.1] - 2021-12-16
### Fixed
- `No such file or directory: main.py` error

## [0.1.0] - 2021-12-16
### Added
- Decompilation with [DecompilerMC]
- Git integration
  - Each version committed to local repo
- Range operators (`..` and `...`)

[Unreleased]: https://github.com/clabe45/shulkr/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/clabe45/shulkr/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/clabe45/shulkr/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/clabe45/shulkr/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/clabe45/shulkr/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/clabe45/shulkr/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/clabe45/shulkr/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/clabe45/shulkr/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/clabe45/shulkr/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/clabe45/shulkr/releases/tag/v0.1.0

[DecompilerMC]: https://github.com/hube12/DecompilerMC
