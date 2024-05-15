# Contributing App

Contributions (pull requests) to the app are very welcome! Here's how to get started.

## Getting started

First fork the library on GitHub (or GitLab).

Then clone the library and go to the app folder.
// TODO: change it to `app` when the time comes

```bash
git clone https://github.com/your-username-here/spectral.git
cd spectral/frontend
```

## Contributing

As stated in the root folder's CONTRIBUTING.md, please use the general guidelines that we agreed upon. This includes:

### pre-commit

```bash
pip install pre-commit
pre-commit install
```

#### formatting hook

The pre-commit hooks enforce formatting with prettier and ESLint with each commit. It is equivalent to doing:

```bash
pnpm prettier --write . && pnpm eslint --fix .
```

This is a "custom" hook that we created and as such does not require downloading any package.

#### conventional-pre-commit

To use the conventional-pre-commit, which enforces [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), run the following command:

```bash
pre-commit install --hook-type commit-msg
```

## Making code changes

Now make your changes. Make sure to include additional tests if necessary.

### Running the application

#### Running frontend service only

If you don't require other services, there's no need to run everything! Instead, you can launch the app in dev mode with the following command:

```bash
pnpm dev
```

This should launch a vite server that auto-updates the app when a write to any file (in the app folder) gets changed.

#### Running all services locally

While making code changes, it might be required to be in contact with another service other than frontend. To simulate this, we provide a docker-compose file in the root directory of this project. To run the docker services, go to _project's root folder_ and write:

```bash
docker compose up
```

The frontend service should be accessible from `http://localhost`.

### Before committing!!

Before committing, make sure all tests are passing (this includes unit and integration tests). To run all tests, execute the following command in the app folder:

```bash
pnpm test
```

### Documentation

As part of our standard, we require that non-trivial code to be explained with comments. Make sure the comments are reasonably written with your judgement.

After you are done with the feature, and made sure to follow what we said previously, you can push your changes back to your fork:

```bash
git push
```

Finally, open a pull request on GitHub (or GitLab)!
