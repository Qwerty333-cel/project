# Документация файла conftest.py

## Общее описание
Файл `conftest.py` содержит конфигурацию для тестов pytest в Django проекте. Он настраивает окружение Django и REST Framework для тестирования API.

## Структура файла

### Импорты
```python
import os
import django
from django.conf import settings
```

### Настройка Django
```python
# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация Django
django.setup()
```
- Устанавливает модуль настроек Django
- Инициализирует Django для тестов

### Настройка REST Framework
```python
# Настройка REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# Добавление настроек REST Framework в settings
settings.REST_FRAMEWORK = REST_FRAMEWORK
```
- Настраивает рендереры и парсеры для тестов
- Использует только JSON формат
- Применяет настройки к тестовому окружению

## Использование
1. Файл автоматически загружается pytest при запуске тестов
2. Настройки применяются ко всем тестам в проекте
3. Обеспечивает корректную работу Django и REST Framework в тестах

## Примечания
- Файл должен находиться в корневой директории тестов
- Настройки применяются глобально для всех тестов
- Используется только JSON формат для API
- Инициализация Django происходит один раз при запуске тестов
- Настройки REST Framework оптимизированы для тестирования 