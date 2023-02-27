'''
Allows the user to select specific participants and sessions with to format
for the MatLab entropy script. 
'''
from helpers import helper_functions as h  # brains behind the operation
import pandas as pd  # dataframe manipulation
import streamlit as st  # GUI
import matplotlib.pyplot as plt  # save plot
import seaborn as sns  # create plot
from stqdm import stqdm  # progress bar


def save_as_files(dataframe: pd.DataFrame, out_path, save_form) -> None:
    """
    Save all unique participants (code) as a separate xlsx file,
    formatted for MatLab.
    """
    import datetime as dt

    p_sess = list(dataframe["id_sess"].unique())
    num_sess = len(p_sess)
    dataframe["date_"] = dataframe["date"].apply(lambda x: x.date())
    for i in stqdm(range(num_sess)):
        p = p_sess[i]
        temp_df = dataframe[(dataframe["id_sess"] == p)]
        temp_df = temp_df[
            ["date", "heart_rate", "speed_rpm", "power_watt", "id_sess"]
        ]  # select approp cols, order for Matlab
        temp_df.columns = [
            "Date",
            "HR",
            "Cadence",
            "Power",
            "ID",
        ]  # format col name for Matlab
        try:
            h.save_dataset(temp_df, f"{out_path}/{p}")
        except PermissionError as p_error:
            st.error(f"Can't save the file, is `{p}`.xlsx open somewhere?")
            st.stop()


def facet_grid(x, y, title, dataframe, out_path, hue=None, reverse=False, save=False):
    """
    Returns a figure for streamlit. Creates facet grid
    using participant and session columns
    """
    if reverse:
        row = "session"
        col = "participant"
    else:
        row = "participant"
        col = "session"
    st.write(f"__NOTE:__ Columns are {col} and rows {row} IDs")
    g = sns.relplot(
        x=x, y=y, data=dataframe, row=row, col=col, facet_kws={"sharex": False}
    )
    g.fig.suptitle(title, y=1)
    if save:
        g.savefig(f"{out_path}/facet_grid.png", dpi=300)
    return g


@st.cache(suppress_st_warning=True)
def load_dataframe(file_locs, pattern):
    """
    This function is cached so the dataset won't be reloaded on each run of the script
    """
    # import and format each bike dataframe
    dataframe = pd.DataFrame()
    for i in range(len(file_locs)):
        temp_df = h.bike_v2_data_loader(file_locs[i], i + 1, pattern)
        dataframe = pd.concat([dataframe, temp_df])
    return dataframe


@st.cache()
def cut_dataframe(dataframe, start, end):
    """
    This function is cached so the dataset won't be recut each time a button is pressed
    """
    if (start == 0) and (end == 0):
        new_df = dataframe.copy()
        return new_df

    if end == 0:
        end = len(dataframe)
    
    new_df = dataframe[(dataframe["seconds_elapsed"] >= start) & (dataframe["seconds_elapsed"] <= end)]
    return new_df


def app(file_locs, pattern, in_path, out_path):
    # all_filenames = h.get_filename(file_locs)
    st.info('__Step 2b is optional__, it is for if one session needs more custom modification than others.')

    st.write('''
This step is optional. It is the same as Step 2a, except it lets the user edit one session at a time.

1. Select the session that needs to be clipped
2. Use the sidebar to indicate where to clip the graph
3. Once satisfied, click `Save` at the bottom of the page
4. The file will be saved in the `output` folder, overwriting any existing file of the same name. 
    ''')
    st.subheader("Individual edit")


    df = load_dataframe(file_locs, pattern)  # run once
    st.sidebar.write("--------------------")
    
    participants = list(df['participant'].unique())
    participants.sort()
    sessions = list(df['session'].unique())
    sessions.sort()

    col1, col2 = st.columns(2)
    with col1:
        participant = st.selectbox('Select the participant', participants)
    with col2: 
        session = st.selectbox('Select the session', sessions)
    
    df = df[(df['participant'] == participant) & (df['session'] == session)]
    start = st.sidebar.number_input("Start (minute)", min_value=0.0, step=1.0)
    end = st.sidebar.number_input("End (minute)", min_value=0.0, step=1.0)
    st.sidebar.info(
        "Modify the dataset to eliminate sudden jumps at the beginning or end of the graphs"
    )
    

    new_df = cut_dataframe(
        df, start, end
    ).copy()  # run if the start/end values are changed
    reverse = st.checkbox("Columns as participants")
    with st.spinner("Loading plot"):
        plot = facet_grid(
            x="seconds_elapsed",
            y="speed_rpm",
            dataframe=new_df,  # run if parameters are changed
            out_path=out_path,
            title="Cadence over time",
            reverse=reverse,
        )
        st.pyplot(plot.fig)

    with st.expander("Show current session's dataset"):
        st.info(
            f"This is a preview of participant {participant}, session {session}"
        )
        preview = new_df.head()
        st.write(preview)

    with st.form("save_results"):
        st.subheader("What should be saved?")
        save_plot = st.checkbox("The plot as it looks now")
        save_matlab = st.checkbox(
            "This session formatted for MatLab (required for MatLab entropy script)",
            value=True,
        )

        save_us = st.form_submit_button("Save")
        save_form = st.empty()
        save_form.info("All selected items will be saved in the 'output' folder")

    if save_us:
        save_form.warning("Do not close browser until successful save")
        if save_plot:
            facet_grid(
                x="seconds_elapsed",
                y="speed_rpm",
                dataframe=new_df,  # run if parameters are changed
                out_path=out_path,
                title="Cadence over time",
                reverse=reverse,
                save=True,
            )
 
        if save_matlab:
            save_as_files(new_df, out_path, save_form)
        save_form.success(f"Saved as __{participant}_{session}.xlsx__ in the output folder!")
