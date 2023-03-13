import re
import pandas as pd
import numpy as np # for nan
import streamlit as st

from typing import List
from helpers.helper_functions import bike_v2_data_loader, bike_v3_data_loader, get_idsess_from_bike_v2

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
    
    def bike_v3_settings(self, all_participants_sessions_df):
        """
        From each file extracts the session number, participant number, mode, stiffness, speed,
        used for the bikev3 only. This information is presented to the user for a brief summary.
        """
        file_locations = self.file_locations
        pattern = self.pattern

        session_info_df = pd.DataFrame(columns=['participant', 'session', 'id_sess', 'mode', 'stiffness', 'speed_set', 'speed_avg', 'length_minutes'])

        for id_sess in all_participants_sessions_df['id_sess'].unique():
            temp_df = all_participants_sessions_df[all_participants_sessions_df['id_sess']==id_sess]
            id_sess_data = {}
            for col in ['participant', 'session', 'id_sess', 'mode']:
                id_sess_data[col] = temp_df[col].unique()[0]

            if id_sess_data['mode'].lower() == 'dynamic':
                grpd_object = temp_df.groupby(['stiffness', 'speed_set'])
            else:
                grpd_object = temp_df.groupby(['stiffness'])

            speed_settings = grpd_object[['speed_rpm']].mean().reset_index()
            speed_settings['length_minutes'] = grpd_object.size().reset_index()[0]/60

            speed_settings['length_minutes'] = speed_settings['length_minutes'].round(2)
            speed_settings['participant'] = id_sess_data['participant']
            speed_settings['session'] = id_sess_data['session']
            speed_settings['mode'] = id_sess_data['mode']

            speed_settings = speed_settings.rename({'speed_rpm': 'speed_avg'}, axis=1)


            session_info_df = pd.concat([session_info_df, speed_settings])

        return session_info_df

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
            part_id, sess_id = get_idsess_from_bike_v2(
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
        # run the appropriate settings extractors
        if bike_version == 2:
            self.bike_v2_settings()
            # format the settings into a dataframe
            settings_dict = {
                "participant": self.participants,
                "session": self.sessions,
                "mode": self.modes,
                "stiffness": self.stiffness,
                "speed": self.speeds,
            }
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
        elif bike_version == 3:
            settings_df = self.bike_v3_settings()
        else:
            raise ValueError(f"Expected bike version 2 or 3, got {bike_version}")

        settings_df["id_sess"] = settings_df["participant"] + "_" + settings_df["session"]
        return settings_df