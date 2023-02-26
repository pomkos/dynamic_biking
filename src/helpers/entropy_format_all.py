"""
Series of functions to get the dataset ready for what MatLab script
expects as input. Formats the entire dataset all at once
"""
from helpers import helper_functions as h  # brains behind the operation
import pandas as pd  # dataframe manipulation
import streamlit as st  # GUI
import matplotlib.pyplot as plt  # save plot
import seaborn as sns  # create plot
from stqdm import stqdm  # progress bar
from typing import List


def save_as_files(dataframe: pd.DataFrame, out_path, save_form) -> None:
    """
    Save all unique participants (code) as a separate xlsx file,
    formatted for MatLab.
    """
    import datetime as dt

    p_sess = list(dataframe["id_sess"].unique())
    num_sess = len(p_sess)
    dataframe["date_"] = dataframe["date"].apply(lambda x: x.date())
    for i in stqdm(range(num_sess)):
        p = p_sess[i]
        temp_df = dataframe[(dataframe["id_sess"] == p)]
        temp_df = temp_df[
            ["date", "heart_rate", "speed_rpm", "power_watt", "id_sess"]
        ]  # select approp cols, order for Matlab
        temp_df.columns = [
            "Date",
            "HR",
            "Cadence",
            "Power",
            "ID",
        ]  # format col name for Matlab
        try:
            h.save_dataset(temp_df, f"{out_path}/{p}")
        except PermissionError as p_error:
            st.error(f"Can't save the file, is `{p}`.xlsx open somewhere?")
            st.stop()


def facet_grid(x, y, title, dataframe, out_path, hue=None, reverse=False, save=False):
    """
    Returns a figure for streamlit. Creates facet grid
    using participant and session columns
    """
    if reverse:
        row = "session"
        col = "participant"
    else:
        row = "participant"
        col = "session"
    st.write(f"__NOTE:__ Columns are {col} and rows {row} IDs")
    st.info("__Tip:__ Text too small? Scroll down to save the image, then open it with windows and zoom in.")
    g = sns.relplot(
        x=x, y=y, data=dataframe, row=row, col=col, facet_kws={"sharex": False}
    )
    g.fig.suptitle(title, y=1)
    if save:
        g.savefig(f"{out_path}/facet_grid.png", dpi=300)
    return g


@st.cache(suppress_st_warning=True)
def load_dataframe(file_locs, pattern, bike_version: int) -> pd.DataFrame:
    """
    This function is cached so the dataset won't be reloaded on each run of the script
    """
    # import and format each bike dataframe
    dataframe = pd.DataFrame()
    if bike_version == 3:
        for i in range(len(file_locs)):
            df = pd.read_csv(file_locs[i], header=1)
            df.columns = [col.strip() for col in df.columns]
            for col in df.select_dtypes('object'):
                df[col] = df[col].str.strip()
            dataframe = pd.concat([dataframe, df])

    elif bike_version == 2:
        for i in range(len(file_locs)):
            temp_df = h.bike_v2_file_formatter(file_locs[i], i + 1, pattern)
            dataframe = dataframe.append(temp_df)
    return dataframe


@st.cache()
def cut_dataframe(dataframe: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """
    This function is cached so the dataset won't be recut each time a button is pressed
    """
    if (start == 0) and (end == 0):
        new_df = dataframe.copy()
        return new_df

    if end == 0:
        end = len(dataframe)
    
    new_df = dataframe[(dataframe["seconds_elapsed"] >= start) & (dataframe["seconds_elapsed"] <= end)]
    return new_df


def app(file_locs: List[str], bike_version: int, pattern: str, in_path: str, out_path: str):
    # all_filenames = h.get_filename(file_locs)

    st.write('''
This step will get the dynamic bike files in the `input` folder ready for entropy analysis. Everything is automatic, except for the clipping. Follow the instructions below:

1. Each session needs to be clipped so there are no sudden jumps from warmup->main or main->cooldown
2. Use the sidebar to indicate where to clip the graphs
3. Once satisfied, click `Save` at the bottom of the page
4. All files will be saved in the `output` folder, overwriting any existing files of the same name
    ''')
    df = load_dataframe(file_locs, pattern, bike_version)  # run once
    st.sidebar.write("--------------------")
    
    start = st.sidebar.number_input("Start", min_value=0.0, step=1.0)
    end = st.sidebar.number_input("End", min_value=0.0, step=1.0)
    st.sidebar.info(
        "Modify the dataset to eliminate sudden jumps at the beginning or end of the graphs"
    )

    new_df = cut_dataframe(
        df, start, end
    ).copy()  # run if the start/end values are changed
    st.subheader("Mass edit")

    reverse = st.checkbox("Columns as participants")
    with st.spinner("Loading facet grid plot"):
        plot = facet_grid(
            x="seconds_elapsed",
            y="speed_rpm",
            dataframe=new_df,  # run if parameters are changed
            out_path=out_path,
            title="Cadence over time",
            reverse=reverse,
        )
        st.pyplot(plot.fig)

    with st.expander("Show current dataset"):
        st.info(
            "This is a dataset of all files in one, save if you want all time series in one file."
        )
        preview = new_df.head()
        st.write(preview)

    with st.form("save_results"):
        st.subheader("What should be saved?")
        save_plot = st.checkbox("The plot as it looks now")
        save_all_in_one = st.checkbox("All sessions in one excel file")
        save_matlab = st.checkbox(
            "All sessions formatted for MatLab (required for MatLab entropy script)",
            value=True,
        )

        save_us = st.form_submit_button("Save")
        save_form = st.empty()
        save_form.info("All selected items will be saved in the 'output' folder")

    if save_us:
        save_form.warning("Do not close browser until successful save")
        if save_plot:
            facet_grid(
                x="seconds_elapsed",
                y="speed_rpm",
                dataframe=new_df,  # run if parameters are changed
                out_path=out_path,
                title="Cadence over time",
                reverse=reverse,
                save=True,
            )
        if save_all_in_one:
            h.save_dataset(new_df, f"{out_path}/all_sessions", extension='xls')
        if save_matlab:
            save_as_files(new_df, out_path, save_form)
        save_form.success("Saved!")
