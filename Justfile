help:
    uv run plotypus --help

build:
    rm -rf dist/
    uv build
    rm -rf src/plotypus.egg-info

publish: build
    uv publish

example-co2:
    uv run plottypus examples/co2_emissions/annual-co2-emissions.csv -t line -x Year -y "Annual CO₂ emissions" -w 80
