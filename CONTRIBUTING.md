# Contributing to HandyPy

Welcome! `handy.py` is a collection of handy utils for Python.

## The contribution process at a glance

1. [Prepare your environment](#preparing-the-environment).
2. [Format your code](#formatting-the-code).
3. [Submit your changes](#submitting-changes) by opening a pull request.
4. [Review and merge Pull Requests](#maintainer-guidelines)

You can expect a reply within a few days, but please be patient when
it takes a bit longer. For more details, read below.

## Preparing the environment

### Code away

HandyPy runs continuous integration (CI) on all pull requests. This will
automatically fix formatting (using [`black`](https://black.readthedocs.io/en/stable/),
[`isort`](https://pycqa.github.io/isort/)) and run tests.
It means you can ignore all local setup on your side, focus on the
code and rely on the CI to fix everything, or point you to the places that
need fixing.

### ... Or create a local development environment

If you prefer to run the tests formatting locally, it's
possible too. Follow platform-specific instructions below.
<!-- For more information about our available tests, see
[tests/README.md](tests/README.md). -->

Whichever platform you're using, you will need a
virtual environment (using `pipenv`). If you're not familiar with what it is and how it works,
please refer to this
[documentation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

### Linux/macOS

On Linux and macOS, you will be able to run the full test suite on Python 3.9.

To install the necessary requirements, run the following commands from a
terminal window:

```bash
pip install -U pip pipx
pipx install pipenv

pipenv sync
pipenv install --dev
```

### Windows

If you are using a Windows operating system, you will not be able to run the
full test suite. One option is to install
[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/faq),
which will allow you to run the full suite of tests. If you choose to install
WSL, follow the Linux/macOS instructions above.

If you do not wish to install WSL, you will not be able to run the pytype
tests, as pytype
[does not currently support running on Windows](https://github.com/google/pytype#requirements).
However, the upside of this is that you will be able to run all
Windows-compatible tests on Python 3.9, or 3.10, as it is only the pytype
tests that cannot currently be run on 3.10.

To install all non-pytype requirements on Windows without WSL, run the
following commands from a Windows terminal:

```bash
> python3 -m pip install -U pip pipx
> pipx install pipenv

> pipenv sync
> pipenv install --dev
```

## Formatting the code

The code is formatted by `black` and `isort`.

The repository is equipped with a [`pre-commit.ci`](https://pre-commit.ci/)
configuration file. This means that you don't *need* to do anything yourself to
run the code formatters. When you push a commit, a bot will run those for you
right away and add a commit to your PR. Neat, no?

That being said, if you *want* to run the checks locally when you commit, you
can install the hooks: please refer to the [pre-commit](https://pre-commit.com/)
documentation.

```bash
pipenv run pre-commit run --all-files
```

## Submitting changes

Even more excellent than a good bug report is a fix for a bug, or the
implementation of a new feature. We'd love to have
your contributions.

We use the usual GitHub pull-request flow, which may be familiar to
you if you've contributed to other projects on GitHub.  For the
mechanics, see [Mypy's git and GitHub workflow help page](https://github.com/python/mypy/wiki/Using-Git-And-GitHub),
or [GitHub's own documentation](https://help.github.com/articles/using-pull-requests/).

Anyone interested in Python may review your code. One of the
maintainers will merge your pull request when they think it's ready.
For every pull request, we aim to promptly either merge it or say why
it's not yet ready; if you go a few days without a reply, please feel
free to ping the thread by adding a new comment.

To get your pull request merged sooner, you should explain why you are
making the change. It is also helpful to add links to online
documentation or to the implementation of the code you are changing.

Also, do not squash your commits or use `git commit --amend`
after you have submitted a pull request, as this erases context during review.
We will squash commits when the pull request is merged.
This way, your pull request will appear as a single commit in our git history, even
if it consisted of several smaller commits.

## Maintainer guidelines

The process for preparing and submitting changes also applies to
maintainers.  This ensures high quality contributions and keeps
everybody on the same page.  Avoid direct pushes to the repository.

When reviewing pull requests, follow these guidelines:

* Try to be helpful and explain issues with the PR,
  especially to new contributors.
* When reviewing auto-generated stubs, just scan for red flags and obvious
  errors. Leave possible manual improvements for separate PRs.
* When reviewing large, hand-crafted PRs, you only need to look for red flags
  and general issues, and do a few spot checks.
* Review smaller, hand-crafted PRs thoroughly.

When merging pull requests, follow these guidelines:

* Always wait for tests to pass before merging PRs.
* Use "[Squash and merge](https://github.com/blog/2141-squash-your-commits)" to merge PRs.
* Make sure the commit message is meaningful. For example, remove irrelevant
  intermediate commit messages.
* The commit message is used to generate the changelog.
  It should be valid Markdown, be comprehensive, read like a changelog entry,
  and assume that the reader has no access to the diff.
* Delete branches for merged PRs (by maintainers pushing to the main repo).
