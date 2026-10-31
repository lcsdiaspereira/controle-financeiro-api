@echo off
title Controle Financeiro - Starter
cd /d "D:\Controle financeiro"

echo ====================================================
echo    INICIANDO CONTROLE FINANCEIRO
echo ====================================================

echo.
echo [1/2] Iniciando Backend...
:: Abre um novo terminal, ativa o venv e roda o uvicorn
start cmd /k ".\venv\Scripts\activate && uvicorn backend.main:app --reload"

echo.
echo [2/2] Iniciando Frontend...
:: Abre um novo terminal, entra na pasta frontend e roda o npm run dev
start cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo    SISTEMA INICIADO COM SUCESSO!
echo ====================================================
echo.
echo As janelas do Backend e Frontend foram abertas.
echo Voce ja pode acessar o sistema no seu navegador.
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause > nul
