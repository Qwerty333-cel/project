# Документация файла start_project.bat

## Общее описание
Файл `start_project.bat` - это скрипт для Windows, который автоматизирует процесс запуска Django-проекта. Он выполняет все необходимые шаги для подготовки окружения, запуска Docker-контейнеров и проверки их работоспособности.

## Структура файла

### Инициализация
```batch
@echo off
echo Starting Django Project...
```
- Отключает вывод команд
- Выводит сообщение о начале работы

### Переход в директорию проекта
```batch
cd /d %~dp0
```
- Переходит в директорию, где находится скрипт
- Использует абсолютный путь

### Очистка порта
```batch
echo Clearing port 5432...
call port_clearer.bat
```
- Очищает порт 5432 для PostgreSQL
- Вызывает вспомогательный скрипт

### Виртуальное окружение
```batch
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate
```
- Создает виртуальное окружение, если его нет
- Активирует виртуальное окружение

### Установка зависимостей
```batch
echo Installing dependencies...
pip install -r requirements.txt
```
- Устанавливает все необходимые пакеты

### Проверка Docker
```batch
docker info > nul 2>&1
if errorlevel 1 (
    echo Docker Desktop is not running. Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start...
    timeout /t 30 
)
```
- Проверяет, запущен ли Docker Desktop
- Запускает Docker Desktop, если он не запущен
- Ждет 30 секунд для инициализации

### Очистка контейнеров
```batch
echo Stopping any running containers...
cmd /c docker-compose down
echo Cleaning up old containers and volumes...
cmd /c docker-compose down -v
cmd /c docker system prune -f
```
- Останавливает все запущенные контейнеры
- Удаляет старые контейнеры и тома
- Очищает неиспользуемые ресурсы Docker

### Запуск контейнеров
```batch
echo Building and starting containers...
cmd /c docker-compose build --no-cache
cmd /c docker-compose up -d
```
- Пересобирает контейнеры без использования кэша
- Запускает контейнеры в фоновом режиме

### Проверка статуса
```batch
echo Waiting for services to be ready...
timeout /t 10 /nobreak
echo Checking container status...
cmd /c docker-compose ps
echo Checking container logs...
cmd /c docker-compose logs web
```
- Ждет 10 секунд для инициализации сервисов
- Проверяет статус контейнеров
- Показывает логи веб-приложения

### Завершение работы
```batch
echo Project is running!
echo Django app: http://localhost:8000
echo PgAdmin: http://localhost:5050
echo Press any key to stop the containers...
pause > nul
cmd /c docker-compose down
deactivate
```
- Выводит информацию о доступных сервисах
- Ждет нажатия клавиши
- Останавливает контейнеры
- Деактивирует виртуальное окружение

## Использование
1. Запуск проекта:
```bash
start_project.bat
```

2. Остановка проекта:
- Нажмите любую клавишу в консоли

## Примечания
- Скрипт автоматизирует все необходимые шаги
- Обеспечивает чистый запуск проекта
- Проверяет наличие всех зависимостей
- Управляет Docker-контейнерами
- Поддерживает виртуальное окружение
- Очищает порты перед запуском
- Показывает статус и логи
- Обеспечивает корректное завершение
- Требует прав администратора
- Подходит для разработки и тестирования 