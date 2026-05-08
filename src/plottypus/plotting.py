from collections.abc import Collection
from typing import Optional

import narwhals as nw
from narwhals.typing import FrameT

from plottypus.backends import get_backend
from plottypus.core import Backend, PlotType


@nw.narwhalify
def plot(
    df: FrameT,
    *,
    x: Optional[str] = None,
    y: str | Collection[str] | None = None,
    type: PlotType | str = PlotType.AUTO,
    backend: Backend | str = Backend.AUTO,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> None:
    if x:
        xcol: str = x
    elif x is None and len(df.columns) == 1:
        xcol = df.columns[0]
    else:
        raise ValueError(f"Cannot determine x column, choose from: {df.columns}")

    if y is None:
        ycols: list[str] = []
    elif isinstance(y, str):
        ycols = [y]
    else:
        ycols = list(y)

    if type == "auto":
        type_ = _get_plot_type(df, xcol, ycols)
    else:
        type_ = PlotType(type)

    b = get_backend(Backend(backend), width=width, height=height)
    return getattr(b, type_.value)(df, x=xcol, y=ycols)


def _get_plot_type(df: nw.DataFrame, xcol: str, ycols: Collection[str]) -> PlotType:
    """Find the best plot type based on the input data."""
    if df[xcol].dtype.is_numeric():
        if not ycols:
            return PlotType.HIST
        if all(df[col].dtype.is_numeric() for col in ycols):
            return PlotType.SCATTER

    raise NotImplementedError("Cannot determine plot type (yet).")
