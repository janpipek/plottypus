from collections.abc import Collection
from typing import Optional

import polars as pl

from plotypus.backends import get_backend
from plotypus.core import Backend, PlotType


def plot(
    df: pl.DataFrame,
    *,
    x: Optional[str] = None,
    y: str | Collection[str] | None = None,
    type: PlotType = PlotType.AUTO,
    backend: Backend = Backend.AUTO,
) -> None:
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

    b = get_backend(backend)
    return getattr(b, type.value)(df, x=xcol, y=ycols)


def _get_plot_type(df: pl.DataFrame, xcol: str, ycols: Collection[str]) -> PlotType:
    """Find the best plot type based on the input data."""
    if df[xcol].dtype.is_numeric():
        if not ycols:
            return PlotType.HIST
        if all(df[col].dtype.is_numeric() for col in ycols):
            return PlotType.SCATTER

    raise NotImplementedError("Cannot determine plot type (yet).")
