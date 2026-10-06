# Changelog

All notable changes to python-relations-sqlite are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

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
