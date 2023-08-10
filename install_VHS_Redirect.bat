@echo off
set "hostsfile=%windir%\System32\drivers\etc\hosts"
set "string_to_append=127.0.0.1 api.vhsgame.com"
set "string_to_append2=127.0.0.1 ns.vhsgame.com"
set "string_to_append3=127.0.0.1 cdn.vhsgame.com"
set "string_to_append4=127.0.0.1 mms.vhsgame.com"

echo   --------------------------------------
echo   --   VHS Hosts Redirect Installer   --
echo   --          ~ SkelXton              --
echo   --------------------------------------
echo.

echo Installing certificate to Trusted Root store...
echo     - - -
REM Install LuigiDevGoodCA.crt certificate to Trusted Root store
certutil -addstore Root "%~dp0LuigiDevGoodCA.crt"

if %errorlevel% EQU 0 (
    echo Certificate installed successfully.
) else (
    echo Certificate installation failed.
    pause 
    exit /b 1
)

echo Adding the new entry to the hosts file...
echo     - - -
REM Check if the new entry already exists in the hosts file
findstr /c:".vhsgame.com" "%hostsfile%" > nul
if not errorlevel 1 (
    echo New entry already exists in the hosts file. Exiting...
    pause
    exit /b 1
)

REM Append a new line and the new entry to the hosts file
echo.>> "%hostsfile%"
echo %string_to_append%>> "%hostsfile%"
echo %string_to_append2%>> "%hostsfile%"
echo %string_to_append3%>> "%hostsfile%"
echo %string_to_append4%>> "%hostsfile%"
echo.

echo New hosts entries added successfully.
echo.
pause

