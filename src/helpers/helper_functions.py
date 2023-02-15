import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import re
from typing import List


def get_idsess(filename: str, pattern: str):
    """
    Returns a list of filenames, extract from string of location
    """
    import re
    import streamlit as st

    # filenames = []
    # nolabels = []
    # for file in file_locs:
    #     if ("/" in file) or ("\\" in file):
    #         filename = file.replace("\\", "/").split("/")[-1].lower()
    #         newname = re.findall('\d{2}_\d{2}_\d{2}_([a-z].+)\.txt$',filename)[0] # extract everything between the time and .txt
    #         newname = newname.replace('dynamic','').replace('static','').strip('_') # remove dynamic and static
    #         if len(newname) == 0: # if regex didn't find a label, the file was named incorrectly
    #             nolabels.append(filename)
    #             # NEED TO NOTIFY USER AND STOP SCRIPT
    #         else:
    #             filenames.append(newname)
    #     else:
    #         filename = file
    #         filenames.append(file)
    # filenames.sort()
    if pattern:
        my_id = re.findall(f"({pattern['id']})", filename)[0]
        sess = re.findall(f"({pattern['sess']})", filename)[0]
        return my_id, sess
    else:
        my_id = filename.split("_")[-2].strip(".txt")
        sess = filename.split("_")[-1].strip(".txt")
        return my_id, sess


def save_dataset(dataframe, name, extension="xlsx"):
    """
    Function to standardize saving files
    """
    dataframe.to_excel(f"{name}.{extension}", index=False)


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

def check_file_format(filename:str) -> None:
    '''
    Checks whether files have been named using the convention
    `partID_sessID`
    '''
    import streamlit as st
    if (filename.count('_') != 7):
        st.warning(f'Was the file "{filename}" renamed per convention? There should be exactly 7 "\_" in the filename')

def bike_v2_file_formatter(file: str, i: int, pattern: str) -> pd.DataFrame:
    """
    Formats the new dynamic bike output files into standard dataframes

    input
    -----
    file: location and filename of the file
    i: subject number

    output
    ------
    temp_df: preformatted and astyped datafrane
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
    participant, session = get_idsess(filename, pattern)
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

class settingsFinder:
    def __init__(self, file_locations: List[str], pattern: str):
        """
        Finds the mode, stiffness, and speed settings of the bike. Call bike_v3_settings
        for the bike put into testing in 2023, and bike_v2_settings for the bike in
        previous years. Ask Dr. Ridgel for guidance as needed.

        Args:
            file_locations (List[str]): List of locations for each raw output of the bike
            pattern (str): Optional. regex pattern for the session/participant combo. Not used as of 8/3/2021
        """
        self.settings: List[str] = []
        self.sessions: List[str] = [] 
        self.participants: List[str] = []

        self.modes: List[str] = []
        self.stiffness: List[str] = []
        self.speeds: List[str] = []

        self.file_locations: List[str] = file_locations
        self.pattern: str = pattern
    
    def bike_v3_settings(self):
        """
        From each file extracts the session number, participant number, mode, stiffness, speed,
        used for the bikev3 only. This information is presented to the user for a brief summary.
        """
        file_locations = self.file_locations
        pattern = self.pattern

        for i in range(len(file_locations)):
            with open(file_locations[i]) as f:
                self.settings.append(f.readline().strip("\n").lower())
            filename = file_locations[i].replace("/", "\\").split("\\")[-1]

            part_id = filename.split('_')[0]
            sess_id = filename.split('_')[1]
            bike_mode = filename.split('_')[-1].strip('.txt')

            self.modes.append(bike_mode)
            self.participants.append(part_id)
            self.sessions.append(sess_id)
            
            df = pd.read_csv(file_locations[i])
            df.columns = [col.strip() for col in df.columns]

            st.error("Next step: get the stiffness and speed settings from new bike file")        

    def bike_v2_settings(self):
        """
        From each file extracts the session number, participant number, mode, stiffness, speed,
        used for the bikev2 only. This information is presented to the user for a brief summary.

        """
        file_locations = self.file_locations
        pattern = self.pattern
        for i in range(len(file_locations)):
            with open(file_locations[i]) as f:
                self.settings.append(f.readline().strip("\n").lower())
            filename = file_locations[i].replace("/", "\\").split("\\")[-1]
            part_id, sess_id = get_idsess(
                filename, pattern
            )  # grab ids with or without custom pattern
            self.participants.append(part_id)
            self.sessions.append(sess_id)

        for i in range(len(self.settings)):
            set = self.settings[i] # one setting line

            bike_mode = re.findall("([a-z]\w+)\s+mode", set)[0]
            self.modes.append(bike_mode)
            if 'dynamic' in set:
                setting_speed = re.findall("speed\s+=\s+(\d+)", set)[0]
                setting_stiffness = re.findall("stiffness\s+=\s+(\d+),", set)[0]
            else: # static mode does not have speed setting
                import numpy as np
                setting_speed = np.nan
                setting_stiffness = re.findall("stiffness\s+=\s+(\d+)", set)[0]
            self.speeds.append(setting_speed)
            self.stiffness.append(setting_stiffness)

    def assemble_settings_df(self, bike_version: int) -> pd.DataFrame:
        """
        Gathers the scraped info into one, neat, dataframe. For presentation to user.

        Returns:
            pd.DataFrame: dataframe with ["participant", "session", "id_sess", "mode", "stiffness", "speed"] columns
        """
        if bike_version == 2:
            self.bike_v2_settings()
        elif bike_version == 3:
            self.bike_v3_settings()
        else:
            raise ValueError(f"Expected bike version 2 or 3, got {bike_version}")

        settings_dict = {
            "participant": self.participants,
            "session": self.sessions,
            "mode": self.modes,
            "stiffness": self.stiffness,
            "speed": self.speeds,
        }
        st.write(settings_dict)
        settings_df = pd.DataFrame(settings_dict)

        settings_df = settings_df.astype(
            {
                "participant": "object",
                "session": "object",
                "mode": "object",
                "stiffness": float,
                "speed": float,
            }
        )
        settings_df["id_sess"] = settings_df["participant"] + "_" + settings_df["session"]
        settings_df = settings_df[
            ["participant", "session", "id_sess", "mode", "stiffness", "speed"]
        ]
        return settings_df


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
