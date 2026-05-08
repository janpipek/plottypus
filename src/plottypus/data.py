from io import BytesIO, TextIOWrapper
from pathlib import Path
from typing import cast

import polars as pl


def read_table(path_or_file: str | Path | TextIOWrapper) -> pl.DataFrame:
    if isinstance(path_or_file, Path | str):
        path = Path(path_or_file)
        match path.suffix:
            case ".csv":
                return pl.read_csv(path, try_parse_dates=True)
            case ".parquet":
                return pl.read_parquet(path)
            case _:
                raise ValueError(f"Unsupported file format: {path_or_file.suffix}")

    elif isinstance(path_or_file, TextIOWrapper):
        f_ = BytesIO(path_or_file.buffer.read())
        for method in ["read_csv", "read_parquet"]:
            try:
                return cast(pl.DataFrame, getattr(pl, method)(f_))
            except:  # noqa: E722
                continue
        raise ValueError("Could interpret input data.")

    raise TypeError(f"Unsupported input object: {type(path_or_file)}")
