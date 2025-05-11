# Документация файла views.py

## Общее описание
Файл `views.py` содержит представления (views) для API endpoints приложения, реализованные с использованием Django REST framework. Представления обеспечивают CRUD операции и дополнительные действия для различных моделей данных.

## Структура файла

### Импорты
```python
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import (
    UserManager, MealPlanManager, MealManager,
    IngredientManager, DietTypeManager, FavoriteManager,
    PriceManager
)
from .serializers import (
    UserSerializer, MealPlanSerializer, MealSerializer,
    IngredientSerializer, DietTypeSerializer, FavoriteSerializer
)
```

### UserViewSet
```python
class UserViewSet(viewsets.ModelViewSet):
    """API endpoint для управления пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def verify_password(self, request, pk=None):
        """Проверить пароль пользователя"""
```
- Наследуется от `ModelViewSet`
- Использует JWT аутентификацию
- Разрешает создание и вход без аутентификации
- Имеет дополнительное действие для проверки пароля

### MealPlanViewSet
```python
class MealPlanViewSet(viewsets.ModelViewSet):
    """API endpoint для управления планами питания"""
    queryset = MealPlans.objects.all()
    serializer_class = MealPlanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость плана питания"""
```
- Управляет планами питания
- Требует аутентификации
- Имеет действие для расчета стоимости

### MealViewSet
```python
class MealViewSet(viewsets.ModelViewSet):
    """API endpoint для управления блюдами"""
    queryset = Meals.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость блюда"""
```
- Управляет блюдами
- Требует аутентификации
- Имеет действие для расчета стоимости

### IngredientViewSet
```python
class IngredientViewSet(viewsets.ModelViewSet):
    """API endpoint для управления ингредиентами"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
```
- Управляет ингредиентами
- Требует аутентификации

### DietTypeViewSet
```python
class DietTypeViewSet(viewsets.ModelViewSet):
    """API endpoint для управления типами диет"""
    queryset = DietTypes.objects.all()
    serializer_class = DietTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
```
- Управляет типами диет
- Требует аутентификации

### FavoriteViewSet
```python
class FavoriteViewSet(viewsets.ModelViewSet):
    """API endpoint для управления избранными блюдами"""
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
```
- Управляет избранными блюдами
- Требует аутентификации

## Использование
1. Все endpoints требуют JWT аутентификации, кроме:
   - Создание пользователя
   - Вход пользователя

2. Доступные операции для каждого ViewSet:
   - GET (list, retrieve)
   - POST (create)
   - PUT/PATCH (update, partial_update)
   - DELETE (destroy)

3. Дополнительные действия:
   - `/users/{id}/verify_password/` - проверка пароля
   - `/mealplans/{id}/calculate_price/` - расчет стоимости плана
   - `/meals/{id}/calculate_price/` - расчет стоимости блюда

## Примечания
- Все представления используют JWT аутентификацию
- Большинство endpoints требуют аутентификации
- Используются соответствующие сериализаторы для каждой модели
- Реализованы дополнительные действия для специфических операций
- Все представления наследуются от ModelViewSet для стандартных CRUD операций 