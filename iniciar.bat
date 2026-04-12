@echo off
chcp 65001 >nul
title VeritaPlugin - Servidor

echo.
echo  VeritaPlugin - Iniciando servidor...
echo  ─────────────────────────────────────────────
echo.

:: Verificar .env
if not exist ".env" (
    echo  [ERRO] Arquivo .env nao encontrado.
    echo  Execute instalar.bat primeiro.
    echo.
    pause
    exit /b 1
)

:: Verificar se a chave está preenchida
findstr /c:"cole_sua_chave_aqui" .env >nul 2>&1
if not errorlevel 1 (
    echo  [ERRO] Chave OpenAI nao configurada.
    echo  Execute instalar.bat para configurar sua chave.
    echo.
    pause
    exit /b 1
)

echo  [OK] Configuracao encontrada.
echo.
echo  Servidor rodando em http://localhost:8080
echo  Mantenha esta janela aberta enquanto usa o plugin.
echo  Para encerrar, feche esta janela ou pressione Ctrl+C.
echo.
echo  ─────────────────────────────────────────────
echo.

python api.py
