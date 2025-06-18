@echo off
setlocal enabledelayedexpansion

:: Change to your project directory if needed
cd /d "%~dp0"

:: Check if .gitmodules exists
if not exist ".gitmodules" (
    echo ❌ No .gitmodules file found in this folder.
    pause
    exit /b
)

:: Make a temp folder to store submodule copies
mkdir __temp__

echo 🔍 Reading submodules...
for /f "tokens=2 delims== " %%A in ('findstr "path =" .gitmodules') do (
    set submodule=%%A
    set submodule=!submodule:~0,-1!
    echo 🔄 Cloning !submodule!...
    for /f "tokens=2 delims== " %%B in ('findstr "url =" .gitmodules') do (
        set url=%%B
        git clone !url! __temp__\!submodule!
        goto :copy
    )
)

:copy
:: Replace the submodule folder with actual code
rmdir /s /q !submodule!
move __temp__\!submodule! !submodule!

:: Cleanup submodule link
git submodule deinit -f .
git rm -f !submodule!

:: Delete .gitmodules if it still exists
if exist ".gitmodules" del .gitmodules

:: Final commit
git add .
git commit -m "🧹 Removed submodules and copied code into project"
git push

rmdir /s /q __temp__

echo ✅ Done! All submodules replaced.
pause
