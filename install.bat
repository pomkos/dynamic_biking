:: This file installs or reinstalls the required python libraries for dynamic bike script to run
:: Assumes miniconda has been installed already
:: To install miniconda: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

@ECHO OFF

:: EDIT ME ::
:: Edit the below line to point to the anaconda directory as demonstrated below ::
CALL C:\Users\albei\anaconda3\Scripts\activate.bat C:\Users\albei\anaconda3

:: This line installs everything in the requirements.txt file ::
pip install -r requirements.txt --upgrade

echo ''
echo "-------------------------------------"
echo "Required libraries installed. Close the window and open start_me.bat file"
echo "-------------------------------------"
echo ''

:: This line keeps the terminal open ::
PAUSE