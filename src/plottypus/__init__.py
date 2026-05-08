"""Wrapper around CLI plotting tools."""

from plottypus.core import Backend, PlotType
from plottypus.data import read_table
from plottypus.plotting import plot

__all__ = ["plot", "Backend", "PlotType", "read_table"]
