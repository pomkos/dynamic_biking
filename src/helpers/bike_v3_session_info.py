import streamlit as st
import pandas as pd
import re

from helpers import helper_functions as h
from typing import List

def app(file_locs: List[str], out_path: str, pattern: str):
    st.write(file_locs)
    st.info('NOTE: filename expected format: "participant001_session001_date_time_type.txt"')
    file_locs = [file_locs[0]]
    df = bike_v3_file_formatter(file_locs[0], i=1, pattern=pattern)

    s = h.settingsFinder(file_locations=file_locs, pattern=pattern)
    settings = s.assemble_settings_df(bike_version=3)

    st.info("to be implemented")
    
def bike_v3_file_formatter(file: str, i: int, pattern: str) -> pd.DataFrame:
    '''
    Adds participant, session, id_sess columns
    '''
    # extract filename from location, used to get the participant ID and date
    if ("/" in file) or ("\\" in file):
        filename = file.replace("\\", "/").split("/")[-1]
    else:
        filename = file

    # extract participant id from the filename
    participant_id = filename.split("_")[0]
    session_id = filename.split("_")[1]

    temp_df = pd.read_csv(file, skiprows=1)
    
    # standardize column names
    temp_df.columns = [col.strip().lower().replace(' ', '_') for col in temp_df.columns]
    temp_df.columns = [col.replace(')', '').replace('(','_') for col in temp_df.columns]

    # format strings to avoid unpleasant surprises
    for col in temp_df.select_dtypes('object'):
        temp_df[col] = temp_df[col].str.strip()
    
    temp_df['seconds_elapsed'] = pd.to_timedelta(temp_df['session_timer']).dt.total_seconds()
    temp_df = temp_df.rename({
        'session_timer': 'timer'
    }, axis=1)

    # extract date from the filename, then append the time column
    temp_df["date"] = (
        re.findall("(\d\d_\d\d_\d\d\d\d)", filename)[0].replace("_", "/")
        + " "
        + temp_df["time"]
    ).astype('datetime64[ns]')

    temp_df['participant'] = participant_id
    temp_df['session'] = session_id
 
    # reorganize columns
    temp_df = temp_df[
        [
            "participant",
            "session",
            "date",
            "timer",
            "seconds_elapsed",
            "speed_rpm",
            "power_w",
            "heart_beat",
            "speed_set",
            "stiffness"
        ]
    ]

    # rename some columns
    temp_df = temp_df.rename(
        {"power_w": "power_watt", "heart_beat": "heart_rate"}, axis=1
    )
    temp_df["id_sess"] = temp_df["participant"] + "_" + temp_df["session"]

    return temp_df