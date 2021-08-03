import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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


def file_formatter(file: str, i: int, pattern: str) -> pd.DataFrame:
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
    # remove spaces from the timer columb
    temp_df["timer"] = temp_df["timer"].str.replace(" ", "")

    # extract date from filename, then create datetime column
    temp_df["date"] = (
        re.findall("(\d\d_\d\d_\d\d\d\d)", filename)[0].replace("_", "/")
        + " "
        + temp_df["time_s"]
    )
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    # format timer column as timedelta
    temp_df["timer"] = pd.to_timedelta(temp_df["timer"])
    # in seconds, because timedelta might be more dificult to calculate from
    temp_df["seconds_elapsed"] = temp_df["timer"].apply(lambda x: x.total_seconds())
    # define data types for each column
    temp_df = temp_df.astype(
        {"speed_rpm": float, "power_w": float, "heart_beat": float}
    )

    # extract sess, assumed to be at end of the filename
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

    temp_df["part_sess"] = temp_df["participant"] + "_" + temp_df["session"]
    return temp_df


def settings_finder(my_list: list, pattern: str) -> pd.DataFrame:
    """
    Finds the mode, stiffness, and speed settings of the bike

    input
    -----
    list: List of file locations, will be put into sess_finder function
    pattern: placeholder, for user to provide ID pattern. Not used as of 8/3/2021

    output
    ------
    settings_df: dataframe with 'sess', 'mode', 'stiffness', and 'speed' columns
    """
    import re

    settings = []
    sess = []
    parts = []
    import streamlit as st

    for i in range(len(my_list)):
        with open(my_list[i]) as f:
            settings.append(f.readline().strip("\n").lower())
        filename = my_list[i].replace("/", "\\").split("\\")[-1]
        part_id, sess_id = get_idsess(
            filename, pattern
        )  # grab ids with or without custom pattern
        parts.append(part_id)
        sess.append(sess_id)

    modes = []
    stiffs = []
    speeds = []

    for i in range(len(settings)):
        set = settings[i] # one setting line

        bike_mode = re.findall("([a-z]\w+)\s+mode", set)[0]
        setting_stiffness = re.findall("stiffness\s+=\s+(\d+),", set)[0]
        modes.append(bike_mode)
        stiffs.append(setting_stiffness)
        if 'dynamic' in set:
            setting_speed = re.findall("speed\s+=\s+(\d+)", set)[0]
        else: # static does not have speed setting
            import numpy as np
            setting_speed = np.nan       
        speeds.append(setting_speed)
    settings_df = pd.DataFrame(
        {
            "participant": parts,
            "session": sess,
            "mode": modes,
            "stiffness": stiffs,
            "speed": speeds,
        }
    )

    settings_df = settings_df.astype(
        {
            "participant": "object",
            "session": "object",
            "mode": "object",
            "stiffness": float,
            "speed": float,
        }
    )
    settings_df["part_sess"] = settings_df["participant"] + "_" + settings_df["session"]
    settings_df = settings_df[
        ["participant", "session", "part_sess", "mode", "stiffness", "speed"]
    ]

    return settings_df
