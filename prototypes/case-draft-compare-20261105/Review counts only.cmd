@echo off
setlocal
title Review draft change counts
where python >nul 2>&1
if errorlevel 1 (
  echo This kit needs an existing Python 3.10 or newer.
  echo No software has been installed and no files have been changed.
  pause
  exit /b 2
)
python "%~dp0review_drafts.py" --summary
set "case_review_exit=%errorlevel%"
echo.
pause
exit /b %case_review_exit%
