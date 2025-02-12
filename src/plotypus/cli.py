from pathlib import Path

import typer

from plotypus.core import PlotType
from plotypus.data import read_table
from plotypus.plotting import plot


def app(
    path: str = typer.Argument(..., help="The path to the file to read."),
    type: PlotType = typer.Option(PlotType.AUTO, help="The type of plot to create."),
    x: str = typer.Option(None, help="The column to use for the x-axis."),
    y: str = typer.Option(None, help="The column to use for the y-axis."),
):
    """Plot data from a file."""

    data = read_table(Path(path))
    plot(data, x=x, y=y, type=type)


def run():
    typer.run(app)


if __name__ == "__main__":
    run()
