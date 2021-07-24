# Background

This repo was created to share the code used to create the entropy analysis workflow. Features include:

* Webgui using the [streamlit](https://streamlit.io) library
* Extraction of settings used per participant and session
* Interactive clipping of datasets of dramatic jumps in cadence
* Conversion of dynamic files to be used with the MatLab entropy scripts

# Instructions

1. Run `install.bat` and follow instructions to install miniconda and visual studio code, then the pip libraries
2. Edit `start_me.bat` to reflect location of miniconda, usually in the home directory. Line 9 should look like:

```
SET user=albei
```

3. Launch script by double clicking on `start_me.bat`

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
