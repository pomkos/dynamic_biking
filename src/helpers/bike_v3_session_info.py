import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re

from helpers.settings_finder import settingsFinder
from helpers import helper_functions as h
from typing import List
from dataclasses import dataclass

@dataclass
class userInput:
    save_plot: bool
    save_settings_df: bool
    submit_button: bool

def app(file_locs: List[str], out_path: str, pattern: str):
    st.info('NOTE: filename expected format: "participant001_session001_date_time_type.txt"')
    all_participants_sessions_df = pd.DataFrame()
    df_length = pd.DataFrame()

    for i in range(len(file_locs)):
        file_loc = file_locs[i]
        temp_df, bike_mode = h.bike_v3_data_loader(file_loc, pattern=pattern)
        temp_df['mode'] = bike_mode
        time_diff = round(len(temp_df)/60,1)

        df_length = df_length.append(
            pd.DataFrame(
                {
                    "participant": [temp_df["participant"].unique()[0]],
                    "session": [temp_df["session"].unique()[0]],
                    "length_minutes_session": [time_diff],
                }
            ),
            ignore_index=True,
        )
        if temp_df.empty:
            continue
        else:
            all_participants_sessions_df = pd.concat([all_participants_sessions_df, temp_df])
    sf = settingsFinder(file_locations=file_locs, pattern=pattern)
    summary_of_bike_settings_df = sf.bike_v3_settings(all_participants_sessions_df= all_participants_sessions_df)
    df_info = summary_of_bike_settings_df.merge(df_length, on=["participant", "session"])
    
    st.write(
        """ The table includes some basic information about sessions, including:
    * Settings used
    * Total time for each session
    """
    )
    st.write(df_info)
    plot = h.bar_plot(
        "participant",
        "length_minutes",
        dataframe=df_info,
        out_path=out_path,
        title="Average length of sessions per participant",
    )
    plt.xlabel("Participant Code")
    plt.ylabel("Minutes")
    st.pyplot(plot)
    save_form = st.form("save_all")

    with save_form:
        st.subheader("What should be saved?")
        userInput.save_plot = st.checkbox("The plot as it looks now")
        userInput.save_settings_df = st.checkbox(
            "The table as an excel file (required for MatLab entropy script)",
            value=True,
        )
        userInput.submit_button = st.form_submit_button("Save")
        save_form = st.empty()
        save_form.info("All selected items will be saved in the 'output' folder")

    if userInput.submit_button:
        if userInput.save_settings_df:
            try:
                h.save_dataset(df_info, f"{out_path}/session_info", extension="xls")
            except PermissionError as p:
                st.error("Can't save the dataset, is `session_info.xls` open somewhere?")
                st.stop()
        if userInput.save_plot:
            h.bar_plot(
                "participant",
                "length_minutes",
                dataframe=df_info,
                out_path=out_path,
                title="Length of each session",
                save=True,
            )
        save_form.success("Saved!")

