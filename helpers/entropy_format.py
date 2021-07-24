from helpers import helper_functions as h    # brains behind the operation
import pandas as pd                          # dataframe manipulation
import streamlit as st                       # GUI
import matplotlib.pyplot as plt              # save plot
import seaborn as sns                        # create plot
from stqdm import stqdm                      # progress bar

def save_as_files(dataframe: pd.DataFrame, save_form) -> None:
    '''
    Save all unique participants (code) as a separate xlsx file,
    formatted for MatLab.
    '''
    import datetime as dt
    p_sess = list(dataframe['part_sess'].unique())
    num_sess = len(p_sess)
    dataframe['date_'] = dataframe['date'].apply(lambda x: x.date())
    for i in stqdm(range(num_sess)):
        p = p_sess[i]
        temp_df = dataframe[(dataframe['part_sess'] == p)]
        temp_df = temp_df[['date','heart_rate', 'speed_rpm','power_watt','part_sess']] # select approp cols, order for Matlab
        temp_df.columns = ['Date','HR','Cadence','Power','ID'] # format col name for Matlab
        h.save_dataset(temp_df,f"output/{p}")

def facet_grid(x,y,title, dataframe, hue=None, reverse=False, save=False):
    '''
    Returns a figure for streamlit. Creates facet grid
    using participant and session columns
    '''
    if reverse:
        row = 'session'
        col = 'participant'
    else:
        row = 'participant'
        col = 'session'
    g = sns.relplot(x=x,y=y, data=dataframe, row=row, col=col, facet_kws={'sharex':False})
    g.fig.suptitle(title,y=1)
    if save:
        g.savefig('output/facet_grid.png', dpi=300)
    return g

@st.cache()
def load_dataframe(file_locs):
    '''
    This function is cached so the dataset won't be reloaded on each run of the script
    '''
    # import and format each bike dataframe
    dataframe = pd.DataFrame()
    for i in range(len(file_locs)):
        temp_df = h.file_formatter(file_locs[i], i+1)
        dataframe = dataframe.append(temp_df)
    return dataframe

@st.cache()
def cut_dataframe(dataframe, start, end):
    '''
    This function is cached so the dataset won't be recut each time a button is pressed
    '''
    if start > 0:
        new_df = dataframe[(dataframe['seconds_elapsed'] >= start)]
    if end > 0:
        new_df = dataframe[(dataframe['seconds_elapsed'] <= end)]
    if (start == 0) and (end == 0):
        new_df = dataframe.copy()
    return new_df

def get_filename(file_locs, pattern):
    '''
    Returns a list of filenames, extract from string of location
    '''
    import re
    stripped = [loc.lower().split('dynamic') for loc in file_locs if 'dynamic' in loc]
    filenames = []
    nolabels = []
    for file in file_locs:
        if ("/" in file) or ("\\" in file):
            filename = file.replace("\\", "/").split("/")[-1].lower()
            newname = re.findall('\d{2}_\d{2}_\d{2}_([a-z].+)\.txt$',filename)[0] # extract everything between the time and .txt
            newname = newname.replace('dynamic','').replace('static','').strip('_') # remove dynamic and static
            if len(newname) == 0: # if regex didn't find a label, the file was named incorrectly
                nolabels.append(filename)
                # NEED TO NOTIFY USER AND STOP SCRIPT
            else:
                filenames.append(newname)
        else:
            filename = file
            filenames.append(file)
    filenames.sort()
    return filenames

def app(file_locs):
    from icecream import ic
    df = load_dataframe(file_locs) # run once
    pattern = st.text_input("What is the id pattern? (ex: `pdbike\d\d\d_session\d\d\d`, where \d represents a digit)")
    all_filenames = get_filename(file_locs,pattern)
    # st.write(all_filenames)
    # st.stop()
    st.sidebar.write('--------------------')
    start = st.sidebar.number_input("Start", min_value=0.0, step=1.0)
    end = st.sidebar.number_input("End", min_value=0.0, step=1.0)
    st.sidebar.info("Modify the dataset to eliminate sudden jumps at the beginning or end of the graphs")

    new_df = cut_dataframe(df, start, end).copy() # run if the start/end values are changed
    st.subheader("Are there any sudden jumps?")
    st.write("Prior to entropy analysis sudden jumps at the beginning and end of datasets should be removed. Use the 'start' and 'end' inputs in the sidebar to determine where to cut the datasets.")
    reverse = st.checkbox("Columns as participants")
    with st.spinner("Loading facet grid plot"):
        plot = facet_grid(x='seconds_elapsed',y='speed_rpm', dataframe=new_df ,   # run if parameters are changed
                        title= 'Cadence over time', reverse=reverse)
        st.pyplot(plot.fig)

    st.info("Some sessions may need different cuts. If this is the case, select the appropriate file(s) below. Otherwise select 'None'.")

    file_options = ['None'] + all_filenames
    details = st.multiselect("Select files that need more cuts", options=file_options, default='None')
    with st.beta_expander('Show current dataset'):
        st.info("This is a dataset of all files in one, save if you want all time series in one file.")
        save_new_df = st.checkbox("Save table")
        st.write(new_df)
        if save_new_df:
            h.save_dataset(new_df, 'all_in_one.xlsx')
    with st.form('save_results', clear_on_submit=True):
        st.subheader("What should be saved?")
        save_plot = st.checkbox("The plot as it looks now")
        save_all_in_one = st.checkbox("All sessions in one excel file")
        save_matlab = st.checkbox("All sessions formatted for MatLab (required for MatLab entropy script)", value=True)

        save_us = st.form_submit_button('Save')
        save_form = st.empty()
        save_form.info("All selected items will be saved in the 'output' folder")

    if save_us:
        save_form.warning("Do not close browser until successful save")
        if save_plot:
            facet_grid(x='seconds_elapsed',y='speed_rpm', dataframe=new_df ,   # run if parameters are changed
                    title= 'Cadence over time', reverse=reverse, save=True)
        if save_all_in_one:
            h.save_dataset(new_df, 'all_sessions')
        if save_matlab:
            save_as_files(new_df, save_form)
        save_form.success("Saved!")
