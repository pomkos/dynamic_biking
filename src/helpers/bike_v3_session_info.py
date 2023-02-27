import streamlit as st
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
    st.write(file_locs)
    st.info('NOTE: filename expected format: "participant001_session001_date_time_type.txt"')
    file_locs = [file_locs[0]]
    df = h.bike_v3_data_loader(file_locs[0], i=1, pattern=pattern)

    sf = settingsFinder(file_locations=file_locs, pattern=pattern)
    settings = sf.assemble_settings_df(bike_version=3)

    st.info("to be implemented")
