# Shulkr

This tool decompiles multiple versions of Minecraft and commits each one to Git

## Requirements

- Git
- JDK (>= 17 for Minecraft 1.18)
- Gradle >= 7.3

## Installation

## Usage

```sh
shulkr 1.16 1.17 1.18
```

A commit with the decompiled source code will be generated for each specified
version of Minecraft:

```
40240b1 version 1.18
86dc440 version 1.17
5d13494 version 1.16
```

## Version Patterns

Ranges of versions can be specified with the `..` and `...` operators:
- `A..B` expands to all versions between `A` and `B` (inclusive), *not*
  including snapshots
- `A...B` expands to all versions between `A` and `B` (inclusive), including
  snapshots

`A` and/or `B` can be omitted, defaulting to the earliest and latest supported
versions, respectively.

## Options

### `--repo` / `-p`

By default the source code is generated in the current working directory. To
specify a different location:

```sh
shulkr--repo minecraft-sources MINECRAFT_VERSION
```

If the directory does not exist, a new git repo will be created there.

### `--message` / `-m`

This option lets you customize the commit message format:

```sh
shulkr -m "Minecraft {}" 1.18-rc4
```
