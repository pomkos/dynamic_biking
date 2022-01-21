Download [available here](https://github.com/pomkos/dynamic_biking/releases)

# Table of Contents

1. [Background](#background)
2. [Instructions](#instructions)
    1. [Use](#use)
    2. [Windows](#windows)
    3. [MacOS](#macos)
4. [MatLab Script Instructions](#matlab-script)
    1. [MinGW Addon](#mingw-addon)
    2. [Signal Processing Toolbox addon](#signal-processing-toolbox)
5. [Notes](#notes)
6. [Expected File Layout](#expected-file-layout)

# Background

This repo was created to share the code used to create the entropy analysis workflow. Features include:

* Bash script to install python library requirements for each script
* Bash script to start the main script webgui
* Webgui using the [streamlit](https://streamlit.io) library
* Extraction of settings used per participant and session
* Interactive clipping of datasets of dramatic jumps in cadence
* Conversion of dynamic files to be used with the MatLab entropy scripts
* Exploration of entropy results 

Screenshot of the first page with general instructions for each step.

![image](https://github.com/pomkos/dynamic_biking/raw/main/screenshot.png)

# Instructions


## Use

Basic overview of each step, for both Windows and MacOS:

1. `Step 1`: Click save at the bottom of the page
2. `Step 2a` and `Step 2b`: Clip files as needed, then click save at the bottom of the page
3. `Step 3`: Follow instructions to edit and run MatLab script
4. `Step 4`: Basic data exploration, optional

## Windows

### Install

1. Run `install.bat` and follow instructions to install miniconda and visual studio code, then the pip libraries
    1. Copy paste the first link (miniconda), and download Python 3.8
    2. Copy paste the second link (VScode), downloaded the latest version
    3. Close the black window (terminal)
    4. Double click on `install.bat` again
        1. Type `2`, enter
        2. Wait for installation to finish, message will say "Click startme.bat"

### Start
1. Launch script by double clicking on `start_me.bat`
    1. On first launch it will ask for email, you can press enter without typing anything. Won't be asked again afterwards
    2. It should open a browser window by itself, if it doesn't then copy and paste one of the two links shown. All dynamic bike files should be placed in `input` folder

## MacOS

### Install
1. Download and install miniconda, Python 3.8 version: 
    1. Macbook Pro/Macbook: [click here to download](https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-MacOSX-x86_64.pkg)
    2. Macbook M1: [click here to download](https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.1-MacOSX-arm64.sh)
    3. For both versions: once installation is finished, open the terminal and type in `conda init`. If successful, close the terminal. If an error is written, contact Peter
2. Download the latest version of the dynamic bike script, extract the folder to the Desktop
3. Open the Terminal, then copy paste the following and press enter:

```
cd ~/Desktop/dynamic_biking/src
yes | pip install -r requirements.txt
streamlit run new_bike.py
```

### Start

To start the script, open the terminal and copy-paste the following:

```
cd ~/Desktop/dynamic_biking/src
streamlit run new_bike.py
```

1. On first launch it will ask for email, you can press enter without typing anything. Won't be asked again afterwards
2. It should open a browser window by itself, if it doesn't then copy and paste one of the two links shown. All dynamic bike files should be placed in `input` folder

# MatLab Script

The scripts used in MatLab for ApEn, SamEn, SpecEn analysis require the MinGW compiler (all entropy analysis) and the Signal Processing Toolbox (SpecEn analysis only). This requires logging into MatLab using an account.

## MinGW Compiler

1. Open MatLab
2. Click `APPS` tab
3. Click `Get More Apps`
4. In the search box click `Clear Filters` and then search for MinGW
5. Click `MATLAB Support for MinGW-w64 C/C++ Compiler` in the results
6. Click `Install`

## Signal Processing Toolbox

1. Open MatLab
2. Click `APPS` tab
3. Click `Get More Apps`
4. In the search box click `Clear Filters` and then search for Signal Processing Toolbox
5. Click `Signal Processing Toolbox` in the results
6. Click `Install` (or `Trial`)

If SpecEn analysis is not needed, the Signal Processing Toolbox does not need to be installed. In that case the MatLab script needs to be modified:

__Prevent the script from creating SpecEn columns:__

1. `Line 27`: delete `spec_HR` but leave the `,...` at the end
2. `Line 28`: delete`spec_Cadence` but leave the `,...` at the end
3. `Line 29`: delete `spec_Power` but leave the `};` at the end

__Prevent the script from calculating SpecEn:__

1. `Lines 67 - 71`: add `%`at the beginning

__Prevent the script from looking for SpecEn columns:__

1. `Line 73`: replace `cell(1,18);` with `cell(1,15);`
2. Delete entire `Lines 81, 86, 91` that end with `spec(number);`
3. Renumber `Lines 74 - end` so that `res_day1{1,num}` are sequential each line

Run the script and it should work without the need for Signal Processing Toolbox, with the tradeoff that SpecEn will not be calculated

# Notes

This repo does not contain the MatLab scripts required for ApEn, SamEn, and SpecEn analysis of dynamic bike cadence. The scripts contained in this repo are self contained, but all MatLab scripts must be moved to the `dynamic_biking/src/matlab` folder, with the exception of `entropy_script.m` that should be moved to the `dynamic_biking` folder, before entropy analysis can proceed. 

# Expected File Layout

The dynamic bike scripts expect the following organization:

```
dynamic_biking                          # place entropy_script.m in here
    |-- .gitignore                      # list of file extensions that will not be uploaded to github
    |-- README.md                       # this readme file
    |-- [0] install.bat                 # run first, guides user through conda and pip installation
    |-- [1] start_me.bat                # runs the main script
    |-- entropy_script.m                # loops through bike files and uses matlab scripts to calculate entropies
    |-- src
        |-- homepage.txt                # edit to update instructions on the homepage
        |-- matlab_troubleshooting.txt  # edit to add solutions to problems encountered in matlab
        |-- new_bike.py                 # main script that runs each script as needed
        |-- requirements.txt            # contains libraries required by all scripts
        |-- helpers
            |-- entropy_eda.py          # script for step 4
            |-- entropy_format.py       # script for step 2
            |-- helper_functions.py     # contains various functions used by all steps
            |-- session_info.py         # script for step 1
        |-- images                      # contains screenshots used in step 3
            |-- matlab_code.png
            |-- matlab_error.png
            |-- matlab_menu.png
        |-- matlab                      # place all other matlab scripts in here
            |-- ApSamEn.m               # code for entropy calculation
            |-- Convert_Data.m          # not sure what this does
            |-- MatchCounter.c          # will create MatchCounter.mexw64 on each run
```
