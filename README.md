# Shulkr

![Check New Commits](https://github.com/clabe45/shulkr/actions/workflows/check.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/shulkr.svg)](https://badge.fury.io/py/shulkr)

Shulkr is a tool that decompiles multiple versions of Minecraft and commits each
version to Git

*Version 0.3 altered the directory structure of the generated sources. It is
recommended to regenerate all commits after upgrading. See the [changelog] for
more info.*

## Requirements

- Git
- JDK (>= 17 for Minecraft 1.18 and above)
- Gradle (>= 7.3 for Minecraft 1.18 and above)

## Installation

```
pip install shulkr
```

## Usage

```sh
shulkr 1.16 1.17 1.18
```

This will generate a commit with the decompiled source code for Minecraft 1.16,
1.17 and 1.18 in the current working directory:

```
204b37c (HEAD -> main, tag: 1.18) version 1.18
86dc440 (tag: 1.17) version 1.17
5d13494 (tag: 1.16) version 1.16
```

Note: It's okay to skip versions. Shulkr generates the complete source code for
each version before committing to git, so you can include as many or as little
intermediate versions as you would like.

## Version Patterns

Ranges of versions can be specified with `..` and `...`:
- `A..B` expands to all versions between `A` and `B` (inclusive), *not*
  including snapshots
- `A...B` expands to all versions between `A` and `B` (inclusive), including
  snapshots

`A` and/or `B` can be omitted, defaulting to the earliest and latest supported
versions, respectively.

A *negative pattern* removes all matching versions that came before it. To
negate a pattern, add `-`. The following pattern expands to all versions after
`A`, up to and including `B` (the order is important):
- `A...B -A`

## Options

### `--repo` / `-p`

By default the source code is generated in the current working directory. To
specify a different location:

```sh
shulkr --repo minecraft-sources 1.17..
```

If the directory does not exist, a new git repo will be created there.

### `--message` / `-m`

This option lets you customize the commit message format:

```sh
shulkr -m "Minecraft {}" 1.18-rc4
```

### `--no-tags` / `-T`

By default, each commit is tagged with the name of its Minecraft version. This
can be disabled with `--no-tags`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Licensed under the Apache License, Version 2.0.

[Fork]: https://github.com/clabe45/shulkr/fork
[changelog]: https://github.com/clabe45/shulkr/blob/main/CHANGELOG.md
