help:
    uv run plotypus --help

build:
    rm -rf dist/
    uv build
    rm -rf src/plotypus.egg-info

publish: build
    uv publish
