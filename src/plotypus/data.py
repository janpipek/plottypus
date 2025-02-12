from io import BytesIO
from pathlib import Path
from typing import Any, Optional

import polars as pl
from polars import ComputeError


def read_table(*, path: Optional[Path] = None, f: Any = None) -> pl.DataFrame:
    if path:
        if f:
            raise ValueError("Cannot read from both path and file object.")

        match path.suffix:
            case ".csv":
                return pl.read_csv(path)
            case ".parquet":
                return pl.read_parquet(path)
            case _:
                raise ValueError(f"Unsupported file format: {path.suffix}")

    if f:
        f_ = BytesIO(f.buffer.read())
        for method in ["read_csv", "read_parquet"]:
            try:
                return getattr(pl, method)(f_)
            except ComputeError:
                pass
        raise ValueError("Could interpret input data.")
