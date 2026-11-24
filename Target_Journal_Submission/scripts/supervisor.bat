@echo off
REM Layer B supervisor for Windows (untested here: this project ran on Linux). Loops until FINISHED or STOP file.
cd /d %~dp0..
:loop
if exist state\STOP_SUPERVISOR exit /b 0
findstr /C:"\"status\": \"FINISHED\"" state\agent_state.json >nul 2>&1 && exit /b 0
echo %date% %time% starting claude >> logs\supervisor.log
set /p PROMPT=<BOOTSTRAP_PROMPT.txt
claude -p "%PROMPT%" >> logs\supervisor.log 2>&1
echo %date% %time% agent exited, sleeping 15 min >> logs\supervisor.log
timeout /t 900 /nobreak >nul
goto loop
