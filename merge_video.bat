@echo off
REM Activate the virtual environment
call env2\Scripts\activate.bat

REM Run the python script
python mergevideo.py

echo.
echo Script execution complete.
pause
