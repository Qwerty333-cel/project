# Документация файла test_api.py

## Общее описание
Файл `test_api.py` содержит тесты для API эндпоинтов приложения. Тесты написаны с использованием Django REST framework's `APITestCase` и проверяют функциональность всех основных API эндпоинтов, включая аутентификацию, CRUD операции и защиту эндпоинтов.

## Структура файла

### Импорты
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User as DjangoUser
from core.models import User, DietTypes, MealPlans, Meals, Ingredients, Favorites
```
- Импортируются необходимые классы для тестирования API
- Импортируются модели для работы с базой данных

### Класс TestAPIEndpoints

#### Настройка тестового окружения
```python
def setUp(self):
    # Определение URL эндпоинтов
    self.register_url = '/api/users/'
    self.login_url = '/api/token/'
    self.meal_plan_url = '/api/meal-plans/'
    self.meal_url = '/api/meals/'
    self.ingredient_url = '/api/ingredients/'
    self.diet_type_url = '/api/diet-types/'
    self.favorite_url = '/api/favorites/'

    # Данные тестового пользователя
    self.user_data = {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com"
    }
    
    # Создание тестового типа диеты
    self.diet_type = DietTypes.objects.create(
        name="Test Diet",
        description="Test Diet Description",
        is_restricted=False
    )

    # Регистрация пользователя и получение токена
    self.client.post(self.register_url, self.user_data, format='json')
    response = self.client.post(self.login_url, {
        'username': self.user_data['username'],
        'password': self.user_data['password']
    }, format='json')
    self.token = response.data['access']
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
```
- Инициализирует URL эндпоинтов
- Создает тестовые данные
- Настраивает аутентификацию

#### Очистка после тестов
```python
def tearDown(self):
    # Очистка всех созданных данных
    Favorites.objects.all().delete()
    MealPlans.objects.all().delete()
    Meals.objects.all().delete()
    Ingredients.objects.all().delete()
    User.objects.all().delete()
    DietTypes.objects.all().delete()
    DjangoUser.objects.all().delete()
```
- Удаляет все тестовые данные после каждого теста

### Тесты API

#### Регистрация пользователя
```python
def test_01_register_user(self):
    """Тест регистрации пользователя"""
    # Очистка токена и существующих пользователей
    self.client.credentials()
    User.objects.all().delete()
    DjangoUser.objects.all().delete()
    
    response = self.client.post(self.register_url, self.user_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertTrue(DjangoUser.objects.filter(username=self.user_data['username']).exists())
    self.assertTrue(User.objects.filter(django_user__username=self.user_data['username']).exists())
```
- Проверяет успешную регистрацию нового пользователя
- Проверяет создание записей в обеих моделях пользователей

#### Вход пользователя
```python
def test_02_login_user(self):
    """Тест входа пользователя"""
    self.client.credentials()
    
    response = self.client.post(
        self.login_url,
        {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        },
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)
```
- Проверяет успешный вход пользователя
- Проверяет получение токенов доступа и обновления

#### Проверка защиты эндпоинтов
```python
def test_03_protected_endpoints_require_jwt(self):
    """Тест проверки защиты эндпоинтов"""
    self.client.credentials()
    
    endpoints = [
        self.meal_plan_url,
        self.meal_url,
        self.ingredient_url,
        self.diet_type_url,
        self.favorite_url
    ]
    for url in endpoints:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```
- Проверяет, что защищенные эндпоинты требуют JWT токен
- Проверяет все основные эндпоинты

#### CRUD операции для типов диет
```python
def test_04_diet_type_crud_with_jwt(self):
    """Тест CRUD операций для типов диет"""
    # Create
    diet_type_data = {
        "name": "Low Carb",
        "description": "Low carbohydrate diet",
        "is_restricted": True
    }
    response = self.client.post(self.diet_type_url, diet_type_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    diet_type_id = response.data['id']

    # Read
    response = self.client.get(f'{self.diet_type_url}{diet_type_id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], diet_type_data['name'])

    # Update
    update_data = {"name": "Very Low Carb"}
    response = self.client.patch(f'{self.diet_type_url}{diet_type_id}/', update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], update_data['name'])

    # Delete
    response = self.client.delete(f'{self.diet_type_url}{diet_type_id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```
- Проверяет все CRUD операции для типов диет
- Включает создание, чтение, обновление и удаление

#### CRUD операции для планов питания
```python
def test_05_meal_plan_crud_with_jwt(self):
    """Тест CRUD операций для планов питания"""
    # Create
    meal_plan_data = {
        "user_id": 1,
        "duration": 7,
        "total_price": 100.0
    }
    response = self.client.post(self.meal_plan_url, meal_plan_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    meal_plan_id = response.data['id']

    # Read
    response = self.client.get(f'{self.meal_plan_url}{meal_plan_id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['id'], meal_plan_id)

    # Update
    update_data = {"total_price": 120.0}
    response = self.client.patch(f'{self.meal_plan_url}{meal_plan_id}/', update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(float(response.data['total_price']), update_data['total_price'])

    # Delete
    response = self.client.delete(f'{self.meal_plan_url}{meal_plan_id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```
- Проверяет все CRUD операции для планов питания
- Включает создание, чтение, обновление и удаление

#### CRUD операции для блюд
```python
def test_06_meal_crud_with_jwt(self):
    """Тест CRUD операций для блюд"""
    # Create
    meal_data = {
        "name": "Breakfast",
        "price": 10.5,
        "description": "Healthy breakfast",
        "diet_type_id": self.diet_type.id
    }
    response = self.client.post(self.meal_url, meal_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    meal_id = response.data['id']

    # Read
    response = self.client.get(f'{self.meal_url}{meal_id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], meal_data['name'])

    # Update
    update_data = {"price": 12.0}
    response = self.client.patch(f'{self.meal_url}{meal_id}/', update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(float(response.data['price']), update_data['price'])

    # Delete
    response = self.client.delete(f'{self.meal_url}{meal_id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```
- Проверяет все CRUD операции для блюд
- Включает создание, чтение, обновление и удаление

#### CRUD операции для ингредиентов
```python
def test_07_ingredient_crud_with_jwt(self):
    """Тест CRUD операций для ингредиентов"""
    # Create
    ingredient_data = {
        "name": "Eggs",
        "price_per_unit": 0.5,
        "unit": "piece",
        "store_name": "Local Market"
    }
    response = self.client.post(self.ingredient_url, ingredient_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    ingredient_id = response.data['id']

    # Read
    response = self.client.get(f'{self.ingredient_url}{ingredient_id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], ingredient_data['name'])

    # Update
    update_data = {"price_per_unit": 0.6}
    response = self.client.patch(f'{self.ingredient_url}{ingredient_id}/', update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(float(response.data['price_per_unit']), update_data['price_per_unit'])

    # Delete
    response = self.client.delete(f'{self.ingredient_url}{ingredient_id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```
- Проверяет все CRUD операции для ингредиентов
- Включает создание, чтение, обновление и удаление

#### CRUD операции для избранных блюд
```python
def test_08_favorite_crud_with_jwt(self):
    """Тест CRUD операций для избранных блюд"""
    # Создание тестового блюда
    meal = Meals.objects.create(
        name="Test Meal",
        price=10.0,
        description="Test Description",
        diet_type=self.diet_type
    )

    # Create
    favorite_data = {
        "user_id": 1,
        "meal_id": meal.id
    }
    response = self.client.post(self.favorite_url, favorite_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    favorite_id = response.data['id']

    # Read
    response = self.client.get(f'{self.favorite_url}{favorite_id}/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['user_id'], favorite_data['user_id'])

    # Delete
    response = self.client.delete(f'{self.favorite_url}{favorite_id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```
- Проверяет все CRUD операции для избранных блюд
- Включает создание, чтение и удаление

## Использование
1. Запуск всех тестов:
   ```bash
   python manage.py test core.test.test_api
   ```

2. Запуск конкретного теста:
   ```bash
   python manage.py test core.test.test_api.TestAPIEndpoints.test_01_register_user
   ```

## Примечания
- Тесты используют JWT аутентификацию
- Каждый тест выполняется в изолированной среде
- Данные очищаются после каждого теста
- Тесты проверяют как успешные сценарии, так и обработку ошибок
- Все CRUD операции проверяются с учетом аутентификации
- Тесты следуют порядку выполнения (нумерация в названиях) 