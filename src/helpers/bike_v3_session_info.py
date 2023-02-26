import streamlit as st
import pandas as pd

from helpers import helper_functions as h
from typing import List

def app(file_locs: List[str], out_path: str, pattern: str):
    st.write(file_locs)
    st.info('NOTE: filename expected format: "participant001_session001_date_time_type.txt"')
    file_locs = [file_locs[0]]
    df = h.bike_v3_file_formatter(file_locs[0], i=1, pattern=pattern)

    s = h.settingsFinder(file_locations=file_locs, pattern=pattern)
    settings = s.assemble_settings_df(bike_version=3)

    

    st.info("to be implemented")
    
