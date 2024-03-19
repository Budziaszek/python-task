import os
from typing import Optional, Any, Generator, List

import pandas as pd


def find_files(prefix: str, directory: str) -> Generator[str, None, None]:
    """
    Returns generator with all files that starts with the specified prefix from directory.
    """
    for file in os.listdir(directory):
        if file.startswith(prefix):
            yield str(os.path.join(directory, file))


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


filename_prefix = "Table_"
data_directory = ".\\data"
sheet_name = "Sheet1"  # Always get data from Sheet1, we can potentially use all sheets, first sheet etc.

files = find_files(prefix=filename_prefix, directory=data_directory)
df = pd.concat([read_file(file, sheet_name=sheet_name) for file in files])

df.drop_duplicates(inplace=True)
print(f"Number of null values:'\n {df.isnull().sum()}\n")



