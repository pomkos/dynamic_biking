import re
import pandas as pd
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
    
    def bike_v3_settings(self):
        """
        From each file extracts the session number, participant number, mode, stiffness, speed,
        used for the bikev3 only. This information is presented to the user for a brief summary.
        """
        file_locations = self.file_locations
        pattern = self.pattern

        session_info_df = pd.DataFrame(columns=['participant', 'session', 'id_sess', 'mode', 'stiffness', 'speed_set', 'speed_avg', 'length_minutes'])

        for i in range(len(file_locations)):
            with open(file_locations[i]) as f:
                self.settings.append(f.readline().strip("\n").lower())
            filename = file_locations[i].replace("/", "\\").split("\\")[-1]

            part_id = filename.split('_')[0]
            sess_id = filename.split('_')[1]
            # this is done within the fully assembled settings dataframe
            id_sess = part_id + '_' + sess_id
            bike_mode = filename.split('_')[-1].strip('.txt')

            self.modes.append(bike_mode)
            self.participants.append(part_id)
            self.sessions.append(sess_id)
            
            temp_df = bike_v3_data_loader(file_locations[i], i=i, pattern=None)
            speed_settings = temp_df.groupby(['stiffness', 'speed_set'])[['speed_rpm','interval_timer']].mean()
            speed_settings['participant'] = part_id
            speed_settings['session'] = sess_id
            speed_settings['mode'] = bike_mode
            speed_settings = speed_settings.reset_index().rename({'interval_timer': 'length_minutes'}, axis=1)
            speed_settings = speed_settings.rename({'speed_rpm': 'speed_avg'}, axis=1)

            st.write(speed_settings)

            session_info_df = pd.concat([session_info_df, speed_settings])

        st.write(session_info_df)
        st.error("Next step: get the stiffness and speed settings from new bike file")
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
        settings_df = settings_df[
            ["participant", "session", "id_sess", "mode", "stiffness", "speed_avg"]
        ]

        return settings_df