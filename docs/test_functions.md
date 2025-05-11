# Документация файла test_functions.py

## Общее описание
Файл `test_functions.py` содержит модульные тесты для функций-менеджеров приложения. Тесты проверяют функциональность классов-менеджеров для работы с пользователями, планами питания, блюдами, ингредиентами, типами диет и избранными блюдами.

## Структура файла

### Импорты и настройка окружения
```python
import os
import sys

# Добавляем корневую директорию проекта в sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from core.models import DietTypes, User, MealPlans, Meals, Ingredients, Favorites, MealPlanMeal, MealIngredient
from core.functions import (
    UserManager, MealPlanManager, MealManager,
    IngredientManager, DietTypeManager, FavoriteManager
)
```
- Настраивает окружение Django
- Импортирует необходимые классы и модели
- Импортирует классы-менеджеры для тестирования

### Тесты функций пользователя

#### Класс TestUserFunctions
```python
class TestUserFunctions(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            'weight': 70.5,
            'height': 175.0,
            'age': 30
        }
```
- Инициализирует тестовые данные пользователя

#### Создание пользователя
```python
def test_create_user(self):
    user = UserManager.create_user(**self.user_data)
    self.assertIsNotNone(user)
    self.assertEqual(user.username, self.user_data['username'])
    self.assertEqual(user.email, self.user_data['email'])
    self.assertEqual(user.weight, self.user_data['weight'])
    self.assertEqual(user.height, self.user_data['height'])
    self.assertEqual(user.age, self.user_data['age'])
```
- Проверяет создание пользователя
- Проверяет корректность сохраненных данных

#### Получение пользователя
```python
def test_get_user(self):
    user = UserManager.create_user(**self.user_data)
    retrieved_user = UserManager.get_user_by_id(user.id)
    self.assertEqual(retrieved_user, user)
```
- Проверяет получение пользователя по ID
- Проверяет соответствие полученных данных

#### Удаление пользователя
```python
def test_delete_user(self):
    user = UserManager.create_user(**self.user_data)
    self.assertTrue(UserManager.delete_user(user.id))
    self.assertIsNone(UserManager.get_user_by_id(user.id))
```
- Проверяет удаление пользователя
- Проверяет отсутствие пользователя после удаления

#### Проверка пароля
```python
def test_verify_password(self):
    user = UserManager.create_user(**self.user_data)
    self.assertTrue(UserManager.verify_password(user, self.user_data['password']))
    self.assertFalse(UserManager.verify_password(user, 'wrongpassword'))
```
- Проверяет верификацию правильного пароля
- Проверяет верификацию неправильного пароля

### Тесты функций плана питания

#### Класс TestMealPlanFunctions
```python
class TestMealPlanFunctions(TestCase):
    def setUp(self):
        self.user = UserManager.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.meal_plan_data = {
            'user_id': self.user.id,
            'duration': 7,
            'total_price': 100.00
        }
```
- Создает тестового пользователя
- Инициализирует данные плана питания

#### Создание плана питания
```python
def test_create_meal_plan(self):
    meal_plan = MealPlanManager.create_meal_plan(**self.meal_plan_data)
    self.assertIsNotNone(meal_plan)
    self.assertEqual(meal_plan.duration, self.meal_plan_data['duration'])
    self.assertEqual(meal_plan.total_price, self.meal_plan_data['total_price'])
```
- Проверяет создание плана питания
- Проверяет корректность сохраненных данных

#### Получение плана питания
```python
def test_get_meal_plan(self):
    meal_plan = MealPlanManager.create_meal_plan(**self.meal_plan_data)
    retrieved_plan = MealPlanManager.get_meal_plan_by_id(meal_plan.id)
    self.assertEqual(retrieved_plan, meal_plan)
```
- Проверяет получение плана питания по ID
- Проверяет соответствие полученных данных

#### Удаление плана питания
```python
def test_delete_meal_plan(self):
    meal_plan = MealPlanManager.create_meal_plan(**self.meal_plan_data)
    self.assertTrue(MealPlanManager.delete_meal_plan(meal_plan.id))
    self.assertIsNone(MealPlanManager.get_meal_plan_by_id(meal_plan.id))
```
- Проверяет удаление плана питания
- Проверяет отсутствие плана после удаления

### Тесты функций блюд

#### Класс TestMealFunctions
```python
class TestMealFunctions(TestCase):
    def setUp(self):
        self.diet_type = DietTypeManager.create_diet_type(
            name='Test Diet',
            is_restricted=False,
            description='Test diet description'
        )
        self.meal_data = {
            'name': 'Test Meal',
            'price': 15.99,
            'description': 'Test meal description',
            'diet_type_id': self.diet_type.id
        }
```
- Создает тестовый тип диеты
- Инициализирует данные блюда

#### Создание блюда
```python
def test_create_meal(self):
    meal = MealManager.create_meal(**self.meal_data)
    self.assertIsNotNone(meal)
    self.assertEqual(meal.name, self.meal_data['name'])
    self.assertEqual(meal.price, self.meal_data['price'])
    self.assertEqual(meal.description, self.meal_data['description'])
```
- Проверяет создание блюда
- Проверяет корректность сохраненных данных

#### Получение блюда
```python
def test_get_meal(self):
    meal = MealManager.create_meal(**self.meal_data)
    retrieved_meal = MealManager.get_meal_by_id(meal.id)
    self.assertEqual(retrieved_meal, meal)
```
- Проверяет получение блюда по ID
- Проверяет соответствие полученных данных

#### Удаление блюда
```python
def test_delete_meal(self):
    meal = MealManager.create_meal(**self.meal_data)
    self.assertTrue(MealManager.delete_meal(meal.id))
    self.assertIsNone(MealManager.get_meal_by_id(meal.id))
```
- Проверяет удаление блюда
- Проверяет отсутствие блюда после удаления

### Тесты функций ингредиентов

#### Класс TestIngredientFunctions
```python
class TestIngredientFunctions(TestCase):
    def setUp(self):
        self.ingredient_data = {
            'name': 'Test Ingredient',
            'price_per_unit': 2.99,
            'unit': 'kg',
            'store_name': 'Test Store'
        }
```
- Инициализирует данные ингредиента

#### Создание ингредиента
```python
def test_create_ingredient(self):
    ingredient = IngredientManager.create_ingredient(**self.ingredient_data)
    self.assertIsNotNone(ingredient)
    self.assertEqual(ingredient.name, self.ingredient_data['name'])
    self.assertEqual(ingredient.price_per_unit, self.ingredient_data['price_per_unit'])
    self.assertEqual(ingredient.unit, self.ingredient_data['unit'])
```
- Проверяет создание ингредиента
- Проверяет корректность сохраненных данных

#### Получение ингредиента
```python
def test_get_ingredient(self):
    ingredient = IngredientManager.create_ingredient(**self.ingredient_data)
    retrieved_ingredient = IngredientManager.get_ingredient_by_id(ingredient.id)
    self.assertEqual(retrieved_ingredient, ingredient)
```
- Проверяет получение ингредиента по ID
- Проверяет соответствие полученных данных

#### Удаление ингредиента
```python
def test_delete_ingredient(self):
    ingredient = IngredientManager.create_ingredient(**self.ingredient_data)
    self.assertTrue(IngredientManager.delete_ingredient(ingredient.id))
    self.assertIsNone(IngredientManager.get_ingredient_by_id(ingredient.id))
```
- Проверяет удаление ингредиента
- Проверяет отсутствие ингредиента после удаления

### Тесты функций типов диет

#### Класс TestDietTypeFunctions
```python
class TestDietTypeFunctions(TestCase):
    def setUp(self):
        self.diet_type_data = {
            'name': 'Test Diet',
            'is_restricted': True,
            'description': 'Test diet description'
        }
```
- Инициализирует данные типа диеты

#### Создание типа диеты
```python
def test_create_diet_type(self):
    diet_type = DietTypeManager.create_diet_type(**self.diet_type_data)
    self.assertIsNotNone(diet_type)
    self.assertEqual(diet_type.name, self.diet_type_data['name'])
    self.assertEqual(diet_type.is_restricted, self.diet_type_data['is_restricted'])
```
- Проверяет создание типа диеты
- Проверяет корректность сохраненных данных

#### Получение типа диеты
```python
def test_get_diet_type(self):
    diet_type = DietTypeManager.create_diet_type(**self.diet_type_data)
    retrieved_diet_type = DietTypeManager.get_diet_type_by_id(diet_type.id)
    self.assertEqual(retrieved_diet_type, diet_type)
```
- Проверяет получение типа диеты по ID
- Проверяет соответствие полученных данных

#### Удаление типа диеты
```python
def test_delete_diet_type(self):
    diet_type = DietTypeManager.create_diet_type(**self.diet_type_data)
    self.assertTrue(DietTypeManager.delete_diet_type(diet_type.id))
    self.assertIsNone(DietTypeManager.get_diet_type_by_id(diet_type.id))
```
- Проверяет удаление типа диеты
- Проверяет отсутствие типа диеты после удаления

## Использование
1. Запуск всех тестов:
   ```bash
   python manage.py test core.test.test_functions
   ```

2. Запуск конкретного теста:
   ```bash
   python manage.py test core.test.test_functions.TestUserFunctions.test_create_user
   ```

## Примечания
- Тесты используют Django TestCase
- Каждый тест выполняется в изолированной среде
- Тесты проверяют основные CRUD операции
- Все тесты независимы друг от друга
- Тесты следуют принципу AAA (Arrange-Act-Assert)
- Каждый тест проверяет одну конкретную функциональность 