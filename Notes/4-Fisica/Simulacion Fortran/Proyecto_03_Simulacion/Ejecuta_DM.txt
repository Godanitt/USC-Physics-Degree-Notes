@echo off

cd "%~dp0"  REM Cambia al directorio donde se encuentra el archivo .bat
for /L %%i in (1,1,10) do (
    .\CheckMate\x64\Proyecto_3.exe %%i
    echo Finalizamos %%i	

)
pause

