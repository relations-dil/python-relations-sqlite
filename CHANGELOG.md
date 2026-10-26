# Changelog

All notable changes to python-relations-sqlite are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

### Changed
- `make new` works on the ticket branch you're on: it writes VERSION and the changelog section there and commits, makes no branch of its own, and refuses on main, since we branch from the ticket. `B=` and `BRANCH_PREFIX` are gone (relations-dil/python-relations#98).

## [0.6.5] - 2026-10-26

### Added
- Requires relations-sql 0.6.11 (`requirements.txt` and `setup.py`), so a change to only a field's `length` reaches the table rebuild (relations-dil/python-relations-sql#30).
- Jenkins releases on a merge to `main`: a `release` stage (only on `main`) runs `make release`, which does nothing for a version that is already released and otherwise does the test release, the release and the tag. It pushes the tag with the `github` credential, as Leroy Jenkins, one build at a time, with a two hour timeout (relations-dil/python-relations#80). The package builds run in a copy with only the files they use mounted read-only, so nothing root-owned is left in the workspace, and `make tag` stops on a failure instead of ignoring it. The release scripts work with the older git on the Jenkins host.
- `make help` lists every target with what it does (each target has a `## description` after it), and is what a bare `make` runs.
- Release tooling, the same as relations-dil's (relations-dil/python-relations#77): `make new` starts a release, `make version` sets the version, `make release-check` says where a release is up to and what would stop it, `make release` does what's left (checks, TestPyPI and a clean install from it, PyPI, the tag), `make dist-check` builds and checks the distributions, and `make test-release` tests the scripts against a throwaway repo and fake indexes. The work is in `scripts/`.
- A `VERSION` file as the one place the version is set: the `Makefile` reads it and mounts it, `testpypi` and `pypi` pass it as `BUILD_VERSION`, and `setup.py` reads `BUILD_VERSION` or the file.
- A string column whose field has a `length` gets `CHECK (length(column) <= length)`, as SQLite doesn't enforce the length of a type, so a `length` means the same here as it does in MySQL and PostgreSQL. Without a length, and for extracted columns, there is no check (relations-dil/python-relations-sqlite#15).

### Changed
- `make release-check` and `make release` don't run `build`, `test`, `lint` and `setup` again: the Jenkins stages have just run them before the release stage, so it was the same work twice. Run them yourself before checking by hand, as `make release-check` is only the checks and `dist-check` now (relations-dil/python-relations#90).
- Every `docker run` in the `Makefile` uses `--rm`, and a replaced database container is removed with its volume (`docker rm --force -v`), so builds and test runs leave no stopped containers or volumes behind.
- `testpypi` and `pypi` run in the current `python` image with `build` and `twine` installed on the fly, so the custom `gaf3/pypi` image is no longer used.

## [0.6.4] - 2026-10-14

### Changed
- `TABLE.PRIMARY` is `PRIMARY KEY (%s)`, so an id that isn't `auto` (a string id from relations-dil 0.6.18) gets a table-level primary key. `PRIMARY_AUTO` is `False`, so an `auto` id still gets none, its column is `INTEGER PRIMARY KEY`.
- `TABLE.modify` carries the `id` into the rebuilt table, so a string id keeps its primary key when the table is rebuilt for another change.
- A rebuilt table for an int id that isn't `auto` now gets a table-level primary key as well.

## [0.6.3] - 2026-06-06

- Table migrations now skip fields with no store (a false `store`) when copying columns to the new table.
- Bumped the `relations-sql` requirement to 0.6.8 and `relations-dil` to 0.6.14, and installed git in the Dockerfile.

## [0.6.2] - 2022-11-25

- Switched to the PyPI `relations-sql` release (0.6.7) and required `relations-dil` 0.6.12 in the requirements file.
- Renamed the distribution to `relations-sqlite`.

## [0.6.1] - 2022-08-06

- Prepared the package for PyPI with a `LICENSE.txt`, a `PYPI.md` description, and `testpypi` and `pypi` Makefile targets.
- Removed the git-based installs from the Dockerfile and setup step.

## [0.6.0] - 2022-03-14

- Fixed table migrations: the `TABLE.name` method now handles separate migration and definition names and schemas and takes a `rename` flag, so renaming a table to its `_old_` copy no longer reuses the schema.
- The row copy during a migration now lists its columns explicitly (sorted by name), and dependencies moved to `python-relations` 0.6.9 and `relations-sql` 0.6.5.

## [0.5.0] - 2022-03-13

- Updated the `python-relations` requirement to 0.6.8 and `relations-sql` to 0.6.4, adding support for familial access.

## [0.4.0] - 2022-02-18

- Updated the `python-relations` requirement to 0.6.7 and `relations-sql` to 0.6.3, which changed labels to titles.

## [0.3.0] - 2021-11-21

- Renamed the package to `python-relations-sqlite` and moved its dependencies to the relations-dil organization (`python-relations` 0.6.6, `relations-sql` 0.6.2).

## [0.2.0] - 2021-11-13

- Updated the `python-relations` requirement to 0.6.5 and `relations-sql` to 0.6.1 after the library renames.

## [0.1.0] - 2021-11-12

- Initial release of the SQLite dialect for `relations-sql`, providing SQLite versions of the expression, criterion, criteria, clause and query classes.
- Added SQLite DDL classes for `COLUMN`, `INDEX` and `TABLE`, with `INTEGER PRIMARY KEY` for auto ids, generated (`AS (...)`) columns for extracted values, and table migrations done by renaming the old table to an `_old_` copy and copying rows across.
- Included Dockerfile, Jenkinsfile and Makefile.
