# plottypus

**!!! WORK IN PROGRESS !!!**

This is an example (though perhaps useful) project to demonstrate how to use
various plotting libraries in Python:

- [plotext](https://github.com/piccolomo/plotext)
- [plotille](https://github.com/tammoippen/plotille)
- [physt](https://github.com/janpipek/physt)

## Installation

The application is (pip/uv/pipx-installable):

```
uv tool install plottypus
```

```
pipx install plottypus
```

```
pip install plottypus
```

## Usage

```
Usage: plottypus [OPTIONS] [PATH]

 Plot data from a file.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│   path      [PATH]  The path to the file to read. [default: None]                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --type     -t      [auto|hist|scatter|heatmap|line|bar|hbar]  The type of plot to create. [default: auto]   │
│            -x      TEXT                                       The column to use for the x-axis.             │
│                                                               [default: None]                               │
│            -y      TEXT                                       The column(s) to use for the y-axis.          │
│                                                               [default: None]                               │
│ --backend  -b      [auto|plotext|plotille|physt]              The plotting backend to use. [default: auto]  │
│ --width    -w      INTEGER                                    The width of the plot. [default: None]        │
│ --height   -h      INTEGER                                    The height of the plot. [default: None]       │
│ --help                                                        Show this message and exit.                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

You can pipe in CSV or Parquet data, enabling a natural collaboration with other tools
like duckdb or xsv.
