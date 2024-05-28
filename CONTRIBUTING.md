# Contributing

Contributions (pull requests) are very welcome! Here's how to get started.

## Getting started

First fork the library on GitHub (or GitLab).

Then clone the library.

```bash
git clone https://github.com/your-username-here/spectral.git
cd spectral
```

There are two main components: the app and the kernel. Each of them have a separate CONTRIBUTING.md, however there are also some general guidelines that apply to both. Here we continue with the general guidelines.

Install the [pre-commit hook](https://pre-commit.com/#install). For example:

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

These hooks mainly run formatters and linters for Python and Svelte. They also enforce [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). In general, this project uses the conventional commits convention, so we expect all commits to follow it (except merge commits). If a PR does not follow conventional commits it will be squashed.

## Making code changes

Spectral is divided in two parts, the app (SvelteKit) and the kernel (Python). You can refer to the readmes of the [app](app/README.md) and [kernel](/kernel/README.md) respectively to gain more insight into how to contribute.

To try out your changes, you can run the whole application using docker. First install [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/), and run:

```bash
docker compose up --build
```

Make sure to add tests when appropriate. Ideally, there should be a test that would fail without your PR. The `ci.py` script does all testing, typechecking and linting:

```bash
./ci.py
```

Verify that the tests are passing! The CI will run the tests, but you can might want to run them locally as well. You can run only integration tests by doing:

```bash
./ci.py integration
```

Please make sure to keep a reasonable git history following conventional commits. If this is not the case in a PR, the PR will be squashed by the maintainers.

After you are done with the feature, you can push your changes back to your fork:

```bash
git push
```

Finally, open a pull request on GitHub!

## Making documentation changes

Make your changes. You can then build the documentation by doing

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

Then doing `Control-C`, and running:

```bash
mkdocs serve
```

(So you run `mkdocs serve` twice.)

You can then see your local copy of the documentation by navigating to `localhost:8000` in a web browser.

## Documenting code

As part of our standard, we require that non-trivial code to be explained with comments. Make sure the comments are reasonably written with your judgement.
