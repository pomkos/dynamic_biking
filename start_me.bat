:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF

:: EDIT ME ::
:: Edit the below line to add windows username, without quotes ::
SET user=albei

:: 
CALL C:\Users\%user%\anaconda3\Scripts\activate.bat C:\Users\%user%\anaconda3

echo.
echo "-------------------------------------"
echo "Starting the dynamic bike script"
echo.
echo "Keep this window open while the script is running"
echo "-------------------------------------"

:: This line just runs the streamlit script ::
streamlit run new_bike_st.py

:: Keep the terminal open ::
PAUSE