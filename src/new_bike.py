import glob  # Find files
import streamlit as st  # GUI
import os  # Get directory location
from helpers import helper_functions as h

st.set_page_config(
    page_title="Dynamic Bike Script", page_icon=":bike:"
)  # Give website a title and icon
st.title("Dynamic Bike Script")  # Title on main page

h.check_matlab_file_loc()

def read_txt_as_str(filename: str, extension: str) -> str:
    """
    Loads txt files, returns contents as string
    """
    if 'README' in filename:
        st.info("Entropy analysis requires the following two addons.")
        contents = ""
        f = open(f"{filename}.{extension}", "r")
        lines_to_read = [i for i in range(40, 78)]
        for position, line in enumerate(f):
            if position in lines_to_read:
                contents += line
        return contents
    else:
        contents = ""
        with open(
            f"{filename}.{extension}", "r"
        ) as f:  # so people can edit instructions without seeing code
            for line in f.readlines():
                # the "@" is reserved for commenting within the text file
                if line[0] != "@":
                    contents += line
        return contents


# Create input/output folders
if not os.path.exists("../input"):
    os.makedirs("../input")
if not os.path.exists("../output"):
    os.makedirs("../output")

get_info = st.sidebar.radio(
    "What should we explore?",  # Options in the sidebar
    options=[
        "Homepage",
        "Step 1: Overview",
        "Step 2a: Format all sessions",
        "Step 2b: Format per participant",
        "Step 3: Entropy calculation",
        "Step 4: View results",
    ],
    index=0,
).lower()
input_place = st.empty()
# folder = st.text_input('paste location of files')

dir_path = os.path.dirname(os.path.realpath(__file__)).strip('src')
in_path = "../input"
out_path = "../output"
file_locs = glob.glob(
    f"{in_path}/*.txt", recursive=True
)  # Make a list of txt files in the folder and subfolders
# Just a basic readme, edit as needed

if "homepage" in get_info:
    input_place.empty()
    st.write(
        "Welcome to the Dynamic Bike Script :bike:! Follow the instructions to get dynamic bike output files ready for MatLab entropy analysis."
    )
    homepage = read_txt_as_str("homepage", 'txt')
    st.write(homepage)
    st.stop()

elif "entropy" in get_info:
    input_place.empty()
    # give user warning if the matlab files are not found
    from helpers import helper_functions as h
    h.check_matlab_file_loc()
    st.write(
        f"""
    1. Double click the `entropy_script.m` file in the `dynamic_biking` folder
    1. Click the green `▶` "Run" button under "Editor" tab
    """
    )
    with st.expander("Demonstration", expanded=True):
        st.image("images/matlab_menu.png")

    st.write(
        """__Retrieving entropy results__

All entropy results are saved in the file defined in line 21 of the MatLab script, in the `output` folder
    """
    )
    st.write('---------------------------------------------------------')
    matlab = read_txt_as_str("matlab_troubleshooting",'txt')
    st.write('### Installation')
    with st.expander('MatLab Setup Instructions'):
        matlab_install = read_txt_as_str('../README','md')
        st.write(matlab_install)
    st.write(matlab)

    st.write("""#### ApSamEn not found in current folder
In case the error below appears, click `add its folder to the MATLAB path` and run the script again

```
Building with 'MinGW64 Compiler (C)'.
MEX completed successfully.
'ApSamEn' is not found in the current folder or on the MATLAB path, but exists in:
    [FOLDER LOCATION]

Change the MATLAB current folder or add its folder to the MATLAB path.

Error in apsamen_cleaned (line 61)
         [ap(n,num),  sam(n,num)]  = ApSamEn(data1(N1:N2,num),2,0.2*std1(num),n);
```
    """)
    
    with st.expander("Error solution"):
        st.image("images/matlab_error.png")
    
    st.stop()

elif "result" in get_info:
    input_place.empty()
    st.info(
        """
    Explore using the tools below or use SPSS or other software for graphing"""
    )
    ent_file = st.text_input("Entropy file name", value="entropies.xls")
    from helpers import entropy_eda

    entropy_eda.app(ent_file, out_path)

if len(file_locs) < 1:
    st.warning('No ".txt" files found. Make sure all files are in the "input" folder, not a subdirectory.')
    st.stop()

# Theres a bug where two forms cant be submitted
# # Ask user for id pattern
# if st.sidebar.checkbox('Use custom id pattern'):
#     with st.sidebar.form("submit_patterns"):
#         id_pattern = st.text_input("What is the id pattern? (ex: `pdbike\d\d`, where \d represents a digit)")
#         sess_pattern = st.text_input("What is the session pattern? (ex: `day\d\d`, where \d represents a digit)")
#         pattern={'id':id_pattern, 'sess':sess_pattern}
#         st.info("Required if participant IDs do not follow the recommended pattern of xxx000_yyy000")
#         if not st.form_submit_button():
#             st.stop()
# else:
#     pattern=None

if "overview" in get_info:
    from helpers import session_info

    session_info.app(file_locs, out_path, pattern=None,)  # Load session_info app

elif "sessions" in get_info:
    from helpers import entropy_format_all

    entropy_format_all.app(file_locs, pattern=None, in_path=in_path, out_path=out_path)  # Load entropy_format_all

elif "participant" in get_info:
    from helpers import entropy_format_specific

    entropy_format_specific.app(file_locs, pattern=None, in_path=in_path, out_path=out_path) # Load entropy_format_specific