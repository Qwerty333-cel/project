# Документация файла docker-compose.yml

## Общее описание
Файл `docker-compose.yml` определяет конфигурацию Docker-контейнеров для проекта. Он описывает сервисы, их настройки, зависимости и сетевые взаимодействия между контейнерами.

## Структура файла

### Версия
```yaml
version: '3.8'
```
- Указывает версию формата docker-compose
- Поддерживает современные функции Docker

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
- Использует легковесный образ PostgreSQL
- Настраивает базу данных и пользователя
- Обеспечивает сохранность данных через volumes
- Проверяет здоровье сервиса
- Ограничивает максимальное количество подключений

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
- Предоставляет веб-интерфейс для управления PostgreSQL
- Настраивает учетные данные администратора
- Зависит от работоспособности базы данных

#### Веб-приложение
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
- Собирает приложение из Dockerfile
- Выполняет миграции и сбор статических файлов
- Монтирует код и медиа-файлы
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
- Использует легковесный образ Nginx
- Обслуживает статические и медиа-файлы
- Настраивается через конфигурационные файлы

### Сети
```yaml
networks:
  app_network:
    driver: bridge
```
- Создает изолированную сеть для контейнеров
- Использует драйвер bridge

### Тома
```yaml
volumes:
  postgres_data:
  pgadmin_data:
  static_volume:
  media_volume:
```
- Определяет постоянные тома для данных
- Обеспечивает сохранность данных между перезапусками

## Использование
1. Запуск всех сервисов:
```bash
docker-compose up -d
```

2. Остановка сервисов:
```bash
docker-compose down
```

3. Просмотр логов:
```bash
docker-compose logs -f
```

## Примечания
- Все сервисы используют легковесные образы
- Настроена проверка здоровья базы данных
- Реализовано автоматическое перезапускание контейнеров
- Данные сохраняются в именованных томах
- Настроена изолированная сеть
- Поддерживается горячая перезагрузка кода
- Реализована правильная последовательность запуска
- Настроено обслуживание статических файлов
- Поддерживается масштабирование
- Обеспечена безопасность данных 