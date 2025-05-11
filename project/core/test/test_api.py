from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User as DjangoUser
from core.models import User, DietTypes, MealPlans, Meals, Ingredients, Favorites

class TestAPIEndpoints(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/'
        self.login_url = '/api/token/'
        self.meal_plan_url = '/api/meal-plans/'
        self.meal_url = '/api/meals/'
        self.ingredient_url = '/api/ingredients/'
        self.diet_type_url = '/api/diet-types/'
        self.favorite_url = '/api/favorites/'

        # Данные для тестового пользователя
        self.user_data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }
        
        # Создаем тестовый тип диеты
        self.diet_type = DietTypes.objects.create(
            name="Test Diet",
            description="Test Diet Description",
            is_restricted=False
        )

        # Регистрируем пользователя и получаем токен
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def tearDown(self):
        # Очищаем все созданные данные после тестов
        Favorites.objects.all().delete()
        MealPlans.objects.all().delete()
        Meals.objects.all().delete()
        Ingredients.objects.all().delete()
        User.objects.all().delete()
        DietTypes.objects.all().delete()
        DjangoUser.objects.all().delete()

    def test_01_register_user(self):
        """Тест регистрации пользователя"""
        # Очищаем токен для этого теста
        self.client.credentials()
        
        # Очищаем существующего пользователя
        User.objects.all().delete()
        DjangoUser.objects.all().delete()
        
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DjangoUser.objects.filter(username=self.user_data['username']).exists())
        self.assertTrue(User.objects.filter(django_user__username=self.user_data['username']).exists())

    def test_02_login_user(self):
        """Тест входа пользователя"""
        # Очищаем токен для этого теста
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

    def test_03_protected_endpoints_require_jwt(self):
        """Тест проверки защиты эндпоинтов"""
        # Очищаем токен для этого теста
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

    def test_08_favorite_crud_with_jwt(self):
        """Тест CRUD операций для избранных блюд"""
        # Создаем блюдо для избранного
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