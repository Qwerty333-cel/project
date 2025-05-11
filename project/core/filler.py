import os
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from core.models import DietTypes, User, MealPlans, Meals, Ingredients, Favorites, MealPlanMeal, MealIngredient
from django.contrib.auth.models import User as DjangoUser
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Initialize Faker with English locale
Faker.seed(1234)  # Fix seed for reproducibility
fake = Faker(['en_US'])

def generate_random_date():
    # Generate timezone-aware date
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    return fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=timezone.get_current_timezone())

def generate_unique_username():
    while True:
        username = fake.user_name()
        if not DjangoUser.objects.filter(username=username).exists():
            return username

def generate_unique_email():
    while True:
        email = fake.email()
        if not DjangoUser.objects.filter(email=email).exists():
            return email

def generate_unique_password_hash():
    while True:
        password = fake.password(length=12)
        password_hash = generate_password_hash(password)
        if not User.objects.filter(password_hash=password_hash).exists():
            return password_hash

def create_diet_types():
    diet_types = []
    for _ in range(7):  # Generate 7 random diet types
        name = fake.word().capitalize()
        description = fake.sentence()
        is_restricted = fake.boolean()
        
        diet_type = DietTypes.objects.create(
            name=name,
            description=description,
            is_restricted=is_restricted
        )
        diet_types.append(diet_type)
    return diet_types

def create_users(diet_types):
    users = []
    for _ in range(20):
        # Generate unique user data
        username = generate_unique_username()
        email = generate_unique_email()
        password = fake.password(length=12)
        
        # Generate physical characteristics
        weight = round(random.uniform(45, 120), 1)  # kg
        height = round(random.uniform(150, 200), 1)  # cm
        age = random.randint(18, 80)
        
        # Create Django user first
        django_user = DjangoUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create our custom user
        user = User.objects.create(
            django_user=django_user,
            weight=weight,
            height=height,
            age=age,
            diet_type=random.choice(diet_types)
        )
        
        # Profile will be created automatically by the signal
        users.append(user)
    return users

def create_meals(diet_types):
    meals = []
    for _ in range(30):  # Generate 30 random meals
        # Generate meal data using Faker
        name = fake.catch_phrase()
        description = fake.paragraph(nb_sentences=3)
        price = round(random.uniform(5, 50), 2)
        
        meal = Meals.objects.create(
            name=name,
            description=description,
            price=price,
            diet_type=random.choice(diet_types)
        )
        meals.append(meal)
    return meals

def create_meal_plans(users, meals):
    meal_plans = []
    for _ in range(15):
        # Generate meal plan data
        duration = random.randint(7, 30)
        total_price = round(random.uniform(50, 500), 2)
        
        meal_plan = MealPlans.objects.create(
            user=random.choice(users),
            duration=duration,
            total_price=total_price
        )
        
        # Add random meals to the plan
        selected_meals = random.sample(meals, k=random.randint(1, 5))
        meal_plan.meals.add(*selected_meals)
        meal_plans.append(meal_plan)
    return meal_plans

def create_favorites(users, meals):
    # Создаем множество для отслеживания уже созданных пар
    created_pairs = set()
    
    # Пытаемся создать 30 уникальных избранных
    attempts = 0
    max_attempts = 100  # Максимальное количество попыток
    
    while len(created_pairs) < 30 and attempts < max_attempts:
        user = random.choice(users)
        meal = random.choice(meals)
        pair = (user.id, meal.id)
        
        if pair not in created_pairs:
            try:
                Favorites.objects.create(
                    user=user,
                    meal=meal
                )
                created_pairs.add(pair)
            except Exception as e:
                print(f"Ошибка при создании избранного: {e}")
        
        attempts += 1
    
    print(f"Создано {len(created_pairs)} уникальных избранных блюд")

def create_ingredients():
    ingredients = []
    for _ in range(40):  # Generate 40 random ingredients
        # Generate ingredient data using Faker
        name = fake.word().capitalize()
        price_per_unit = round(random.uniform(1, 20), 2)
        unit = random.choice(['kg', 'g', 'l', 'ml', 'oz', 'lb'])
        store_name = fake.company()
        valid_from = generate_random_date()
        
        ingredient = Ingredients.objects.create(
            name=name,
            price_per_unit=price_per_unit,
            unit=unit,
            store_name=store_name,
            valid_from=valid_from
        )
        ingredients.append(ingredient)
    return ingredients

def create_meal_ingredients(meals, ingredients):
    for meal in meals:
        # Add 3-8 random ingredients to each meal
        selected_ingredients = random.sample(ingredients, k=random.randint(3, 8))
        for ingredient in selected_ingredients:
            # Generate quantity based on ingredient unit
            if ingredient.unit in ['kg', 'l']:
                quantity = round(random.uniform(0.1, 1.0), 2)
            else:
                quantity = round(random.uniform(1, 10), 2)
                
            MealIngredient.objects.create(
                meal=meal,
                ingredient=ingredient,
                quantity=quantity
            )

def populate_database():
    try:
        with transaction.atomic():
            print("Creating diet types...")
            diet_types = create_diet_types()
            print(f"Created {len(diet_types)} diet types")

            print("Creating users...")
            users = create_users(diet_types)
            print(f"Created {len(users)} users")

            print("Creating meals...")
            meals = create_meals(diet_types)
            print(f"Created {len(meals)} meals")

            print("Creating meal plans...")
            meal_plans = create_meal_plans(users, meals)
            print(f"Created {len(meal_plans)} meal plans")

            print("Creating favorites...")
            create_favorites(users, meals)
            print("Created favorites")

            print("Creating ingredients...")
            ingredients = create_ingredients()
            print(f"Created {len(ingredients)} ingredients")

            print("Creating meal ingredients...")
            create_meal_ingredients(meals, ingredients)
            print("Created meal ingredients")

        print("\nDatabase successfully populated with test data!")
        print(f"Summary:")
        print(f"- {len(diet_types)} diet types")
        print(f"- {len(users)} users")
        print(f"- {len(meals)} meals")
        print(f"- {len(meal_plans)} meal plans")
        print(f"- {len(ingredients)} ingredients")
    except Exception as e:
        print(f"\nError while populating database: {e}")
        raise

if __name__ == "__main__":
    populate_database()
