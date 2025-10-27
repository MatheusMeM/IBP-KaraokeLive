@echo off
REM NOVO - Define o título inicial da janela
title IBP-KaraokeLive - Auto Restart

REM ========================================
REM  IBP-KaraokeLive - Auto Restart
REM  Reinicia automaticamente se o app fechar
REM ========================================

REM Criar diretório de logs se não existir
if not exist "C:\IBP-Logs" mkdir "C:\IBP-Logs"

REM Arquivo de log
set "LOG_FILE=C:\IBP-Logs\app-restart.log"

REM Escrever cabeçalho no log
echo ======================================== >> "%LOG_FILE%"
echo IBP-KaraokeLive Auto-Restart >> "%LOG_FILE%"
echo Iniciado em: %DATE% %TIME% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

REM Aguardar 5 segundos para sistema carregar
timeout /t 5 /nobreak >nul

REM Contador de reinícios
set RESTART_COUNT=0

:START_APP
REM NOVO - Limpa a tela do console para uma nova tentativa
cls

REM Incrementar contador
set /a RESTART_COUNT+=1

REM NOVO - Atualiza o título da janela com a contagem de tentativas
title IBP-KaraokeLive - Tentativa #%RESTART_COUNT%

REM Log
echo. >> "%LOG_FILE%"
echo [%DATE% %TIME%] Iniciando Tentativa #%RESTART_COUNT% >> "%LOG_FILE%"

REM Ir para diretório do projeto
cd /d "C:\Users\MNDS\Documents\GitHub\IBP-KaraokeLive"

REM Verificar se diretório existe
if not exist "main.py" (
    echo [%DATE% %TIME%] ERRO: main.py nao encontrado! >> "%LOG_FILE%"
    echo ERRO: Diretorio incorreto ou main.py nao encontrado!
    echo Pressione qualquer tecla para sair...
    pause >nul
    exit /b 1
)

REM Ativar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    echo [%DATE% %TIME%] Ativando venv... >> "%LOG_FILE%"
    call venv\Scripts\activate.bat
) else (
    echo [%DATE% %TIME%] AVISO: venv nao encontrado >> "%LOG_FILE%"
)

REM Iniciar o aplicativo
echo [%DATE% %TIME%] Iniciando aplicativo (main.py)... >> "%LOG_FILE%"
echo.
echo ========================================
echo   IBP-KaraokeLive - Tentativa #%RESTART_COUNT%
echo ========================================
echo.
echo Iniciando aplicativo...
echo Pressione ESC na janela do app para fechar normalmente.
echo Logs: %LOG_FILE%
echo.

python main.py

REM Capturar código de saída
set EXIT_CODE=%ERRORLEVEL%

REM NOVO - Limpa a tela para mostrar a mensagem de status final de forma clara
cls

echo [%DATE% %TIME%] Aplicativo fechou (codigo de saida: %EXIT_CODE%) >> "%LOG_FILE%"
echo.
echo ========================================
echo   Aplicativo Fechou
echo ========================================
echo   Codigo de saida: %EXIT_CODE%
echo   Tentativa: #%RESTART_COUNT%
echo   Data/Hora: %DATE% %TIME%
echo ========================================
echo.

REM Verificar se foi fechamento normal (ESC) ou crash
if %EXIT_CODE%==0 (
    echo [%DATE% %TIME%] Fechamento normal detectado (Codigo: 0). Nao reiniciando. >> "%LOG_FILE%"
    echo Fechamento normal. Nao reiniciando.
    echo.
    echo Pressione qualquer tecla para sair...
    pause >nul
    exit /b 0
)

REM Se chegou aqui, foi um crash - reiniciar
echo [%DATE% %TIME%] CRASH detectado (Codigo: %EXIT_CODE%)! Reiniciando em 5 segundos... >> "%LOG_FILE%"
echo.
echo CRASH DETECTADO!
echo.
echo O aplicativo sera reiniciado em 5 segundos...
echo Para cancelar, feche esta janela agora.
echo.

timeout /t 5 /nobreak

REM Voltar para o início e reiniciar
goto START_APP