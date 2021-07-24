:: This batch file runs the streamlit app made for the dynamic bike ::
:: Last edited by:
::                 Peter Gates; July 18, 2021 ::

:: EDIT ME ::
:: Edit the below line to point to the anaconda directory as demonstrated below ::

CALL C:\Users\albei\anaconda3\Scripts\activate.bat C:\Users\albei\anaconda3

echo "Starting the dynamic bike script"

:: This line just runs the streamlit script ::
streamlit run new_bike_st.py

:: Keep the terminal open ::
PAUSE