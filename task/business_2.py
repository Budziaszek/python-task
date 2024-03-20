import os
import pandas as pd
from numpy import mean

from task.shared import read_file

if __name__ == "__main__":
    data_directory = ".\\data"
    output_directory = ".\\results_mpan"
    filename = "interval_data.xlsx"
    sheet_name = "Data"

    df = read_file(os.path.join(data_directory, filename), sheet_name=sheet_name)
    # Note: for viewing it would be probably better to order by (date, hour)
    df = df.melt(id_vars=["MPAN", "Date"], var_name="Hour", value_name="Value")
    df["Timestamp"] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Hour'])
    print(df)

    unique_mpan = df["MPAN"].unique()
    grouped = df.groupby(df["MPAN"])

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    for mpan in unique_mpan:
        mpan_df = grouped.get_group(mpan)
        result = mpan_df[["MPAN", "Timestamp", "Value"]]\
            .groupby([pd.Grouper(key='Timestamp', freq='W-MON')])\
            .agg({"Value": ['min', 'max', 'mean']})
        result.to_excel(os.path.join(output_directory, f"results_{mpan}.xlsx"))
