import os

from task.shared import read_file

if __name__ == "__main__":
    data_directory = ".\\data"
    filename = "interval_data.xlsx"
    sheet_name = "Data"
    df = read_file(os.path.join(data_directory, filename), sheet_name=sheet_name)

    df.melt(id_vars=["MPAN", "Date"], var_name="Hour", value_name="Value")