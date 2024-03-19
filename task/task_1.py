import csv
import os
from typing import Optional, Any, Generator, Dict

import numpy as np
import pandas as pd
from pandas.tseries.offsets import CDay, CustomBusinessDay
from pandas.tseries.holiday import (
    Holiday,
    GoodFriday,
    EasterMonday,
    AbstractHolidayCalendar,
    next_monday,
    next_monday_or_tuesday,
    MO
)


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


class HolidaysUK(AbstractHolidayCalendar):
    rules = [
        Holiday('New Years Day', month=1, day=1, observance=next_monday),
        GoodFriday,
        EasterMonday,
        Holiday('Early May Bank Holiday', month=5, day=1, offset=pd.DateOffset(weekday=MO(1))),
        Holiday('Spring Bank Holiday', month=5, day=31, offset=pd.DateOffset(weekday=MO(-1))),
        Holiday('Summer Bank Holiday', month=8, day=31, offset=pd.DateOffset(weekday=MO(-1))),
        Holiday('Christmas Day', month=12, day=25, observance=next_monday),
        Holiday('Boxing Day', month=12, day=26, observance=next_monday_or_tuesday)
    ]


def count_business_days(business_days: CustomBusinessDay, start_date: pd.Timestamp, end_date: pd.Timestamp):
    """
    Counts business days between two dates.
    """
    if pd.isnull(start_date) or pd.isnull(end_date):
        return np.datetime64('NaT')
    return len(pd.date_range(start_date, end_date, freq=business_days))


def convert_currency(
        amount: float,
        from_currency: str,
        to_currency: str,
        currency_rates_usd:
        Dict[str, float]) -> float:
    return round((amount / currency_rates_usd[from_currency]) * currency_rates[to_currency], 2)


if __name__ == "__main__":
    filename_prefix = "Table_"
    data_directory = ".\\data"
    output_directory = ".\\results"
    sheet_name = "Sheet1"  # Always get data from Sheet1, we can potentially use all sheets, first sheet etc.
    acctg_date_column = 'Acctg Date'
    date_column = 'Date'
    amount_column = 'Amount'
    currency_column = "Currency"
    type_column = "Type"
    currency_file = "FXrates.csv"

    files = find_files(prefix=filename_prefix, directory=data_directory)
    df = pd.concat([read_file(file, sheet_name=sheet_name) for file in files])

    df.drop_duplicates(inplace=True)

    print(f"Number of null values:\n {df.isnull().sum()}\n")
    numeric_columns = df.select_dtypes(include=np.number).columns
    df[numeric_columns] = df[numeric_columns].fillna(value=1337)

    date_columns = [acctg_date_column, date_column]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)

    df['Period'] = df[acctg_date_column] - df[date_column]
    # Use custom calendar
    business_days = CDay(calendar=HolidaysUK())
    df["Period Business Days"] = df.apply(
        lambda row: count_business_days(
            business_days=business_days,
            start_date=row[acctg_date_column],
            end_date=row[date_column]),
        axis=1)

    # Read currency data
    with open(os.path.join(data_directory, currency_file)) as f:
        currency_data = csv.reader(f)
        next(currency_data)
        currency_rates = {key: float(value) for key, value in currency_data}

    # Converting amount (inplace, changing currency column)
    df[amount_column + "PLN"] = df.apply(
        lambda row: convert_currency(
            amount=row[amount_column],
            from_currency=row[currency_column],
            to_currency="PLN",
            currency_rates_usd=currency_rates),
        axis=1)
    # df[currency_column] = "PLN"

    unique = df[type_column].unique()
    grouped = df.groupby(df[type_column])

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    for u in unique:
        # Need to do something with special chars
        # Note: Using ASCII representation to make sure no file will be overwritten.
        #       Best solution should be discussed. Personally, I would consider removing polish chars.
        u_modified = ''.join([c if c.isalnum() else str(ord(c)) for c in u])
        print(u, u_modified)
        filename = os.path.join(output_directory, f"Table_{u_modified}.xlsx")
        grouped.get_group(u).to_excel(filename)
