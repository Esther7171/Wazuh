@echo off
REM Batch script to connect via SSH
REM Replace 'cybrotech' and '122.160.144.106' with the desired username and IP if needed

set username=cybrotech
set ip=122.160.144.106
set port=9999

echo Connecting to %username%@%ip% on port %port%...
ssh %username%@%ip% -p %port%

REM Pause the script to see output after execution
pause

