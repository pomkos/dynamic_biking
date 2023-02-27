import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import re
from typing import List

def save_dataset(dataframe, name, extension="xlsx"):
    """
    Function to standardize saving files
    """
    dataframe.to_excel(f"{name}.{extension}", index=False)


def get_idsess_from_bike_v2(filename: str, pattern: str):
    """
    Returns a list of filenames, extract from string of location
    """
    import re
    import streamlit as st

    if pattern:
        my_id = re.findall(f"({pattern['id']})", filename)[0]
        sess = re.findall(f"({pattern['sess']})", filename)[0]
        return my_id, sess
    else:
        my_id = filename.split("_")[-2].strip(".txt")
        sess = filename.split("_")[-1].strip(".txt")
        return my_id, sess


def bar_plot(x, y, title, dataframe, out_path, hue=None, save=False):
    """
    Function so streamlit can show it easier
    """
    fig, ax = plt.subplots()
    g = sns.barplot(x=x, y=y, data=dataframe, hue=hue, ax=ax)
    plt.title(title)
    plt.xticks(rotation=45, horizontalalignment="right")
    if save:
        plt.savefig(f"{out_path}/bar_plot.png", dpi=300)
    return fig

def bike_v2_data_loader(file: str, i: int, pattern: str) -> pd.DataFrame:
    """
    Formats the new dynamic bike output files into standard dataframes

    input
    -----
    file: location and filename of the file
    i: subject number

    output
    ------
    temp_df: preformatted and astyped dataframe
    """
    import re
    import streamlit as st

    # extract filename from location
    if ("/" in file) or ("\\" in file):
        filename = file.replace("\\", "/").split("/")[-1]
    else:
        filename = file
    # read in file
    temp_df = pd.read_csv(file, skiprows=1, delimiter=",?\s\s+", engine="python")
    # columns in all lowercase, and using _ instead of space
    temp_df.columns = [
        col.lower().replace("(", "_").replace(")", "").replace(" ", "_")
        for col in temp_df.columns
    ]

    # remove spaces from the timer column
    temp_df["timer"] = temp_df["timer"].str.replace(" ", "")

    # extract date from filename, then create datetime column
    temp_df["date"] = (
        re.findall("(\d\d_\d\d_\d\d\d\d)", filename)[0].replace("_", "/")
        + " "
        + temp_df["time_s"]
    )
    temp_df["date"] = pd.to_datetime(temp_df["date"])

    # in seconds, because timedelta might be more dificult to calculate from
    temp_df["seconds_elapsed"] = pd.to_timedelta(temp_df["timer"]).apply(lambda x: x.total_seconds())
    # define data types for each column
    temp_df = temp_df.astype(
        {"speed_rpm": float, "power_w": float, "heart_beat": float}
    )
    # extract sess, assumed to be at end of the filename
    check_file_format(filename)
    participant, session = get_idsess_from_bike_v2(filename, pattern)
    temp_df["session"] = session
    temp_df["participant"] = participant

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
        ]
    ]
    # rename some columns
    temp_df = temp_df.rename(
        {"power_w": "power_watt", "heart_beat": "heart_rate"}, axis=1
    )

    temp_df["id_sess"] = temp_df["participant"] + "_" + temp_df["session"]

    return temp_df

def bike_v3_data_loader(file: str, i: int, pattern: str) -> pd.DataFrame:
    """
    Formats the dynamic bike v3 output files into standard dataframes

    input
    -----
    file: location and filename of the file
    i: subject number

    output
    ------
    temp_df: preformatted and astyped dataframe
    """
    import re
    # extract filename from location, used to get the participant ID and date
    if ("/" in file) or ("\\" in file):
        filename = file.replace("\\", "/").split("/")[-1]
    else:
        filename = file

    # extract participant id from the filename
    participant_id = filename.split("_")[0]
    session_id = filename.split("_")[1]
 
    temp_df = pd.read_csv(file, header=1)

    temp_df['participant'] = participant_id
    temp_df['session'] = session_id

    temp_df.columns = [col.strip() for col in temp_df.columns]
    temp_df = temp_df.rename({
        'Time': 'time',
        'Session Timer': 'session_timer',
        'Interval Timer': 'interval_timer',
        'Speed(RPM)': 'speed_rpm',
        'Power(W)': 'power_watt',
        'Heart Beat': 'heart_rate',
        'Stiffness': 'stiffness',
        'Speed Set': 'speed_set'
    }, axis=1)
    # extract date from the filename, then append the time column
    temp_df["date"] = (
        re.findall("(\d\d_\d\d_\d\d\d\d)", file)[0].replace("_", "/")
        + " "
        + temp_df["time"]
    ).astype('datetime64[ns]')

    # get the seconds elapsed for each interval
    for timer_type in ['session', 'interval']:
        temp_df[f'seconds_elapsed_{timer_type}'] = pd.to_timedelta(temp_df[f'{timer_type}_timer']).dt.total_seconds()
    
    temp_df["id_sess"] = temp_df["participant"] + "_" + temp_df["session"]

    return temp_df

def check_if_file_exists(file_loc: str) -> bool:
    '''
    Checks whether the given file exists in the given location. This is to make
    sure the user copied MatLab files in the correct place.

    file_loc should include filename
    '''
    from os.path import exists
    file_exists = exists(file_loc)
    return file_exists

def check_matlab_file_loc():
    import streamlit as st
    import os

    filedir = os.getcwd().split('/src')[0].replace('\src','')
    file_exist_dict = {}
    for filename in ['entropy_script.m', 'ApSamEn.m', 'Convert_Data.m', 'MatchCounter.c']:
        if filename == 'entropy_script.m':
            file_loc = f'{filedir}/{filename}'
        else:
            file_loc = f'{filedir}/src/matlab/{filename}'
        file_exist_dict[filename] = check_if_file_exists(file_loc)
    
    num_not_exist = 0
    for filename, exists in file_exist_dict.items():
        if not exists:
            if filename == 'entropy_script.m':
                st.warning(f"__WARNING__: `{filename}` was not found in the `{filedir}` folder")
            else:
                st.warning(f"__WARNING__: `{filename}` was not found in the `{filedir}\matlab` folder")
            num_not_exist += 1
    if num_not_exist:
        st.info("__INFO__: The MatLab script assumes each of the above files are in the given location. Move them there before double clicking on `entropy_script.m`. These are not included with this script, but Dr. Ridgel has them.")

def check_file_format(filename:str) -> None:
    '''
    Checks whether files have been named using the convention
    `partID_sessID`
    '''
    import streamlit as st
    if (filename.count('_') != 7):
        st.warning(f'Was the file "{filename}" renamed per convention? There should be exactly 7 "\_" in the filename')