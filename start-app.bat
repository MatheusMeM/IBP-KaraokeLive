@echo off
REM ========================================
REM  IBP-KaraokeLive - Auto Start
REM ========================================

REM Aguardar 10 segundos para garantir que tudo carregou
timeout /t 10 /nobreak >nul

REM Ir para o diretorio do projeto
cd /d "C:\Users\MNDS\Documents\GitHub\IBP-KaraokeLive"

REM Ativar ambiente virtual (se existir)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Iniciar o aplicativo
python main.py

REM Se o aplicativo fechar, aguardar antes de sair
timeout /t 5
