# Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## Project Implementation

At a high-level, shulkr does the following for each version of Minecraft
resolved from the supplied version patterns:
1. Generate the source code using [DecompilerMC] or [yarn]
2. Commit the version to git
3. Optionally, tag the version
## Testing

Please make sure to update tests as appropriate:
- **Unit tests** should mock all dependencies and test the code in isolation.
- **Smoke tests** should test the most important functional requirements in a
  real environment. They should not mock any dependencies and should be as fast
  as possible.
- **Functional tests** should test all functional requirements in a real
  environment. They should not mock any dependencies.

## Commit Message Guidelines

> Adopted from [Angular's commit message guidelines]

We have very precise rules over how our git commit messages can be formatted.
This leads to **more readable messages** that are easy to follow when looking
through the **project history**.

### Commit Message Format

Each commit message consists of a **header**, a **body** and a **footer**. The
header has a special format that includes a **type**, a **scope** and a
**subject**:

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The **header** is mandatory and the **scope** of the header is optional.

Any line of the commit message cannot be longer 100 characters! This allows the
message to be easier to read on GitHub as well as in various git tools.

The footer should contain a [closing reference to an issue] and describe any
breaking changes.

Samples: (even more [samples])

```
fix(shulkr): add except case to main() try-except block

This way, `ValueError`s thrown by any other function in main()
(technically main_uncaught) will be printed gracefully.
```
```
docs(*): update overview in contributing guide
```

### Breaking Changes

Breaking changes can be indicated by adding a `!` between the type and the
scope, or by adding a footer with the `BREAKING CHANGE:` prefix (see *Footer*).
Example:

```
feat!(shulkr): gracefully quit when no versions are resolved

For compatability with Windows, the command must be supplied as a list
of tokens, and it cannot be run in a shell.

Fixes #18
```

### Revert

If the commit reverts a previous commit, it should begin with `revert: `,
followed by the header of the reverted commit. In the body it should say: `This
reverts commit <hash>.`, where the hash is the SHA of the commit being reverted.

### Type

Must be one of the following:

* **build**: Changes that affect the build system or external dependencies
* **ci**: Changes to our CI configuration files and scripts
* **docs**: Documentation only changes
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **style**: Changes that do not affect the meaning of the code (white-space,
  formatting, missing semi-colons, etc)
* **test**: Adding missing tests or correcting existing tests

### Scope

The scope should be the name of the Python package affected.

The following is the list of supported scopes:

* [**java**](../java)
* [**minecraft**](../minecraft)
* [**mint**](../mint)
* [**shulkr**](../shulkr)

If the change does not belong to a single package, you can use `*` instead.

### Subject

The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

### Body

Just as in the **subject**, use the imperative, present tense: "change" not
"changed" nor "changes". The body should include the motivation for the change
and contrast this with previous behavior.

### Footer

The footer should contain any information about **Breaking Changes** and is also
the place to reference GitHub issues that this commit **Closes**.

**Breaking Changes** placed in the footer should start with the word `BREAKING
*CHANGE:` with a space or two newlines. The rest of the commit message is then
*used for this.

[DecompilerMC]: https://github.com/hube12/DecompilerMC
[yarn]: https://github.com/FabricMC/yarn
[Angular's commit message guidelines]: https://github.com/angular/angular/blob/main/CONTRIBUTING.md
[closing reference to an issue]: https://help.github.com/articles/closing-issues-via-commit-messages
[samples]: https://github.com/clabe45/shulkr/commits/main
