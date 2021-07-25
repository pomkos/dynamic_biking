:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF
cd ./src

:: Grab user name from new_bike.config
set user=%username%
set conda=anaconda3

:: Run anaconda 
CALL C:\Users\%user%\%conda%\Scripts\activate.bat C:\Users\%user%\%conda%

echo.
echo "-------------------------------------"
echo "Starting the dynamic bike script"
echo.
echo "Keep this window open while the script is running"
echo "-------------------------------------"

:: This line just runs the streamlit script ::
streamlit run new_bike.py

:: Keep the terminal open ::
PAUSE