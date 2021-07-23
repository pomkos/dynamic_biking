:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 18, 2021 ::

:: EDIT ME ::
:: Edit the below line to point to the anaconda directory as demonstrated below ::

if exists C:\Users\albei\miniconda3\ (
    loc = C:\Users\albei\miniconda3
) else (
    echo "Select the correct location, then replace the old one in start_me.bat with the new one" >"conda_location.txt"
    echo where conda >"conda_location.txt"
    echo "Please edit the start_me.bat file using the correct location from conda_location.txt"
    EXIT /B
)

echo "Activating miniconda"

CALL loc\Scripts\activate.bat loc

echo "Starting the dynamic bike script"

:: This line just runs the streamlit script ::
streamlit run new_bike_st.py

:: Keep the terminal open ::
PAUSE