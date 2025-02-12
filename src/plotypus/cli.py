import sys
from pathlib import Path
from typing import Optional

import typer

from plotypus.core import Backend, PlotType
from plotypus.data import read_table
from plotypus.plotting import plot


def app(
    path: Optional[Path] = typer.Argument(None, help="The path to the file to read."),
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
    width: Optional[int] = typer.Option(
        None, "-w", "--width", help="The width of the plot."
    ),
    height: Optional[int] = typer.Option(
        None, "-h", "--height", help="The height of the plot."
    ),
):
    """Plot data from a file."""

    f = sys.stdin if not sys.stdin.isatty() else None

    data = read_table(path=path, f=f)
    plot(data, x=x, y=y, type=type, backend=backend, width=width, height=height)


def run():
    typer.run(app)


if __name__ == "__main__":
    run()
