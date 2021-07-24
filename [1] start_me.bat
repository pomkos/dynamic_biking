:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF

:: Grab user name from new_bike.config
findstr /V "#" new_bike.config >new_bike.tmpcfg
set /p user= < new_bike.tmpcfg
del new_bike.tmpcfg

:: Run anaconda 
CALL C:\Users\%user%\anaconda3\Scripts\activate.bat C:\Users\%user%\anaconda3

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