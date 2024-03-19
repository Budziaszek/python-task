import os
from typing import Optional, Any

import pandas as pd


def read_file(filepath: str, sheet_name: Optional[str] = None) -> pd.DataFrame | dict[Any, pd.DataFrame]:
    """
    Reads csv or xmls file. Returns dataframe. Reads the specified sheet (sheet_name) or all.
    """

    file_name, file_extension = os.path.splitext(filepath)

    if file_extension == '.csv':
        return pd.read_csv(filepath)
    elif file_extension == ".xlsx":
        return pd.read_excel(filepath, sheet_name=sheet_name)
    else:
        raise ValueError(f"File extension '{file_extension}' is not supported.")
