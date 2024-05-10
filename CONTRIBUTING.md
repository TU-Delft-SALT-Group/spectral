# Contributing

Contributions (pull requests) are very welcome! Here's how to get started.

## Getting started

First fork the library on GitHub (or GitLab).

Then clone the library.

```bash
git clone https://github.com/your-username-here/spectral.git
cd spectral
```

There are two main components: the frontend and the backend. Each of them have a separate CONTRIBUTING.md, however there are also some general guidelines that apply to both. Here we continue with the general guidelines.

Install the [pre-commit hook](https://pre-commit.com/#install). For example:

```bash
pip install pre-commit
pre-commit install
```

These hooks use ruff to format the Python backend code, and pyright to lint it. For svelte we use ESLint and Prettier.

### conventional-pre-commit
To use the conventional-pre-commit, which enforces [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), run the following command:

```bash
pre-commit install --hook-type commit-msg
```

## Making code changes 

Now make your changes. Make sure to include additional tests if necessary.

Verify that the tests are passing! The CI will run the tests, but you can might want to run them locally as well. You can run only integration tests by doing:

```bash
???
```

After you are done with the feature, you can push your changes back to your fork:

```bash
git push
```

Finally, open a pull request on GitHub (or GitLab)!

## Making documentation changes

Make your changes. You can then build the documentation by doing

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

Then doing `Control-C`, and running:

```
mkdocs serve
```

(So you run `mkdocs serve` twice.)

You can then see your local copy of the documentation by navigating to `localhost:8000` in a web browser.
