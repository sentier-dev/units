# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [BSD license][License] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code][Source Code]
- [Documentation][Documentation]
- [Issue Tracker][Issue Tracker]
- [Code of Conduct][Code of Conduct]

[License]: https://opensource.org/licenses/BSD-3-Clause
[Source Code]: https://github.com/Depart-de-Sentier/dds_glossary
[Documentation]: https://dds_glossary.readthedocs.io/
[Issue Tracker]: https://github.com/Depart-de-Sentier/dds_glossary/issues

## How to report a bug

Report bugs on the [Issue Tracker][Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker][Issue Tracker].

## How to set up your development environment

Install the package with development requirements:

```console
$ pip install -e ".[dev]"
```

## How to test the project


1. Install the package with development requirements:

```console
$ pip install -e ".[test]"
```

2. Run the full test suite:

```console
$ pytest
```

List the available Nox sessions:

Unit tests are located in the _tests_ directory,
and are written using the [pytest][pytest] testing framework.


## How to submit changes

Open a [pull request][pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The test suite must pass without errors and warnings.
- Include unit tests.
- If your changes add functionality, update the documentation accordingly.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running one of following commands, depending on your dependencies manager:

```console
# conda or mamba
$ conda install pre-commit
```

or

```
$ pip install pre-commit
```


It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pytest]: https://pytest.readthedocs.io/
[pull request]: https://github.com/Depart-de-Sentier/dds_glossary/pulls
[code of conduct]: CODE_OF_CONDUCT.md
