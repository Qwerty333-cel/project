# Документация файла config/urls.py

## Общее описание
Файл `urls.py` в директории `config` определяет основные URL-маршруты проекта. Он включает маршруты для административной панели, API endpoints и аутентификации JWT.

## Структура файла

### Импорты
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from core.views import (
    UserViewSet, MealPlanViewSet, MealViewSet,
    IngredientViewSet, DietTypeViewSet, FavoriteViewSet
)
```

### Регистрация маршрутов API
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
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Доступные endpoints

### Административная панель
- `GET /admin/` - доступ к административной панели Django

### Аутентификация
- `POST /api/token/` - получение JWT токена
- `POST /api/token/refresh/` - обновление JWT токена

### API Endpoints
Все API endpoints доступны по базовому пути `/api/`:

#### Пользователи
- `GET /api/users/` - список пользователей
- `POST /api/users/` - создание пользователя
- `GET /api/users/{id}/` - получение пользователя
- `PUT /api/users/{id}/` - обновление пользователя
- `DELETE /api/users/{id}/` - удаление пользователя
- `POST /api/users/{id}/verify_password/` - проверка пароля

#### Планы питания
- `GET /api/meal-plans/` - список планов
- `POST /api/meal-plans/` - создание плана
- `GET /api/meal-plans/{id}/` - получение плана
- `PUT /api/meal-plans/{id}/` - обновление плана
- `DELETE /api/meal-plans/{id}/` - удаление плана
- `GET /api/meal-plans/{id}/calculate_price/` - расчет стоимости

#### Блюда
- `GET /api/meals/` - список блюд
- `POST /api/meals/` - создание блюда
- `GET /api/meals/{id}/` - получение блюда
- `PUT /api/meals/{id}/` - обновление блюда
- `DELETE /api/meals/{id}/` - удаление блюда
- `GET /api/meals/{id}/calculate_price/` - расчет стоимости

#### Ингредиенты
- `GET /api/ingredients/` - список ингредиентов
- `POST /api/ingredients/` - создание ингредиента
- `GET /api/ingredients/{id}/` - получение ингредиента
- `PUT /api/ingredients/{id}/` - обновление ингредиента
- `DELETE /api/ingredients/{id}/` - удаление ингредиента

#### Типы диет
- `GET /api/diet-types/` - список типов диет
- `POST /api/diet-types/` - создание типа диеты
- `GET /api/diet-types/{id}/` - получение типа диеты
- `PUT /api/diet-types/{id}/` - обновление типа диеты
- `DELETE /api/diet-types/{id}/` - удаление типа диеты

#### Избранное
- `GET /api/favorites/` - список избранных блюд
- `POST /api/favorites/` - добавление в избранное
- `GET /api/favorites/{id}/` - получение избранного блюда
- `PUT /api/favorites/{id}/` - обновление избранного
- `DELETE /api/favorites/{id}/` - удаление из избранного

## Примечания
- Все API endpoints требуют JWT аутентификации
- Используется DefaultRouter для автоматической генерации URL-паттернов
- Административная панель доступна по стандартному пути
- JWT токены имеют ограниченный срок действия
- Все API endpoints начинаются с префикса `/api/`
- Поддерживаются стандартные CRUD операции
- Реализованы дополнительные действия для специфических операций 