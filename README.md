# Background

This repo was created to share the code used to create the entropy analysis workflow. Features include:

* Webgui using the [streamlit](https://streamlit.io) library
* Extraction of settings used per participant and session
* Interactive clipping of datasets of dramatic jumps in cadence
* Conversion of dynamic files to be used with the MatLab entropy scripts

# Instructions

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
1. Edit `start_me.bat` to reflect location of miniconda, usually in the home directory. Line 7 should look like:

```
CALL C:\Users\<USERNAME>\miniconda3\Scripts\activate.bat C:\Users\<USERNAME>\miniconda3
```
3. Clone repo, install python, install pip libraries

```
git clone https://github.com/pomkos/dynamic_biking
cd dynamic_biking

conda install python=3.8
pip install -r requirements.txt
```

4. Launch script by double clicking on `start_me.bat`

# MatLab script

The scripts used in MatLab for ApEn, SamEn, SpecEn analysis require the MinGW compiler. This requires logging into MatLab using an account.

1. Open MatLab
2. Click `APPS` tab
3. Click `Get More Apps`
4. In the search box click `Clear Filters` and then search for MinGW
5. Click `MATLAB Support for MinGW-w64 C/C++ Compiler` in the results
6. Click `Install`

# Notes

This repo does not contain the MatLab scripts required for ApEn, SamEn, and SpecEn analysis of dynamic bike cadence. The scripts contained in this repo are self contained, but the MatLab scripts must be moved to the `dynamic_biking` folder before entropy analysis can proceed. 
