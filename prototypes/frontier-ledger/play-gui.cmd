@echo off
setlocal
where node >nul 2>nul
if errorlevel 1 (
 echo Frontier Ledger needs Node.js 20 or newer already installed.
 pause
 exit /b 1
)
node -e "process.exit(Number(process.versions.node.split('.')[0])>=20?0:1)"
if errorlevel 1 (
 echo Frontier Ledger needs Node.js 20 or newer.
 pause
 exit /b 1
)
node "%~dp0play-gui.js"
if errorlevel 1 pause
endlocal
