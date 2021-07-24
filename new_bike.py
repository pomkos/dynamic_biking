import glob                                 # Find files
import streamlit as st                      # GUI
import os                                   # Get directory location

st.set_page_config(page_title='Dynamic Bike Script', page_icon=':bike:')                     # Give website a title and icon
st.title("Dynamic Bike Script")                                                              # Title on main page

def read_txt_as_str(filename: str) -> str:
    '''
    Loads txt files, returns contents as string
    '''
    contents = ''
    with open(f'{filename}.txt','r') as f: # so people can edit instructions without seeing code
        for line in f.readlines():
            # the "@" is reserved for commenting within the text file
            if line[0] != '@':
                contents += line
    return contents

# Create input/output folders
if not os.path.exists('input'):
    os.makedirs('input')
if not os.path.exists('output'):
    os.makedirs('output')

get_info = st.sidebar.radio('What should we explore?',                                       # Options in the sidebar
                            options=['Homepage','Step 1: Overview', 'Step 2: Formatting', 'Step 3: MatLab'],
                            index=0).lower()
input_place = st.empty()
# folder = st.text_input('paste location of files')
folder = 'input'

dir_path = os.path.dirname(os.path.realpath(__file__))
out_path = dir_path + '\\output'
file_locs = glob.glob(f"{folder}/*.txt", recursive=True)                               # Make a list of txt files in the folder and subfolders

# Just a basic readme, edit as needed
if 'homepage' in get_info:
    input_place.empty()
    st.write("Welcome to the Dynamic Bike Script :bike:! This script was created to make entropy analysis more accurate and less prone to human error.")
    homepage = read_txt_as_str('homepage')
    st.write(homepage)
    st.stop()
    
elif 'matlab' in get_info:
    input_place.empty()
    st.subheader('Editing MatLab Script')
    st.write(f"""
    1. Double click `entropy_script.m`
    1. Edit the file at:
        * Line 17: in quotes: `'{dir_path}'`
        * Line 19: in quotes: `'{out_path}'`
        * Line 22: output filename can be anything but must end in .xls (ex: in quotes: `entropies.xls`)
    1. Click the "Run" button under "Editor" tab
    """)
    matlab = read_txt_as_str('matlab_instructions')
    st.write(matlab)
    st.stop()

if len(file_locs) < 1:
    st.warning('No ".txt" files found.')
    st.stop()

if 'overview' in get_info:
    from helpers import session_info
    session_info.app(file_locs)                                                              # Load session_info app

elif 'format' in get_info:
    from helpers import entropy_format
    entropy_format.app(file_locs)                                                            # Load entropy_format 
