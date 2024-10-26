@echo off
setlocal enabledelayedexpansion

REM Definir los valores de entrada para cada iteración
set entrada1=A
set entrada2=B
set entrada3=C

REM Bucle para ejecutar el programa 10 veces
for /L %%i in (1,1,10) do (
    echo Ejecutando iteración %%i con valores de entrada !entrada1!, !entrada2!, !entrada3!
    
    REM Llamar al ejecutable y pasarle los tres valores de entrada
    mi_programa.exe !entrada1! !entrada2! !entrada3!
    
    REM Cambiar los valores de entrada en cada iteración (puedes personalizar esta lógica)
    set /a entrada1=!entrada1!+1
    set /a entrada2=!entrada2!+1
    set /a entrada3=!entrada3!+1
)

echo Todas las ejecuciones completadas.
endlocal
pause