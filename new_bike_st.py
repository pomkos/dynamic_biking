import glob                                 # Find files
import streamlit as st                      # GUI
import os                                   # Get directory location

st.set_page_config(page_title='Dynamic Bike Script', page_icon=':bike:')                     # Give website a title and icon
st.title("Dynamic Bike Script")                                                              # Title on main page

get_info = st.sidebar.radio('What should we explore?',                                       # Options in the sidebar
                            options=['Homepage','Step 1: Overview', 'Step 2: Formatting', 'Step 3: MatLab'],
                            index=0).lower()
input_place = st.empty()
input_folder = input_place.text_input("Paste location of files, if not in input folder",              # Grab user input
                            value="input")
if not input_folder:
    st.stop()
dir_path = os.path.dirname(os.path.realpath(__file__))
out_path = dir_path + '\\output'
file_locs = glob.glob(f"{input_folder}/*.txt", recursive=True)                               # Make a list of txt files in the folder and subfolders
if len(file_locs) < 1:
    st.warning('No ".txt" files found. Is this the right folder?')
    st.stop()

# Just a basic readme, edit as needed
if 'homepage' in get_info:
    input_place.empty()
    st.write("Welcome to the Dynamic Bike Script :bike:! This script was created to make entropy analysis more accurate and less prone to human error.")
    st.write("""
    ### Prerequisites
    1. All bike files copied to this machine (input folder is a good location)
    1. Miniconda installed with:
        * Python 3.8
        * All libraries found in `requirements.txt`
    1. Line 7 of `start_me.bat` edited to reflect location of miniconda 

    ### How To

    #### Step 1: Overview
    This step initializes the `session_info.py` script. It will preview settings and length of each bike session, including as a bar graph.
    
    1. Review results
    1. Save dataframe as excel file (Required)
    1. Save bar plot (optional)

    #### Step 2: Formatting
    The purpose of this step is to get each bike session file ready for entropy analysis. Minor cleaning and column renaming is involved.

    1. Review results
    1. Edit `Start` and `End` in the sidebar as needed to minimize severe jumps in cadence until satisfied
    1. Save plot (optional)
    1. Save all sessions in one excel sheet (optional)
    1. Save all sessions in separate excel sheets (Required)

    #### Step 3: MatLab
    Some minor adjustments to the MatLab script may be required if the script is run on a new laptop or by a new user
    """)
elif 'overview' in get_info:
    from helpers import session_info
    session_info.app(file_locs)                                                              # Load session_info app

elif 'format' in get_info:
    from helpers import entropy_format
    entropy_format.app(file_locs)                                                            # Load entropy_format 

elif 'matlab' in get_info:
    input_place.empty()
    st.subheader('Editing MatLab Script')
    st.write(f"""
    1. Double click `apsamen_cleaned.m`
    1. Edit the file at:
        * Line 16: `'{dir_path}'`
        * Line 19: `'{out_path}'`
        * Line 21: output filename can be anything but must end in .xls (ex: `entropies.xls`)
    1. Click the "Run" button under "Editor" tab
        * In case of an error like below, click `add its folder to the MATLAB path` and run the script again
    """)
    st.code("""Building with 'MinGW64 Compiler (C)'.
MEX completed successfully.
'ApSamEn' is not found in the current folder or on the MATLAB path, but exists in:
    [FOLDER LOCATION]

Change the MATLAB current folder or add its folder to the MATLAB path.

Error in apsamen_cleaned (line 61)
         [ap(n,num),  sam(n,num)]  = ApSamEn(data1(N1:N2,num),2,0.2*std1(num),n);
    """, language="matlab")
    st.write("""
    """)
    st.subheader("Retrieving Entropy Results")
    st.write("All entropy results are saved in the file defined in line 21 of the MatLab script, in the `output` folder")