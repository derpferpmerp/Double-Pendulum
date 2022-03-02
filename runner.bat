@echo off

Setlocal EnableDelayedExpansion

echo --- Calculating N Pendulum --
python3 generateJson.py @@@

echo -- Animating --
echo.

FOR /f "tokens=1,2,3 delims=: " %%g in ('find /c /v "" tmp.json') do @set "LineCount=%%i"

set /a LineCount=%LineCount% - 20

set divident=%LineCount%
set divisor=840

for /f "delims=" %%a in ('powershell -Command %divident%/%divisor%') do set seconds=%%a

FOR /f "usebackq" %%i IN (`PowerShell [Math]::Round^(%seconds%^,2^,[MidpointRounding]::AwayFromZero^)`) DO SET rounded=%%i

echo It will take an estimated %rounded% minutes for the video creation
echo.

:start
SET choice=
SET /p choice=Proceed to Rendering the Video? [Y/N]: 
IF NOT '%choice%'=='' SET choice=%choice:~0,1%
IF /i '%choice%'=='Y' GOTO yes
IF /i '%choice%'=='N' GOTO no
IF '%choice%'=='' GOTO no
ECHO "%choice%" is not valid
ECHO.
GOTO start

:fixTime
echo.
echo -- Fixing Time Dilation --
echo.
python3 changeVideoSpeed.py
EXIT

:no
echo.
echo  you can run the rendering process anytime you want by executing:
echo.
echo     powershell.exe /c "manim render --fps 30 main.py"
echo.
echo  and then:
echo.
echo     python3 changeVideoSpeed.py
echo.

EXIT

:yes
powershell.exe /c "manim render --fps 30 main.py"
GOTO fixTime