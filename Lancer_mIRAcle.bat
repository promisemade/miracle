@echo off
title mIRAcle - Application Web
color 0A
echo.
echo   ================================================================
echo   =                                                              =
echo   =              mIRAcle - Application Web                       =
echo   =           Preparation Oral IRA Lille                         =
echo   =                                                              =
echo   =         Style Football Manager - 413 fiches                  =
echo   =                                                              =
echo   ================================================================
echo.
echo   Verification des dependances...
echo.

REM Se placer dans le bon dossier
cd /d "%~dp0"

REM Vérifier si l'environnement virtuel existe
if exist ".venv\Scripts\python.exe" (
    echo   [OK] Environnement virtuel detecte
    set PYTHON_CMD=.venv\Scripts\python.exe
    set PIP_CMD=.venv\Scripts\pip.exe
) else (
    echo   [INFO] Utilisation de Python systeme
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

REM Installer les dépendances si nécessaire
echo   Installation/verification des dependances...
%PIP_CMD% install flask PyMuPDF --quiet 2>nul

echo.
echo   [OK] Dependances verifiees
echo.
echo   ================================================================
echo   =  OUVERTURE DU NAVIGATEUR dans 3 secondes...                  =
echo   =                                                              =
echo   =  Adresse: http://localhost:5000                              =
echo   =  Mobile:  Utilisez l'IP affichee dans la console             =
echo   ================================================================
echo.

REM Ouvrir le navigateur après un délai
start "" cmd /c "timeout /t 3 >nul && start http://localhost:5000"

REM Lancer l'application web
%PYTHON_CMD% app.py
