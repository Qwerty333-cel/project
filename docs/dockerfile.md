# Документация файла Dockerfile

## Общее описание
`Dockerfile` - это файл с инструкциями для создания Docker-образа приложения. Он определяет, как будет собрано и запущено приложение в контейнере.

## Структура файла

### Базовый образ
```dockerfile
FROM python:3.11-slim-bullseye as builder
```
- Использует официальный образ Python 3.11
- `slim-bullseye` - облегченная версия на базе Debian Bullseye
- `as builder` - задает имя этапа сборки

### Переменные окружения
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive
```
- `PYTHONDONTWRITEBYTECODE=1` - отключает создание .pyc файлов
- `PYTHONUNBUFFERED=1` - отключает буферизацию вывода Python
- `DEBIAN_FRONTEND=noninteractive` - отключает интерактивные диалоги при установке пакетов

### Установка системных зависимостей
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libpq-dev \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
```
- Обновляет списки пакетов
- Устанавливает необходимые пакеты:
  - `build-essential` - инструменты для компиляции
  - `curl` - утилита для работы с HTTP
  - `libpq-dev` - библиотеки для работы с PostgreSQL
  - `netcat-traditional` - утилита для работы с сетевыми соединениями
- Очищает кэш apt для уменьшения размера образа

### Рабочая директория
```dockerfile
WORKDIR /app
```
- Создает и переходит в директорию `/app`
- Все последующие команды будут выполняться в этой директории

### Копирование и установка зависимостей
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- Копирует файл `requirements.txt` в контейнер
- Устанавливает Python-зависимости
- `--no-cache-dir` - отключает кэширование pip

### Создание пользователя
```dockerfile
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django
```
- Создает пользователя `django` с UID 1000
- Передает права на директорию `/app` пользователю `django`
- Переключается на пользователя `django` для безопасности

### Копирование файлов проекта
```dockerfile
COPY --chown=django:django . .
```
- Копирует все файлы проекта в контейнер
- `--chown=django:django` - устанавливает владельца файлов

### Настройка портов и томов
```dockerfile
EXPOSE 8000
VOLUME ["/app/staticfiles", "/app/media"]
```
- `EXPOSE 8000` - указывает, что контейнер будет использовать порт 8000
- `VOLUME` - создает тома для статических и медиа файлов

### Команда запуска
```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
- Запускает сервер разработки Django
- `0.0.0.0:8000` - слушает на всех интерфейсах порт 8000

## Использование
Для сборки и запуска контейнера:
```bash
# Сборка образа
docker build -t myapp .

# Запуск контейнера
docker run -p 8000:8000 myapp
```

## Примечания
- Образ оптимизирован для разработки
- Для продакшн рекомендуется использовать gunicorn вместо runserver
- Тома для статических и медиа файлов позволяют сохранять данные между запусками
- Использование непривилегированного пользователя повышает безопасность 