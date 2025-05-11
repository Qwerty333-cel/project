# Документация файла docker-compose.yml

## Общее описание
Файл `docker-compose.yml` определяет конфигурацию многоконтейнерного приложения. Он описывает сервисы, их настройки, зависимости и связи между ними.

## Структура файла

### Версия
```yaml
version: '3.8'
```
- Указывает версию формата docker-compose
- 3.8 поддерживает все современные функции Docker

### Сервисы

#### База данных (PostgreSQL)
```yaml
db:
  image: postgres:15-alpine
  container_name: postgres_db
  restart: unless-stopped
  environment:
    POSTGRES_DB: mydatabase
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: laygon
    POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    LANG: en_US.UTF-8
    LC_ALL: en_US.UTF-8
    PGDATA: /var/lib/postgresql/data/pgdata
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres -d mydatabase"]
    interval: 5s
    timeout: 5s
    retries: 10
    start_period: 10s
  networks:
    - app_network
  hostname: db
  command: postgres -c 'max_connections=1000'
```
- Использует легковесный образ PostgreSQL 15 на Alpine Linux
- Настраивает базу данных с указанными параметрами
- Пробрасывает порт 5432
- Сохраняет данные в именованном томе
- Проверяет здоровье сервиса
- Ограничивает максимальное количество соединений

#### PgAdmin
```yaml
pgadmin:
  image: dpage/pgadmin4:latest
  container_name: pgadmin
  restart: unless-stopped
  environment:
    PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
    PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-changeme}
    PGADMIN_CONFIG_SERVER_MODE: "False"
  ports:
    - "5050:80"
  volumes:
    - pgadmin_data:/var/lib/pgadmin
  depends_on:
    db:
      condition: service_healthy
  networks:
    - app_network
```
- Веб-интерфейс для управления PostgreSQL
- Доступен на порту 5050
- Использует переменные окружения для настройки
- Зависит от работоспособности базы данных

#### Веб-приложение (Django)
```yaml
web:
  build:
    context: .
    dockerfile: Dockerfile
  container_name: django_app
  restart: unless-stopped
  command: >
    sh -c "
      echo 'Waiting for database...' &&
      sleep 15 &&
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      python manage.py runserver 0.0.0.0:8000
    "
  volumes:
    - .:/app:delegated
    - static_volume:/app/staticfiles
    - media_volume:/app/media
  ports:
    - "8000:8000"
  env_file:
    - .env
  environment:
    - DB_HOST=db
    - DB_PORT=5432
  depends_on:
    db:
      condition: service_healthy
  networks:
    - app_network
```
- Собирается из локального Dockerfile
- Выполняет миграции и собирает статические файлы
- Монтирует локальные директории и тома
- Использует переменные окружения из .env
- Зависит от работоспособности базы данных

#### Nginx
```yaml
nginx:
  image: nginx:alpine
  container_name: nginx
  restart: unless-stopped
  ports:
    - "80:80"
  volumes:
    - static_volume:/app/staticfiles
    - media_volume:/app/media
    - ./nginx:/etc/nginx/conf.d
  depends_on:
    - web
  networks:
    - app_network
```
- Веб-сервер для раздачи статических файлов
- Использует легковесный образ Alpine
- Монтирует конфигурацию и статические файлы
- Зависит от веб-приложения

### Сети
```yaml
networks:
  app_network:
    driver: bridge
```
- Создает изолированную сеть для контейнеров
- Использует драйвер bridge для коммуникации

### Тома
```yaml
volumes:
  postgres_data:
  pgadmin_data:
  static_volume:
  media_volume:
```
- Определяет именованные тома для хранения данных
- Обеспечивает сохранность данных между перезапусками

## Использование
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f
```

## Примечания
- Все сервисы настроены на автоматический перезапуск
- Используются легковесные образы где возможно
- Настроены проверки здоровья для критических сервисов
- Данные сохраняются в именованных томах
- Конфигурация оптимизирована для разработки 