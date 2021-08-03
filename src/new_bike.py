import glob  # Find files
import streamlit as st  # GUI
import os  # Get directory location

st.set_page_config(
    page_title="Dynamic Bike Script", page_icon=":bike:"
)  # Give website a title and icon
st.title("Dynamic Bike Script")  # Title on main page


def read_txt_as_str(filename: str) -> str:
    """
    Loads txt files, returns contents as string
    """
    contents = ""
    with open(
        f"{filename}.txt", "r"
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
        "Step 2: Formatting",
        "Step 3: MatLab",
        "Step 4: Graphing",
    ],
    index=0,
).lower()
input_place = st.empty()
# folder = st.text_input('paste location of files')

dir_path = os.path.dirname(os.path.realpath(__file__)).strip('src')
in_path = "..\\input"
out_path = "..\\output"
file_locs = glob.glob(
    f"{in_path}/*.txt", recursive=True
)  # Make a list of txt files in the folder and subfolders
# Just a basic readme, edit as needed

if "homepage" in get_info:
    input_place.empty()
    st.write(
        "Welcome to the Dynamic Bike Script :bike:! This script was created to make entropy analysis more accurate and less prone to human error."
    )
    homepage = read_txt_as_str("homepage")
    st.write(homepage)
    st.stop()

elif "matlab" in get_info:
    input_place.empty()
    st.write("## Running MatLab Script")
    st.write(
        f"""
    1. Open the `entropy_script.m` file
    1. Click the green `▶` "Run" button under "Editor" tab
    """
    )
    with st.beta_expander("Example of Step 2"):
        st.image("images/matlab_menu.png")
    matlab = read_txt_as_str("matlab_troubleshooting")

    st.write(matlab)

    st.write("""### ApSamEn not found in current folder
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
    
    with st.beta_expander("Error solution"):
        st.image("images/matlab_error.png")
    

    st.write(
        """## Retrieving Entropy Results
All entropy results are saved in the file defined in line 21 of the MatLab script, in the `output` folder
    """
    )
    st.stop()

elif "graphing" in get_info:
    input_place.empty()
    st.info(
        """
    Explore using the tools below or use SPSS or other software for graphing"""
    )
    ent_file = st.text_input("Entropy file name", value="entropies.xls")
    from helpers import entropy_eda

    entropy_eda.app(ent_file, out_path)

if len(file_locs) < 1:
    st.warning('No ".txt" files found. Make sure all files are in the input folder.')
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

elif "format" in get_info:
    from helpers import entropy_format

    entropy_format.app(file_locs, pattern=None, in_path=in_path, out_path=out_path)  # Load entropy_format
