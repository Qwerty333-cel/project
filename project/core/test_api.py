import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import (
    UserManager, MealPlanManager, MealManager,
    IngredientManager, DietTypeManager, FavoriteManager
)
from faker import Faker

fake = Faker()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return UserManager.create_user(
        username=fake.user_name(),
        password="testpass123",
        email=fake.email(),
        weight=70.0,
        height=175,
        age=25
    )

@pytest.fixture
def test_diet_type():
    return DietTypeManager.create_diet_type(
        name=fake.word(),
        is_restricted=False,
        description=fake.text()
    )

@pytest.fixture
def test_meal(test_diet_type):
    return MealManager.create_meal(
        name=fake.word(),
        price=15.99,
        description=fake.text(),
        diet_type_id=test_diet_type.id
    )

@pytest.fixture
def test_ingredient():
    return IngredientManager.create_ingredient(
        name=fake.word(),
        price_per_unit=5.99,
        unit="kg",
        store_name=fake.company()
    )

class TestUserAPI:
    def test_create_user(self, api_client):
        """Тест создания пользователя"""
        data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': fake.email(),
            'weight': fake.random_int(min=40, max=150),
            'height': fake.random_int(min=150, max=200),
            'age': fake.random_int(min=18, max=80)
        }
        response = api_client.post('/api/users/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username=data['username']).exists()

    def test_get_user(self, api_client, test_user):
        url = reverse('user-detail', args=[test_user.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == test_user.username

    def test_update_user(self, api_client, test_user):
        url = reverse('user-detail', args=[test_user.id])
        data = {'weight': 80.0, 'height': 185}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['weight'] == 80.0

    def test_delete_user(self, api_client, test_user):
        url = reverse('user-detail', args=[test_user.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=test_user.id).exists()

    def test_verify_password(self, api_client, test_user):
        url = reverse('user-verify-password', args=[test_user.id])
        data = {'password': 'testpass123'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_valid'] is True

class TestMealPlanAPI:
    def test_create_meal_plan(self, api_client, test_user):
        """Тест создания плана питания"""
        data = {
            'user_id': test_user.id,
            'duration': fake.random_int(min=1, max=30),
            'total_price': fake.random_int(min=1000, max=10000)
        }
        response = api_client.post('/api/meal-plans/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert MealPlans.objects.filter(user_id=test_user.id).exists()

    def test_get_meal_plan(self, api_client, test_user):
        meal_plan = MealPlanManager.create_meal_plan(
            user_id=test_user.id,
            duration=14,
            total_price=1000.0
        )
        url = reverse('meal-plan-detail', args=[meal_plan.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['duration'] == 14

    def test_calculate_plan_price(self, api_client, test_user):
        meal_plan = MealPlanManager.create_meal_plan(
            user_id=test_user.id,
            duration=14,
            total_price=1000.0
        )
        url = reverse('meal-plan-calculate-price', args=[meal_plan.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'price' in response.data

class TestMealAPI:
    def test_create_meal(self, api_client, test_diet_type):
        url = reverse('meal-list')
        data = {
            'name': 'New Meal',
            'price': 20.99,
            'description': 'New meal description',
            'diet_type_id': test_diet_type.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Meals.objects.filter(name='New Meal').exists()

    def test_get_meal(self, api_client, test_meal):
        url = reverse('meal-detail', args=[test_meal.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == test_meal.name

    def test_calculate_meal_price(self, api_client, test_meal):
        url = reverse('meal-calculate-price', args=[test_meal.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'price' in response.data

class TestIngredientAPI:
    def test_create_ingredient(self, api_client):
        url = reverse('ingredient-list')
        data = {
            'name': 'New Ingredient',
            'price_per_unit': 10.99,
            'unit': 'kg',
            'store_name': 'New Store'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Ingredients.objects.filter(name='New Ingredient').exists()

    def test_get_ingredient(self, api_client, test_ingredient):
        url = reverse('ingredient-detail', args=[test_ingredient.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == test_ingredient.name

class TestDietTypeAPI:
    def test_create_diet_type(self, api_client):
        url = reverse('diet-type-list')
        data = {
            'name': 'New Diet',
            'is_restricted': True,
            'description': 'New diet description'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert DietTypes.objects.filter(name='New Diet').exists()

    def test_get_diet_type(self, api_client, test_diet_type):
        url = reverse('diet-type-detail', args=[test_diet_type.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == test_diet_type.name

class TestFavoriteAPI:
    def test_create_favorite(self, api_client, test_user, test_meal):
        """Тест добавления блюда в избранное"""
        data = {
            'user_id': test_user.id,
            'meal_id': test_meal.id
        }
        response = api_client.post('/api/favorites/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Favorites.objects.filter(user_id=test_user.id, meal_id=test_meal.id).exists()

    def test_get_favorite(self, api_client, test_user, test_meal):
        favorite = FavoriteManager.create_favorite(
            user_id=test_user.id,
            meal_id=test_meal.id
        )
        url = reverse('favorite-detail', args=[favorite.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user_id'] == test_user.id
        assert response.data['meal_id'] == test_meal.id 