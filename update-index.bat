@echo off
setlocal

:: Configurações (AJUSTE ESTAS LINHAS ANTES DE USAR!)
set REPO_URL=https://github.com/djavan-ryuuzaki/win-py-whls
set PYTHON_EXEC=python

:: Verifica se o Python está disponível
%PYTHON_EXEC% --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: Python nao encontrado. Verifique se esta instalado e no PATH.
    exit /b 1
)

:: Verifica se os scripts existem
if not exist build-index.py (
    echo Erro: build-index.py nao encontrado na pasta atual.
    exit /b 1
)
if not exist update-readme.py (
    echo Erro: update-readme.py nao encontrado na pasta atual.
    exit /b 1
)

echo.
echo 🔧 Atualizando indice de wheels...
%PYTHON_EXEC% build-index.py . --repo-url %REPO_URL%
if %ERRORLEVEL% neq 0 (
    echo Falha ao executar build-index.py.
    exit /b 1
)

echo.
echo 📝 Atualizando README.md...
%PYTHON_EXEC% update-readme.py
if %ERRORLEVEL% neq 0 (
    echo Falha ao executar update-readme.py.
    exit /b 1
)

echo.
echo ✅ Atualizacao concluida com sucesso!
echo Nao se esqueca de fazer commit das alteracoes:
echo   - wheels.json
echo   - README.md
echo   - Novos arquivos .whl (se houver)

pause