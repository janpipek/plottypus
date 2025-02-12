import physt.plotting.ascii
import plotext as plt
import polars as pl
from physt import h1, h2

from plotypus.core import Backend


class BaseBackend:
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
    pass


class Plotext(BaseBackend):
    def scatter(self, df: pl.DataFrame, *, x: str, y: list[str]):
        for col_y in y:
            plt.scatter(df[x], df[col_y])
        plt.show()


class Physt(BaseBackend):
    def hist(self, df: pl.DataFrame, *, x: str, y: list[str]):
        if len(y) == 0:
            h = h1(df[x], "pretty")
            physt.plotting.ascii.hbar(h, show_values=True)

    def heatmap(self, df: pl.DataFrame, *, x: str, y: list[str]):
        if len(y) == 1:
            h = h2(df[x], df[y[0]], "pretty")
            physt.plotting.ascii.map(h)


class AutoBackend(BaseBackend):
    def _default_plot(self, name, *args, **kwargs):
        for backend_type in [Physt, Plotille, Plotext]:
            try:
                backend = backend_type()
                return getattr(backend, name)(*args, **kwargs)
            except NotImplementedError:
                pass
        raise NotImplementedError(f"Plot type {name} not supported in any backend")


def get_backend(backend: Backend) -> BaseBackend:
    return {
        Backend.AUTO: AutoBackend,
        Backend.PLOTILLE: Plotille,
        Backend.PLOTEXT: Plotext,
        Backend.PHYST: Physt,
    }[backend]()
