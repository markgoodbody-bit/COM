@echo off
rem Frontier Ledger launcher for Windows. It runs play.js with the Node.js already on this PC.
rem It downloads nothing, installs nothing and uses no network. Saves go to the folder you start in.
setlocal
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js was not found on this PC.
  echo Install Node.js 20 or later yourself from https://nodejs.org, then start play.cmd again.
  echo Press a key to close this window.
  pause >nul
  exit /b 1
)
set "major=0"
for /f "tokens=1 delims=v." %%v in ('node --version') do set "major=%%v"
if %major% LSS 20 (
  echo Frontier Ledger needs Node.js 20 or later. This PC has:
  call node --version
  echo Press a key to close this window.
  pause >nul
  exit /b 1
)
rem "call" returns here even when node is a .cmd shim, so an error stays on screen.
call node "%~dp0play.js" %*
set "code=%errorlevel%"
if not "%code%"=="0" (
  echo Frontier Ledger stopped with exit code %code%. Press a key to close this window.
  pause >nul
)
exit /b %code%
