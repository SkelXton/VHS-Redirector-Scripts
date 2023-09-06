@echo off
set "hostsfile=%windir%\System32\drivers\etc\hosts"

echo   --------------------------------------
echo   --  VHS Hosts Redirect Uninstaller  --
echo   --         ~ SkelXton               --
echo   --------------------------------------
echo.

echo Searching and removing the string from the hosts file...
echo     - - -
REM Use findstr with regular expression to find lines containing ".vhsgame.com" and store the result in a temporary file
findstr /v /i /r /c:".*\.vhsgame\.com.*" "%hostsfile%" > "%hostsfile%.tmp"

REM Overwrite the original hosts file with the modified content (excluding the target string)
move /y "%hostsfile%.tmp" "%hostsfile%"

echo.
echo Removing certificate from Trusted Root store...
echo     - - -
REM Remove LuigiDevGoodCA.crt certificate from Trusted Root store
certutil -delstore Root 7121d851d63039bd

echo.
echo Entries removed successfully (be sure to double check just to be safe)!
echo You can use the command: "certutil -store -user Root" to check the certificate.
echo.

pause
