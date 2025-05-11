# Документация файла run_programs.bat

## Общее описание
Файл `run_programs.bat` - это интерактивный скрипт для Windows, который предоставляет меню для запуска различных программ проекта в двух окружениях: Docker-контейнере и виртуальном окружении Python. Он позволяет выполнять различные операции с проектом через удобный интерфейс.

## Структура файла

### Выбор окружения
```batch
echo Choose environment to run programs:
echo 1. Docker Container
echo 2. Virtual Environment
set /p env_choice="Enter your choice (1-2): "
```
- Предлагает выбрать окружение
- Поддерживает Docker и виртуальное окружение

### Меню Docker
```batch
:docker_menu_loop
echo Choose a program to run in Docker:
echo 1. Run Django development server
echo 2. Run Django shell
echo 3. Run Django tests
echo 4. Run API tests
echo 5. Run database filler
echo 6. Run database eraser
echo 7. Make migrations
echo 8. Apply migrations
echo 9. Exit
```
- Предоставляет доступ к основным командам Django
- Выполняет команды в Docker-контейнере
- Включает тестирование и управление базой данных

### Меню виртуального окружения
```batch
:venv_menu_loop
echo Choose a program to run in virtual environment:
echo 1. Run Django development server
echo 2. Run Django shell
echo 3. Run Django tests
echo 4. Run API tests
echo 5. Run database filler
echo 6. Run database eraser
echo 7. Open terminal (continue working in venv)
echo 8. Make migrations
echo 9. Apply migrations
echo 10. Exit
```
- Предоставляет те же команды в виртуальном окружении
- Дополнительно позволяет открыть терминал
- Управляет виртуальным окружением

### Обработка команд
```batch
if "%choice%"=="1" (
    echo Starting Django development server...
    docker-compose exec web python manage.py runserver 0.0.0.0:8000
    if errorlevel 1 (
        echo Failed to start Django server!
        pause
    )
    goto docker_menu_loop
)
```
- Выполняет выбранную команду
- Обрабатывает ошибки
- Возвращает в меню

## Использование
1. Запуск скрипта:
```bash
run_programs.bat
```

2. Выбор окружения:
- 1 - Docker Container
- 2 - Virtual Environment

3. Выбор команды:
- 1-9 для Docker
- 1-10 для виртуального окружения

## Доступные команды

### Общие команды
- Запуск сервера разработки
- Запуск Django shell
- Запуск тестов
- Запуск API тестов
- Заполнение базы данных
- Очистка базы данных
- Создание миграций
- Применение миграций

### Специфичные команды
- Docker: выполнение в контейнере
- Virtual Environment: открытие терминала

## Примечания
- Требует установленного Docker или Python
- Поддерживает интерактивный режим
- Обрабатывает ошибки выполнения
- Предоставляет удобный интерфейс
- Автоматизирует рутинные операции
- Поддерживает два окружения
- Обеспечивает возврат в меню
- Позволяет быстро переключаться между командами
- Упрощает работу с проектом
- Подходит для разработки и тестирования 