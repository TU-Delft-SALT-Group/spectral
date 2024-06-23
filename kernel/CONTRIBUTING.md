# Contributing to kernel

Contributions (pull requests) are very welcome! Here's how to get started on the kernel.

## Dependencies

For dependency management we use poetry. To install poetry run:

```bash
pip install poetry
```

To ensure that all the dependencies for the project are installed run the following:

```bash
poetry install
```

## Tips

* ```poetry shell``` enters the poetry venv, and now you won't have to _poetry run_ everything
* ```poetry install -D package_name``` installs package as a development dependency
* ```pytest --pdb``` runs pytest with a debugger: stop on an error (or breakpoint)

## Tests

There are currently two test suites available. Firstly, you can run pytest from the root of the kernel:
```bash
poetry run pytest --testmon -n auto
```
_magical flags are needed for better performance and caching_

Besides that, you are always free to run the mutation testing suite (this will take a while, estimated 10 minutes and growing!):
```bash
poetry run mutmut run
```
We are targeting 50% mutation coverage, so here is that...

## Troubleshooting

If something is not working, it is likely issue with some cache.

* Reset cache for docker with ```docker prune -a; docker volume prune -fa```
* Reset cache for testing with ```rm .testmon* .mutmut*```

Otherwise, you can try to check whether poetry is alright via:
```bash
poetry lock
poetry install
```
