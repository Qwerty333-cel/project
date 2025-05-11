# Документация файла serializers.py

## Общее описание
Файл `serializers.py` содержит сериализаторы Django REST framework для преобразования моделей в JSON и обратно. Сериализаторы определяют, какие поля моделей будут включены в API и как они будут валидироваться.

## Структура файла

### Импорты
```python
from rest_framework import serializers
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import UserManager
```

### UserSerializer
```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'weight', 'height', 'age', 'diet_type_id']
```
- Наследуется от `ModelSerializer`
- Определяет поля для создания и обновления пользователя
- Пароль доступен только для записи
- Имя пользователя и email обязательны
- Включает дополнительные поля: вес, рост, возраст, тип диеты

#### Методы
- `create`: Создает нового пользователя через UserManager
- `update`: Обновляет данные пользователя, включая пароль

### MealPlanSerializer
```python
class MealPlanSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = MealPlans
        fields = ['id', 'user_id', 'duration', 'total_price']
```
- Сериализует планы питания
- Требует ID пользователя
- Включает длительность и общую стоимость

### MealSerializer
```python
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meals
        fields = ['id', 'name', 'description', 'price', 'diet_type_id']
```
- Сериализует блюда
- Включает название, описание, цену и тип диеты

### IngredientSerializer
```python
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'price_per_unit', 'unit', 'store_name', 'valid_from']
```
- Сериализует ингредиенты
- Включает название, цену за единицу, единицу измерения, название магазина и дату начала действия

### DietTypeSerializer
```python
class DietTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietTypes
        fields = ['id', 'name', 'description', 'is_restricted']
```
- Сериализует типы диет
- Включает название, описание и флаг ограничений

### FavoriteSerializer
```python
class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    meal_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Favorites
        fields = ['id', 'user_id', 'meal_id']
```
- Сериализует избранные блюда
- Требует ID пользователя и ID блюда

## Использование
1. Создание объектов:
   ```python
   serializer = UserSerializer(data=request.data)
   if serializer.is_valid():
       user = serializer.save()
   ```

2. Обновление объектов:
   ```python
   serializer = UserSerializer(user, data=request.data, partial=True)
   if serializer.is_valid():
       user = serializer.save()
   ```

3. Сериализация объектов:
   ```python
   serializer = UserSerializer(user)
   return Response(serializer.data)
   ```

## Примечания
- Все сериализаторы наследуются от ModelSerializer
- Используются встроенные валидаторы Django REST framework
- Пароль пользователя доступен только для записи
- Некоторые поля помечены как обязательные
- Сериализаторы интегрированы с менеджерами моделей
- Поддерживают частичное обновление объектов 