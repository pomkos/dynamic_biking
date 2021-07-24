:: This file installs or reinstalls the required python libraries for dynamic bike script to run
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF

SET /p response="Which conda is installed? (anaconda/miniconda/neither): "
if %response%==anaconda GOTO conda
if %response%==miniconda GOTO mini
if %response%==neither GOTO instructions
:eof

:: ------------------------ INITIATION SECTION ------------------------ ::
:instructions
ECHO "Step 1. Install miniconda3 64bit from the opened link"
ECHO.
ECHO "The link didn't open? Copy paste into your browser: https://docs.conda.io/en/latest/miniconda.html"
ECHO "Close the browser to continue"
 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://docs.conda.io/en/latest/miniconda.html
ECHO.
ECHO "Step 2. Install visual studio code from the opened link"
ECHO.
ECHO "The link didn't open? Copy paste into your browser: https://code.visualstudio.com/Download"
ECHO "Close the browser to continue"
 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://code.visualstudio.com/Download
ECHO.
SET /p cntn="Step 3. Did miniconda and Visual Studio Code install? (Y/n): "
if %cntn%=="Y" GOTO mini else ECHO "Please contact technical support"
:eof
:end


:: ------------------------ ANACONDA SECTION ------------------------ ::
:conda
SET /p user="What is the windows username? "

:: EDIT ME ::
:: Edit the below line to point to the anaconda directory as demonstrated below ::
CALL C:\Users\%user%\anaconda3\Scripts\activate.bat C:\Users\%user%\anaconda3
:: This line installs everything in the requirements.txt file ::
pip install -r requirements.txt --upgrade

echo.
echo "-------------------------------------"
echo "Required libraries installed."
echo "-------------------------------------"
echo.
echo "Please open start_me.bat"
echo.
:: This line keeps the terminal open ::
PAUSE
:: This line exits the terminal
EXIT

:end

:: ------------------------ MINICONDA SECTION ------------------------ ::
:mini
SET /p user="What is the windows username? "
:: Store the username in new_bike.config
echo %user% > "new_bike.config"

CALL C:\Users\%user%\miniconda3\Scripts\activate.bat C:\Users\%user%\miniconda3
:: This line installs everything in the requirements.txt file ::
pip install -r requirements.txt --upgrade

echo.
echo "-------------------------------------"
echo "Required libraries installed."
echo "-------------------------------------"
echo.
echo "Please open start_me.bat"
echo.
:: This line keeps the terminal open ::
PAUSE
:: This line exits the terminal
EXIT

:end
