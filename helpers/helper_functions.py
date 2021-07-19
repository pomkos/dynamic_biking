import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def save_dataset(dataframe, name):
    '''
    Function to standardize saving files
    '''
    dataframe.to_excel(f'{name}.xlsx', index=False)

def bar_plot(x, y, title, dataframe, hue=None, save=False):
    '''
    Function so streamlit can show it easier
    '''
    fig, ax = plt.subplots()
    g = sns.barplot(x=x, y=y, data=dataframe, hue = hue, ax=ax)
    plt.title(title)
    plt.xticks(rotation=45, horizontalalignment='right')
    if save:
        plt.savefig('output/bar_plot.png', dpi=300)
    return fig

def file_formatter(file: str, i: int) -> pd.DataFrame:
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
    temp_df["session"] = filename.split("_")[-1].strip(".txt").strip().lower()
    temp_df["participant"] = filename.split("_")[-2].strip().lower()

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
    
    temp_df['part_sess'] = temp_df['participant'] + '_' + temp_df['session']
    
    return temp_df


def sess_finder(my_list: list) -> list:
    """
    Extracts the settings and participant sess from loc/filename.csv, but
    assumes everything after last '_' is the participant sess.

    TEMP: numbers each sess

    input
    -----
    my_list: list
        List of file locations

    output
    ------
    settings: list
        list of items where each item is the first line of the dynamic bike output
    sess: list
        list of participant recordings
    part: list
        list of participant names
    """
    settings = []
    sess = []
    part = []
    for i in range(len(my_list)):
        with open(my_list[i]) as f:
            settings.append(f.readline().strip("\n").lower())
        part.append(my_list[i].split("_")[-2].lower())
        sess.append(my_list[i].split("_")[-1].strip(".txt").lower())
    return settings, sess, part


def settings_finder(my_list: list) -> pd.DataFrame:
    """
    Finds the mode, stiffness, and speed settings of the bike

    input
    -----
    list: List of file locations, will be put into sess_finder function

    output
    ------
    settings_df: dataframe with 'sess', 'mode', 'stiffness', and 'speed' columns
    """
    import re

    settings, sess, parts = sess_finder(my_list)

    modes = []
    stiffs = []
    speeds = []
    for i in range(len(settings)):
        modes.append(re.findall("([a-z]\w+)\s+mode", settings[i])[0])
        stiffs.append(re.findall("stiffness\s+=\s+(\d+),", settings[i])[0])
        speeds.append(re.findall("speed\s+=\s+(\d+)", settings[i])[0])

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
    settings_df['part_sess'] = settings_df['participant'] + '_' + settings_df['session']
    settings_df = settings_df[['participant','session','part_sess','mode','stiffness','speed']]

    return settings_df
