@echo off
echo ============================================
echo fake-useragent Test Suite
echo ============================================
echo.

cd /d "%~dp0"

python test_fake_useragent.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo All tests passed!
    echo ============================================
) else (
    echo.
    echo ============================================
    echo Some tests failed. See output above.
    echo ============================================
)

exit /b %ERRORLEVEL%
