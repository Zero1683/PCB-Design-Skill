@echo off
setlocal
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js 18+ is required. Install Node.js LTS, then reopen this launcher.
  pause
  exit /b 1
)
node "%~dp0scripts\easyeda_bridge.mjs" start
echo.
echo EDA_CONNECTED = connected. WAITING_FOR_EDA = enable Run API Gateway in EasyEDA.
pause
