from pathlib import Path

import typer

from plotypus.core import Backend, PlotType
from plotypus.data import read_table
from plotypus.plotting import plot


def app(
    path: str = typer.Argument(..., help="The path to the file to read."),
    type: PlotType = typer.Option(
        PlotType.AUTO, "-t", "--type", help="The type of plot to create."
    ),
    x: str = typer.Option(None, "-x", help="The column to use for the x-axis."),
    y: list[str] = typer.Option(
        None, "-y", help="The column(s) to use for the y-axis."
    ),
    backend: Backend = typer.Option(
        Backend.AUTO, "-b", "--backend", help="The plotting backend to use."
    ),
):
    """Plot data from a file."""

    data = read_table(Path(path))
    plot(data, x=x, y=y, type=type, backend=backend)


def run():
    typer.run(app)


if __name__ == "__main__":
    run()
