# Background

This repo was created to share the code used to create the entropy analysis workflow. Features include:

* Webgui using the [streamlit](https://streamlit.io) library
* Extraction of settings used per participant and session
* Interactive clipping of datasets of dramatic jumps in cadence
* Conversion of dynamic files to be used with the MatLab entropy scripts

Screenshot of the first page with general instructions for each step.

![image](https://github.com/pomkos/dynamic_biking/raw/main/Screen%20Shot%202021-07-27%20at%2010.04.26.png)

# Instructions

1. Run `install.bat` and follow instructions to install miniconda and visual studio code, then the pip libraries
2. Launch script by double clicking on `start_me.bat`
3. All dynamic bike files should be placed in `input` folder
4. `Step 1`: Click save at the bottom of the page
5. `Step 2`: Clip files as needed, then click save at the bottom of the page
6. `Step 3`: Follow instructions to edit and run MatLab script
7. `Step 4`: Basic data exploration, optional

# MatLab script

The scripts used in MatLab for ApEn, SamEn, SpecEn analysis require the MinGW compiler (all entropy analysis) and the Signal Processing Toolbox (SpecEn analysis only). This requires logging into MatLab using an account.

## MinGW compiler

1. Open MatLab
2. Click `APPS` tab
3. Click `Get More Apps`
4. In the search box click `Clear Filters` and then search for MinGW
5. Click `MATLAB Support for MinGW-w64 C/C++ Compiler` in the results
6. Click `Install`

## Signal processing toolbox

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

1. `Lines 67 - 71`: add `%`

__Prevent the script from looking for SpecEn columns:__

1. `Line 73`: replace `cell(1,18);` with `cell(1,15);`
2. Delete entire `Lines 81, 86, 91` that end with `spec(number);`
3. Renumber `Lines 74 - end` so that `res_day1{1,num}` are sequential each line

Run the script and it should work without the need for Signal Processing Toolbox, with the tradeoff that SpecEn will not be calculated

# Notes

This repo does not contain the MatLab scripts required for ApEn, SamEn, and SpecEn analysis of dynamic bike cadence. The scripts contained in this repo are self contained, but all MatLab scripts must be moved to the `dynamic_biking/src/matlab` folder, with the exception of `entropy_script.m` that should be moved to the `dynamic_biking` folder, before entropy analysis can proceed. 

# Expected file layout

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
