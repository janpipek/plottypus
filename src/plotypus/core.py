from enum import StrEnum


class PlotType(StrEnum):
    AUTO = "auto"
    HIST = "hist"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    LINE = "line"
    BAR = "bar"
    HBAR = "hbar"


class Backend(StrEnum):
    AUTO = "auto"
    PLOTEXT = "plotext"
    PLOTILLE = "plotille"
    PHYST = "physt"
