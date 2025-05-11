# Документация файла config.py

## Общее описание
Файл `config.py` содержит конфигурационные параметры для подключения к базе данных. Он использует библиотеку `python-decouple` для безопасного получения значений из переменных окружения.

## Структура файла

### Импорты
```python
from decouple import config
```

### Конфигурация базы данных
```python
DATABASE_URL = config("DATABASE_URL", default="postgresql://postgres:laygon@localhost:5432/mydatabase")
db_url = 'postgresql://postgres:laygon@localhost:5432/mydatabase'
```

## Параметры

### DATABASE_URL
- Тип: `str`
- Источник: переменная окружения `DATABASE_URL`
- Значение по умолчанию: `"postgresql://postgres:laygon@localhost:5432/mydatabase"`
- Формат: `postgresql://{user}:{password}@{host}:{port}/{database}`
- Описание: URL для подключения к базе данных PostgreSQL

### db_url
- Тип: `str`
- Значение: `"postgresql://postgres:laygon@localhost:5432/mydatabase"`
- Описание: Резервный URL для подключения к базе данных

## Примечания
- Использует python-decouple для безопасного хранения конфиденциальных данных
- Поддерживает конфигурацию через переменные окружения
- Имеет значения по умолчанию для разработки
- Формат URL соответствует стандарту PostgreSQL
- Может быть переопределен через переменные окружения
- Содержит резервный URL для случаев, когда переменная окружения не установлена 