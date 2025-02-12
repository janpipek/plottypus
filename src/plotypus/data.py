from pathlib import Path

import polars as pl


def read_table(path: Path) -> pl.DataFrame:
    match path.suffix:
        case ".csv":
            return pl.read_csv(path)
        case ".parquet":
            return pl.read_parquet(path)
        case _:
            raise ValueError(f"Unsupported file format: {path.suffix}")
