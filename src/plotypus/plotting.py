from collections.abc import Collection
from typing import Optional

import physt.plotting.ascii
import plotext as plt
import polars as pl
from physt import h1

from plotypus.core import PlotType


def plot(
    df: pl.DataFrame,
    *,
    x: Optional[str] = None,
    y: str | Collection[str] | None = None,
    type: PlotType = PlotType.AUTO,
    backend: str = "auto",
):
    if x:
        xcol = x
    elif x is None and len(df.columns) == 1:
        xcol = df.columns[0]
    else:
        raise ValueError("Cannot determine x column.")

    if y is None:
        ycols = []
    elif isinstance(y, str):
        ycols = [y]
    else:
        ycols = list(y)

    if type == "auto":
        type = _get_plot_type(df, xcol, ycols)

    match type:
        case PlotType.SCATTER:
            scatter(df, x=xcol, y=ycols, backend=backend)
        case PlotType.HIST:
            hist(df, x=xcol, y=ycols, backend=backend)


def scatter(df: pl.DataFrame, *, x: str, y: list[str], backend: str):
    for col_y in y:
        plt.scatter(df[x], df[col_y])
    plt.show()


def hist(df: pl.DataFrame, *, x: str, y: list[str], backend: str):
    h = h1(df[x])
    physt.plotting.ascii.hbar(h, show_values=True)


def _get_plot_type(df: pl.DataFrame, xcol: str, ycols: Collection[str]) -> PlotType:
    """Find the best plot type based on the input data."""
    if df[xcol].dtype.is_numeric():
        if not ycols:
            return PlotType.HIST
        if all(df[col].dtype.is_numeric() for col in ycols):
            return PlotType.SCATTER

    raise NotImplementedError("Cannot determine plot type (yet).")
