'''
This script relies on the MatLab entropy calculator scripts' output, 
must have a "Power" and "ID" column, where the "ID" column is unique
to each participant and session.
'''
import glob
import pandas as pd
import streamlit as st

def app(out_path):
    file_locs = glob.glob(
        f"{out_path}/*.xlsx", recursive=True
    )
    # in case they rerun the script but kept original xlsx file in the output folder
    file_locs = [file for file in file_locs if "entropy_effort.xlsx" not in file]
    all_efforts_df = pd.DataFrame()
    for file in file_locs:
        temp_df = pd.read_excel(file)
        new_df = perc_time_in_col(temp_df, col='Power', threshold=0, perc="greater", id_col='ID')
        new_df = new_df[['ID', 'effort']]
        all_efforts_df = all_efforts_df.append(new_df)

    return all_efforts_df



def perc_time_in_col(dataframe, col, threshold=0, perc="greater", id_col="ID"):
    """
    OG purpose: Calculates the percent occurrance of positive `col` values per `id_col`.
    NOT whether the mean is neg or pos.
    input
    -----
    dataframe: pd.DataFrame
    col: str
        Variable of interest to count
    threshold: int
        Number (noninclusive) to consider as threshold
    perc: string
        One of "greater", "lesser", or "equal"
        Determines how to compare all values to the threshold
    id_col: str
        Column participants are identified by
    return
    ------
    df_merged: pd.DataFrame
        Each row represents one `id_col`
        Columns are counts of `col` < 0 and perc in negative for each `id_col`
    """
    try:
        all_count = dataframe.groupby([id_col]).count()[
            [col]
        ]  # count number of lines per id_col

        if perc == "greater":
            val_ = dataframe[dataframe[col] > threshold]  # filter to > threshold
            compare = "pos"
        elif perc == "lesser":
            val_ = dataframe[dataframe[col] < threshold]  # filter to < threshold
            compare = "neg"
        else:
            val_ = dataframe[dataframe[col] == threshold]  # filter to equal threshold
            compare = f"_{threshold}"

        val_count = val_.groupby([id_col]).count()[
            [col]
        ]  # count number of positive lines per id_col

        df1 = all_count.reset_index()  # reset indexes so dataframes can be merged
        df2 = val_count.reset_index()
        df_merged = df2.merge(
            df1, on=[id_col], suffixes=[f"_{compare}", "_all"], how="right"
        )
        # NAs represent id_sess that were in df1 but not in df2
        # if they're not in df2, there were no positive powers
        df_merged = df_merged.fillna(0)
        # calculate and round percent
        df_merged[f"effort"] = round(
            100 * (df_merged[f"{col}_{compare}"] / df_merged[f"{col}_all"]), 2
        )
        df_merged = df_merged.sort_values(f"effort", ascending=False)
        return df_merged
    except Exception as e:
        st.error(
            "REMINDER: make sure participant ID and session labels are one variable (ex: id_sess)"
        )
        return e