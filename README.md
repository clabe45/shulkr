# Shulkr

Shulkr is a tool that decompiles multiple versions of Minecraft and commits each
version to Git

## Requirements

- Git
- JDK (>= 17 for Minecraft 1.18)
- Gradle >= 7.3

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

Note: It's okay to skip versions. Shulkr generates the source code for each
version and then commits it to git, so you can include as many or as little
intermediate versions as you would like.

## Version Patterns

Ranges of versions can be specified with `..` and `...`:
- `A..B` expands to all versions between `A` and `B` (inclusive), *not*
  including snapshots
- `A...B` expands to all versions between `A` and `B` (inclusive), including
  snapshots

`A` and/or `B` can be omitted, defaulting to the earliest and latest supported
versions, respectively.

Versions can be excluded by adding a *negativie pattern* after it. To negate a
pattern, add `-`. The following pattern expands to all versions after `A`, up to
and including `B`:
- `A...B -A`

## Options

### `--repo` / `-p`

By default the source code is generated in the current working directory. To
specify a different location:

```sh
shulkr --repo minecraft-sources MINECRAFT_VERSION
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
