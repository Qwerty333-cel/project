@echo off
echo Choose environment to run programs:
echo 1. Docker Container
echo 2. Virtual Environment
set /p env_choice="Enter your choice (1-2): "

if "%env_choice%"=="1" (
    goto docker_menu
) else if "%env_choice%"=="2" (
    goto venv_menu
) else (
    echo Invalid choice!
    timeout /t 2 >nul
    exit /b 1
)

:docker_menu
::cls
echo Starting Programs in Docker Container...

:: Change to the project directory
cd /d %~dp0

:: Menu for program selection
:docker_menu_loop
::cls
echo Choose a program to run in Docker:
echo 1. Run Django development server
echo 2. Run Django shell
echo 3. Run Django tests
echo 4. Run database filler
echo 5. Run database eraser
echo 6. Exit
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting Django development server...
    docker-compose exec web python manage.py runserver 0.0.0.0:8000
    if errorlevel 1 (
        echo Failed to start Django server!
        pause
    )
    goto docker_menu_loop
) else if "%choice%"=="2" (
    echo Starting Django shell...
    docker-compose exec web python manage.py shell
    if errorlevel 1 (
        echo Failed to start Django shell!
        pause
    )
    goto docker_menu_loop
) else if "%choice%"=="3" (
    echo Running Django tests...
    docker-compose exec web python manage.py test
    if errorlevel 1 (
        echo Tests failed!
        pause
    )
    goto docker_menu_loop
) else if "%choice%"=="4" (
    echo Running database filler...
    docker-compose exec web python core/filler.py
    if errorlevel 1 (
        echo Failed to run database filler!
        pause
    )
    goto docker_menu_loop
) else if "%choice%"=="5" (
    echo Running database eraser...
    docker-compose exec web python core/bd_eraser.py
    if errorlevel 1 (
        echo Failed to run database eraser!
        pause
    )
    goto docker_menu_loop
) else if "%choice%"=="6" (
    goto end
) else (
    echo Invalid choice!
    timeout /t 2 >nul
    goto docker_menu_loop
)

:venv_menu
::cls
echo Starting Programs in Virtual Environment...

:: Change to the project directory
cd /d %~dp0

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Menu for program selection
:venv_menu_loop
::cls
echo Choose a program to run in virtual environment:
echo 1. Run Django development server
echo 2. Run Django shell
echo 3. Run Django tests
echo 4. Run database filler
echo 5. Run database eraser
echo 6. Open terminal (continue working in venv)
echo 7. Exit
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Starting Django development server...
    python manage.py runserver
    if errorlevel 1 (
        echo Failed to start Django server!
        pause
    )
    goto venv_menu_loop
) else if "%choice%"=="2" (
    echo Starting Django shell...
    python manage.py shell
    if errorlevel 1 (
        echo Failed to start Django shell!
        pause
    )
    goto venv_menu_loop
) else if "%choice%"=="3" (
    echo Running Django tests...
    python manage.py test
    if errorlevel 1 (
        echo Tests failed!
        pause
    )
    goto venv_menu_loop
) else if "%choice%"=="4" (
    echo Running database filler...
    python core/filler.py
    if errorlevel 1 (
        echo Failed to run database filler!
        pause
    )
    goto venv_menu_loop
) else if "%choice%"=="5" (
    echo Running database eraser...
    python core/bd_eraser.py
    if errorlevel 1 (
        echo Failed to run database eraser!
        pause
    )
    goto venv_menu_loop
) else if "%choice%"=="6" (
    echo Opening terminal with activated virtual environment...
    echo You can now run any commands in the virtual environment.
    echo Type 'deactivate' to exit the virtual environment.
    cmd /k
    goto venv_menu_loop
) else if "%choice%"=="7" (
    goto venv_end
) else (
    echo Invalid choice!
    timeout /t 2 >nul
    goto venv_menu_loop
)

:venv_end
:: Deactivate virtual environment
deactivate
echo Virtual environment deactivated.

:end
echo Exiting... 