@echo off
chcp 65001 >nul
title VeritaPlugin - Instalação

echo.
echo  ██╗   ██╗███████╗██████╗ ██╗████████╗ █████╗
echo  ██║   ██║██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗
echo  ██║   ██║█████╗  ██████╔╝██║   ██║   ███████║
echo  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║   ██╔══██║
echo   ╚████╔╝ ███████╗██║  ██║██║   ██║   ██║  ██║
echo    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
echo.
echo  Instalação do VeritaPlugin
echo  ─────────────────────────────────────────────
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python não encontrado.
    echo  Baixe em: https://www.python.org/downloads/
    echo  Marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo  [OK] Python encontrado.
echo.

:: Instalar dependências
echo  Instalando dependencias (pode demorar alguns minutos)...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo  [OK] Dependencias instaladas.
echo.
echo  ─────────────────────────────────────────────
echo  Configuracao da chave OpenAI
echo  ─────────────────────────────────────────────
echo.
echo  Acesse https://platform.openai.com/api-keys para obter sua chave.
echo  Ela sera salva localmente no arquivo .env (nao enviada para nenhum servidor).
echo.

:: Ler chave com input oculto via PowerShell
for /f "delims=" %%i in ('powershell -Command "$k = Read-Host -Prompt \" Cole sua chave OpenAI (sk-...)\" -AsSecureString; [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($k))"') do set "OPENAI_KEY=%%i"

if "%OPENAI_KEY%"=="" (
    echo.
    echo  [ERRO] Chave nao informada. Execute instalar.bat novamente.
    pause
    exit /b 1
)

:: Salvar no .env
echo OPENAI_API_KEY=%OPENAI_KEY%> .env

echo.
echo  [OK] Chave salva com seguranca em .env
echo.
echo  ─────────────────────────────────────────────
echo  Instalacao concluida!
echo  Execute iniciar.bat para usar o VeritaPlugin.
echo  ─────────────────────────────────────────────
echo.
pause
