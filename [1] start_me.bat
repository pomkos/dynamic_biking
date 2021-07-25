:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF
cd ./src

:: Grab user name from new_bike.config

:: Run conda
IF EXIST %USERPROFILE%\anaconda3\ (
    set conda=anaconda3
)
IF EXIST %USERPROFILE%\miniconda3\ (
    set conda=miniconda3
)
ECHO %conda%

CALL %USERPROFILE%\%conda%\Scripts\activate.bat %USERPROFILE%\%conda%

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