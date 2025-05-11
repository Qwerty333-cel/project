# Документация файла bd_eraser.py

## Общее описание
Файл `bd_eraser.py` - это скрипт для очистки базы данных Django-проекта. Он удаляет все данные из таблиц в правильном порядке с учетом зависимостей между ними, используя транзакции для обеспечения целостности данных.

## Структура файла

### Импорты и настройка окружения
```python
import os
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
```
- Добавляет корневую директорию проекта в `sys.path`
- Настраивает окружение Django
- Импортирует необходимые модули Django

### Импорт моделей
```python
from django.db import transaction
from django.contrib.auth.models import User as DjangoUser
from core.models import (
    DietTypes, User, MealPlans, Meals, Ingredients, 
    Favorites, MealPlanMeal, MealIngredient, Profile
)
```
- Импортирует транзакции Django
- Импортирует модель пользователя Django
- Импортирует все необходимые модели приложения

### Функция clear_database
```python
def clear_database():
    try:
        with transaction.atomic():
            # ... код очистки базы данных ...
    except Exception as e:
        print(f"\nОшибка при очистке базы данных: {e}")
        raise
```
- Основная функция для очистки базы данных
- Использует транзакции для обеспечения атомарности операций
- Обрабатывает возможные ошибки

### Порядок удаления данных
1. **Связи между блюдами и ингредиентами**
   ```python
   MealIngredient.objects.all().delete()
   ```
   - Удаляет связи между блюдами и их ингредиентами

2. **Связи между планами и блюдами**
   ```python
   MealPlanMeal.objects.all().delete()
   ```
   - Удаляет связи между планами питания и блюдами

3. **Избранные блюда**
   ```python
   Favorites.objects.all().delete()
   ```
   - Удаляет записи об избранных блюдах пользователей

4. **Планы питания**
   ```python
   MealPlans.objects.all().delete()
   ```
   - Удаляет все планы питания

5. **Блюда**
   ```python
   Meals.objects.all().delete()
   ```
   - Удаляет все блюда

6. **Ингредиенты**
   ```python
   Ingredients.objects.all().delete()
   ```
   - Удаляет все ингредиенты

7. **Пользователи сайта**
   ```python
   User.objects.all().delete()
   ```
   - Удаляет пользователей приложения

8. **Профили**
   ```python
   Profile.objects.all().delete()
   ```
   - Удаляет профили пользователей

9. **Пользователи Django**
   ```python
   DjangoUser.objects.all().delete()
   ```
   - Удаляет пользователей Django

10. **Типы диет**
    ```python
    DietTypes.objects.all().delete()
    ```
    - Удаляет все типы диет

### Точка входа
```python
if __name__ == "__main__":
    clear_database()
```
- Запускает очистку базы данных при прямом запуске скрипта

## Использование
1. Скрипт может быть запущен напрямую:
   ```bash
   python core/bd_eraser.py
   ```
2. Или импортирован и использован в другом коде:
   ```python
   from core.bd_eraser import clear_database
   clear_database()
   ```

## Примечания
- Скрипт использует транзакции для обеспечения целостности данных
- Удаление происходит в правильном порядке с учетом зависимостей
- Все операции выполняются в рамках одной транзакции
- При ошибке все изменения откатываются
- Скрипт выводит информацию о процессе очистки
- Рекомендуется использовать с осторожностью в продакшн-окружении 