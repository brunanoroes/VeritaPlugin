@echo off
chcp 65001 >nul
cd /d "%~dp0"
title VeritaPlugin

echo.
echo  ██╗   ██╗███████╗██████╗ ██╗████████╗ █████╗
echo  ██║   ██║██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗
echo  ██║   ██║█████╗  ██████╔╝██║   ██║   ███████║
echo  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║   ██╔══██║
echo   ╚████╔╝ ███████╗██║  ██║██║   ██║   ██║  ██║
echo    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
echo.
echo  ─────────────────────────────────────────────
echo.

:: ── Verificar Python ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python nao encontrado.
    echo  Baixe em: https://www.python.org/downloads/
    echo  Marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

:: ── Primeira execucao: instalar dependencias ──────────────────
if not exist ".instalado" (
    echo  Primeira execucao detectada!
    echo  Instalando dependencias, aguarde...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  [ERRO] Falha ao instalar dependencias.
        pause
        exit /b 1
    )
    echo. > .instalado
    echo.
    echo  [OK] Dependencias instaladas com sucesso!
    echo.
)

:: ── Verificar chave OpenAI ────────────────────────────────────
if not exist ".env" (
    echo  ─────────────────────────────────────────────
    echo  Configuracao da chave OpenAI
    echo  ─────────────────────────────────────────────
    echo.
    echo  Acesse https://platform.openai.com/api-keys para obter sua chave.
    echo  Ela sera salva localmente no arquivo .env apenas no seu computador.
    echo.
    for /f "delims=" %%i in ('powershell -Command "$k = Read-Host -Prompt \" Cole sua chave OpenAI (sk-...)\" -AsSecureString; [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($k))"') do set "OPENAI_KEY=%%i"
    if "%OPENAI_KEY%"=="" (
        echo.
        echo  [ERRO] Chave nao informada. Execute novamente para tentar outra vez.
        pause
        exit /b 1
    )
    echo OPENAI_API_KEY=%OPENAI_KEY%> .env
    echo.
    echo  [OK] Chave salva com seguranca!
    echo.
)

:: Verificar se a chave ainda está como exemplo
findstr /c:"cole_sua_chave_aqui" .env >nul 2>&1
if not errorlevel 1 (
    echo  [ERRO] Chave OpenAI nao configurada.
    echo  Apague o arquivo .env e execute novamente.
    echo.
    pause
    exit /b 1
)

:: ── Iniciar servidor ──────────────────────────────────────────
echo  [OK] Tudo pronto!
echo.
echo  Servidor rodando em http://localhost:8080
echo  Mantenha esta janela aberta enquanto usa o plugin.
echo  Para encerrar, feche esta janela ou pressione Ctrl+C.
echo.
echo  ─────────────────────────────────────────────
echo.

python api.py
