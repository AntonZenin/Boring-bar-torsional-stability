@echo off
echo === Сборка C++ ядра ===

if not exist build mkdir build
cd build

cmake -G "Visual Studio 17 2022" -A x64 ..
if errorlevel 1 (
    echo Ошибка генерации CMake!
    cd ..
    exit /b 1
)


cmake --build . --config Release
if errorlevel 1 (
    echo Ошибка компиляции!
    cd ..
    exit /b 1
)

cd ..
echo.
echo === Сборка завершена! ===
echo Модуль скопирован в gui\borshtanga_core*.pyd
pause