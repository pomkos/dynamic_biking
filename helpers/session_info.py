from helpers import helper_functions as h    # brains behind the operation
import pandas as pd                          # dataframe manipulation
import streamlit as st                       # GUI
import matplotlib.pyplot as plt              # plot labeling

def app(file_locs):
    settings = h.settings_finder(file_locs)
    # import and format each bike dataframe
    df = pd.DataFrame()
    df_length = pd.DataFrame()
    for i in range(len(file_locs)):
        temp_df = h.file_formatter(file_locs[i], i+1)
        time_diff = round((temp_df.iloc[-1,2] - temp_df.iloc[0,2]).seconds/60,2)
        df_length = df_length.append(pd.DataFrame({
            'participant':[temp_df['participant'].unique()[0]],
            'session':[temp_df['session'].unique()[0]],
            'length_minutes':[time_diff]
        }), ignore_index=True)
        df = df.append(temp_df)
    df_info = settings.merge(df_length, on=['participant','session'])

    st.info(""" The table includes some basic information about sessions, including:
    * Settings used
    * Total time for each session
    """)
    st.write(df_info)
    plot = h.bar_plot('participant','length_minutes', dataframe=df_info , title= 'Average length of sessions per participant')
    plt.xlabel('Participant Code')
    plt.ylabel('Minutes')
    st.pyplot(plot)
    save_form = st.form('save_all')

    with save_form:
        st.subheader("What should be saved?")
        save_df_info = st.checkbox('The table as an excel file')
        save_plot = st.checkbox('The plot as it looks now')
        save = st.form_submit_button('Save')
        save_form = st.empty()
        save_form.info("All selected items will be saved in the 'output' folder")

    if save:
        if save_df_info:
            h.save_dataset(df_info, 'session_info')
        if save_plot:
            h.bar_plot('participant','length_minutes', dataframe=df_info , title= 'Length of each session', save=True)
        save_form.success('Saved!')