# Документация файла urls.py

## Общее описание
Файл `urls.py` определяет маршруты API для приложения, используя Django REST framework. Он регистрирует ViewSets для различных моделей и создает соответствующие URL-паттерны.

## Структура файла

### Импорты
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, MealPlanViewSet, MealViewSet,
    IngredientViewSet, DietTypeViewSet, FavoriteViewSet
)
```

### Регистрация маршрутов
```python
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('meal-plans', MealPlanViewSet, basename='meal-plan')
router.register('meals', MealViewSet, basename='meal')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('diet-types', DietTypeViewSet, basename='diet-type')
router.register('favorites', FavoriteViewSet, basename='favorite')
```

### URL-паттерны
```python
urlpatterns = [
    path('', include(router.urls)),
]
```

## Доступные endpoints

### Пользователи
- `GET /users/` - список пользователей
- `POST /users/` - создание пользователя
- `GET /users/{id}/` - получение пользователя
- `PUT /users/{id}/` - обновление пользователя
- `DELETE /users/{id}/` - удаление пользователя
- `POST /users/{id}/verify_password/` - проверка пароля

### Планы питания
- `GET /meal-plans/` - список планов
- `POST /meal-plans/` - создание плана
- `GET /meal-plans/{id}/` - получение плана
- `PUT /meal-plans/{id}/` - обновление плана
- `DELETE /meal-plans/{id}/` - удаление плана
- `GET /meal-plans/{id}/calculate_price/` - расчет стоимости

### Блюда
- `GET /meals/` - список блюд
- `POST /meals/` - создание блюда
- `GET /meals/{id}/` - получение блюда
- `PUT /meals/{id}/` - обновление блюда
- `DELETE /meals/{id}/` - удаление блюда
- `GET /meals/{id}/calculate_price/` - расчет стоимости

### Ингредиенты
- `GET /ingredients/` - список ингредиентов
- `POST /ingredients/` - создание ингредиента
- `GET /ingredients/{id}/` - получение ингредиента
- `PUT /ingredients/{id}/` - обновление ингредиента
- `DELETE /ingredients/{id}/` - удаление ингредиента

### Типы диет
- `GET /diet-types/` - список типов диет
- `POST /diet-types/` - создание типа диеты
- `GET /diet-types/{id}/` - получение типа диеты
- `PUT /diet-types/{id}/` - обновление типа диеты
- `DELETE /diet-types/{id}/` - удаление типа диеты

### Избранное
- `GET /favorites/` - список избранных блюд
- `POST /favorites/` - добавление в избранное
- `GET /favorites/{id}/` - получение избранного блюда
- `PUT /favorites/{id}/` - обновление избранного
- `DELETE /favorites/{id}/` - удаление из избранного

## Примечания
- Все endpoints используют JWT аутентификацию
- Большинство endpoints требуют аутентификации
- Используется DefaultRouter для автоматической генерации URL-паттернов
- Каждый ViewSet имеет свой базовый URL
- Поддерживаются стандартные CRUD операции
- Реализованы дополнительные действия для специфических операций 