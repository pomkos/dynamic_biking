import pandas as pd
import glob  # Find files
import streamlit as st  # GUI
import os  # Get directory location
from helpers import helper_functions as h
from typing import List

st.set_page_config(
    page_title="Dynamic Bike Script", page_icon=":bike:"
)  # Give website a title and icon
st.title("Dynamic Bike File Processor")  # Title on main page

# h.check_matlab_file_loc()
st.warning("DEV MODE: skipped checking for MatLab files")

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

class gatherUserInfo:
    def __init__(self):
        """
        Initiates all user selected variables and starts the 'start' function,
        which will direct the user through the various functions.
        """
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
                "Step 4: Effort calculation",
                "Step 5: View results",
            ],
            index=0,
        ).lower()
        self.input_place = st.empty()
        # folder = st.text_input('paste location of files')

        dir_path = os.path.dirname(os.path.realpath(__file__)).strip('src')
        self.in_path = "../input"
        self.out_path = "../output"
        file_locs = glob.glob(
            f"{self.in_path}/*.txt", recursive=True
        )  # Make a list of txt files in the folder and subfolders
        # Just a basic readme, edit as needed
        
        self.start(file_locs=file_locs, get_info=get_info)

    def start(self, file_locs: List[str], get_info: str):
        if len(file_locs) < 1:
            st.warning('No ".txt" files found. Make sure all files are in the "input" folder, not a subdirectory.')
            st.stop()

        if "homepage" in get_info:
            self.input_place.empty()
            st.write(
                "Welcome to the Dynamic Bike Script :bike:! Follow the instructions to get dynamic bike output files ready for MatLab entropy analysis."
            )
            homepage = read_txt_as_str("homepage", 'txt')
            st.write(homepage)
            st.stop()
        bike_version = st.number_input('Bike Version', min_value=2, max_value=3, step=1)
        # STEP 1 #
        if "overview" in get_info:
            from helpers import bike_v2_session_info, bike_v3_session_info
            if bike_version == 2:
                st.info("For the dynamic bike used 2020-2023")
                bike_v2_session_info.app(file_locs, self.out_path, pattern=None)  # Load session_info app

            elif bike_version == 3:
                st.info("For the dynamic bike used 2023 onwards")
                bike_v3_session_info.app(file_locs, self.out_path, pattern=None)

        # STEP 2A #
        elif "sessions" in get_info:
            from helpers import entropy_format_all

            entropy_format_all.app(file_locs, pattern=None, bike_version=bike_version, in_path=self.in_path, out_path=self.out_path)  # Load entropy_format_all

        # STEP 3A #
        elif "participant" in get_info:
            from helpers import entropy_format_specific

            entropy_format_specific.app(file_locs, pattern=None, in_path=self.in_path, out_path=self.out_path) # Load entropy_format_specific

        # STEP 3 #
        elif "entropy" in get_info:
            self.start_step_3()

        # STEP 4 #
        elif "effort" in get_info:
             self.start_step_4()

        # STEP 5 #
        elif "result" in get_info:
             self.start_step_5()
        
    def start_step_3(self):
        self.input_place.empty()
        # give user warning if the matlab files are not found
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

    def start_step_4(self):
        from helpers import effort_calculator
        st.write("## Effort Calculator")
        st.info("Keep the files from Step 2 as well as the file created by the MatLab script in the `output` folder")
        filename = st.text_input("Entropy  file name", "entropies.xls")
        try:
            matlab_df = df = pd.read_excel(f"{self.out_path}/{filename}")
        except:
            st.error(f"{filename} not found in the output folder")
            st.stop()
        
        effort_df = effort_calculator.app(self.out_path)
        matlab_df_with_effort = matlab_df.merge(effort_df, how='left', on='ID')

        st.write(matlab_df_with_effort.head())

        with st.form('save_effort_df2'):
            st.info("The above preview of the entropy dataset now includes effort calculation as well")
    
            st.subheader("What should be saved?")
            save_df = st.checkbox("Save dataset with effort and entropy as one file", value=True)
            
            save_form = st.empty()
            save_form.info("All selected items will be saved in the 'output' folder")
            save_us = st.form_submit_button("Save")

        if save_us:
            save_form.warning("Do not close browser until successful save")
            if save_df:
                h.save_dataset(matlab_df_with_effort, f"{out_path}/entropy_effort", extension='xlsx')
            save_form.success("Saved!")
        else:
            st.stop()
    def start_step_5(self):

        self.input_place.empty()
        st.info(
            """
        Explore using the tools below or use SPSS or other software for graphing"""
        )
        ent_file = st.text_input("Entropy file name", value="entropy_effort.xlsx")
        from helpers import entropy_eda

        entropy_eda.app(ent_file, self.out_path)

if __name__ == "__main__":
    g = gatherUserInfo()
