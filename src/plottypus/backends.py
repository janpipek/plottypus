from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, Optional

import physt.plotting.ascii
import plotext as plt
import plotille
import polars as pl
from physt import h1, h2

from plottypus.core import Backend

if TYPE_CHECKING:
    from matplotlib.axes import Axes


@dataclass
class BaseBackend:
    width: int
    height: int

    def __init__(self, *, width: Optional[int] = None, height: Optional[int] = None):
        self.width = width or plt.tw() or 80
        self.height = height or plt.th() or 25

    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("hist", df, x=x, y=y)

    def scatter(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("scatter", df, x=x, y=y)

    def line(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("line", df, x=x, y=y)

    def heatmap(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("heatmap", df, x=x, y=y)

    def bar(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("bar", df, x=x, y=y)

    def hbar(self, df: pl.DataFrame, *, x: str, y: list[str]):
        return self._default_plot("hbar", df, x=x, y=y)

    def _default_plot(self, name, *args, **kwargs):
        raise NotImplementedError(
            f"Plot type {name} not supported in {self.__class__.__name__}"
        )


class Plotille(BaseBackend):
    @property
    def _plotille_dims(self) -> dict:
        return {
            "width": max(1, self.width - 20),
            "height": max(1, self.height - 7),
        }

    def line(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])

        fig = plotille.Figure()
        fig.height = self._plotille_dims["height"]
        fig.width = self._plotille_dims["width"]

        for col_y in y:
            fig.plot(df[x].to_list(), df[col_y].to_list(), label=col_y)
        print(fig.show(legend=True))

    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        if y:
            raise ValueError("Plotille does not support histograms with y values")

        df = df.drop_nulls([x])
        print(
            plotille.histogram(df[x].cast(pl.Float64).to_list(), **self._plotille_dims)
        )


class Plotext(BaseBackend):
    def scatter(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])
        for col_y in y:
            plt.scatter(df[x], df[col_y])
        plt.plot_size(self.width, self.height)
        plt.show()

    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])
        plt.hist(df[x].cast(pl.Float64))
        plt.plot_size(self.width, self.height)
        plt.show()

    def hbar(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])
        plt.bar(df[y[0]], df[x], orientation="horizontal")
        plt.plot_size(self.width, self.height)
        plt.show()

    def bar(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])
        plt.bar(df[x], df[y[0]])
        plt.plot_size(self.width, self.height)
        plt.show()

    def line(self, df: pl.DataFrame, *, x: str, y: list[str]):
        df = df.drop_nulls([x, *y])
        for col_y in y:
            plt.plot(df[x], df[col_y], label=col_y)
        plt.plot_size(self.width, self.height)
        plt.xlabel(x)
        plt.show()


class Physt(BaseBackend):
    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        if len(y) == 0:
            h = h1(df[x], "pretty")
            physt.plotting.ascii.hbar(h, show_values=True, width=self.width)

    def heatmap(self, df: pl.DataFrame, *, x: str, y: list[str]):
        if len(y) == 1:
            h = h2(df[x], df[y[0]], "pretty")
            physt.plotting.ascii.map(h)


class _MatplotlibBackend(BaseBackend, ABC):
    @contextmanager
    def get_axes(self) -> Iterator["Axes"]:
        with self._setup_matplotlib():
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            yield ax
            plt.show()

    @abstractmethod
    def _setup_matplotlib(self):
        ...

    def _apply_labels_and_legend(self, ax, xcol, ycols):
        ax.set_xlabel(xcol)
        if len(ycols) == 1:
            ax.set_ylabel(ycols[0])
        if len(ycols) > 1:
            ax.legend()

    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        with self.get_axes() as ax:
            df = df.drop_nulls([x, *y])
            ax.hist(df[x].to_numpy())
            ax.set_ylabel("Frequency")
            self._apply_labels_and_legend(ax=ax, xcol=x, ycols=x)

    def scatter(self, df: pl.DataFrame, *, x: str, y: list[str]):
        with self.get_axes() as ax:
            df = df.drop_nulls([x, *y])
            for col_y in y:
                ax.scatter(df[x].to_numpy(), df[col_y].to_numpy(), label=col_y)
            self._apply_labels_and_legend(ax=ax, xcol=x, ycols=x)

    def line(self, df: pl.DataFrame, *, x: str, y: list[str]):
        with self.get_axes() as ax:
            df = df.drop_nulls([x, *y])
            for col_y in y:
                ax.plot(df[x].to_numpy(), df[col_y].to_numpy(), label=col_y)
            self._apply_labels_and_legend(ax=ax, xcol=x, ycols=x)


class Kitty(_MatplotlibBackend):
    @contextmanager
    def _setup_matplotlib(self) -> Iterator[None]:
        # TODO: Check that it is supported
        import matplotlib

        matplotlib.use("module://matplotlib-backend-kitty")
        yield


class NotCurses(_MatplotlibBackend):
    @contextmanager
    def _setup_matplotlib(self) -> Iterator[None]:
        # TODO: Check that it is supported
        import matplotlib

        matplotlib.use("module://matplotlib-backend-notcurses")
        yield


class AutoBackend(BaseBackend):
    def _default_plot(self, name, *args, **kwargs):
        for backend_type in [Physt, Plotille, Plotext]:
            try:
                backend = backend_type(width=self.width, height=self.height)
                return getattr(backend, name)(*args, **kwargs)
            except NotImplementedError:
                pass
        raise NotImplementedError(f"Plot type {name} not supported in any backend")


def get_backend(
    backend: Backend, *, width: Optional[int], height: Optional[int]
) -> BaseBackend:
    return {
        Backend.AUTO: AutoBackend,
        Backend.PLOTILLE: Plotille,
        Backend.PLOTEXT: Plotext,
        Backend.PHYST: Physt,
        Backend.KITTY: Kitty,
        Backend.NOTCURSES: NotCurses,
    }[backend](width=width, height=height)
