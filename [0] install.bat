:: This file installs or reinstalls the required python libraries for dynamic bike script to run
:: Last edited by:
::                 Peter Gates; July 24, 2021 ::

@ECHO OFF
cd ./src
ECHO "Which conda is installed?"
echo "1: anaconda"
echo "2: miniconda"
echo "3: neither"
SET /p response="Choice: (1, 2, or 3) "
if %response%==1 GOTO conda
if %response%==2 GOTO mini
if %response%==3 GOTO instructions
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
:: EDIT ME ::
:: Edit the below line to point to the anaconda directory as demonstrated below ::
CALL %USERPROFILE%\anaconda3\Scripts\activate.bat %USERPROFILE%\%user%\anaconda3
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
CALL %USERPROFILE%\miniconda3\Scripts\activate.bat %USERPROFILE%\miniconda3
:: This line installs everything in the requirements.txt file ::
pip install -r requirements.txt --upgrade

echo.
echo "-------------------------------------"
echo "Required libraries installed."
echo "-------------------------------------"
echo.
echo "Open start_me.bat"
echo.
:: This line keeps the terminal open ::
PAUSE
:: This line exits the terminal
EXIT

:end
