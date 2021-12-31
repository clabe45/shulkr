# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[Unreleased]: https://github.com/clabe45/shulkr/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/clabe45/shulkr/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/clabe45/shulkr/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/clabe45/shulkr/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/clabe45/shulkr/releases/tag/v0.1.0

[DecompilerMC]: https://github.com/hube12/DecompilerMC
