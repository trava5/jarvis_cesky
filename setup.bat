@echo off
chcp 65001 >nul
echo.
echo ========================================
echo        Instalace J.A.R.V.I.S
echo ========================================
echo.

REM Kontrola Pythonu
python --version >nul 2>&1
if errorlevel 1 (
    echo [CHYBA] Python nebyl nalezen. Nainstalujte Python 3.10+ z python.org.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i

REM Virtuální prostředí
if not exist "venv" (
    echo [*] Vytvářím virtuální prostředí...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM Soubor s klíči API
if not exist "config\api_keys.json" (
    copy "config\api_keys.example.json" "config\api_keys.json" >nul
    echo [*] Vytvořen config\api_keys.json - zadejte do něj klíč Gemini API
)

echo [*] Instaluji balíčky...
pip install --upgrade pip -q
pip install -r requirements.txt -q

REM Instalace písem do Windows může vyžadovat oprávnění správce.
if exist "Fonts" (
    echo [*] Instaluji písma Grift...
    for %%f in (Fonts\*.ttf) do (
        copy "%%f" "%WINDIR%\Fonts\" >nul 2>&1
    )
    echo [OK] Písma nainstalována. Pokud instalace selhala, použijte ručně složku Fonts.
)

echo.
echo ========================================
echo          Instalace dokončena
echo ========================================
echo.
echo Spuštění JARVIS:
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
set /p choice="Spustit nyní? (a/n): "
if /i "%choice%"=="a" python main.py
if /i "%choice%"=="y" python main.py
