@echo off
setlocal
set "PROJECT_ROOT=%~dp0"
set "NODE_COMMAND="
set "NPM_COMMAND="

where node >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "NODE_COMMAND=node"
  set "NPM_COMMAND=npm"
) else (
  for /d %%D in ("%TEMP%\node-v*-win-x64") do (
    set "NODE_COMMAND=%%~fD\node.exe"
    set "NPM_COMMAND=%%~fD\npm.cmd"
  )
)

if not defined NODE_COMMAND (
  echo Node.js is required. Install Node.js LTS and run this file again.
  exit /b 1
)

pushd "%PROJECT_ROOT%"

if not exist "node_modules" (
  call "%NPM_COMMAND%" install
  if errorlevel 1 exit /b 1
)

if /I "%~1"=="--validate" (
  "%NODE_COMMAND%" "scripts\self-test.mjs"
  if errorlevel 1 exit /b 1
  "%NODE_COMMAND%" "node_modules\vite\bin\vite.js" build
  if errorlevel 1 exit /b 1
  popd
  exit /b 0
)

echo Starting React POC at http://localhost:5173
"%NODE_COMMAND%" "node_modules\vite\bin\vite.js" --host localhost --port 5173
set "RUN_EXIT=%ERRORLEVEL%"
popd
exit /b %RUN_EXIT%
