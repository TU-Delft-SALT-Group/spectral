FROM python:3.12-bookworm as python-base

WORKDIR /docs

RUN pip install mkdocs

CMD mkdocs serve

