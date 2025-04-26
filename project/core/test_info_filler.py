from faker import Faker
from django.utils.timezone import now
from django.db import transaction
from werkzeug.security import generate_password_hash
from .models import DietTypes, User, MealPlans, Meals, Ingredients, Favorites, MealPlanMeal, MealIngredient

# Создание экземпляра Faker
fake = Faker()

def populate_database():
    try:
        with transaction.atomic():  # Используем транзакцию для обеспечения целостности данных
            # Создание тестовых типов диет
            diet_types = [
                DietTypes.objects.create(
                    name="Vegetarian",
                    description="No meat products",
                    is_restricted=False
                ),
                DietTypes.objects.create(
                    name="Keto",
                    description="Low carb, high fat diet",
                    is_restricted=True
                ),
                DietTypes.objects.create(
                    name="Vegan",
                    description="No animal products",
                    is_restricted=True
                )
            ]

            # Создание тестовых пользователей
            users = []
            for _ in range(10):
                user = User.objects.create(
                    username=fake.user_name(),
                    password_hash=generate_password_hash(fake.password()),
                    weight=fake.random_int(min=50, max=100),
                    height=fake.random_int(min=150, max=200),
                    age=fake.random_int(min=18, max=80),
                    email=fake.email(),
                    diet_type=fake.random_element(diet_types)
                )
                users.append(user)

            # Создание тестовых планов питания
            meal_plans = []
            for _ in range(10):
                meal_plan = MealPlans.objects.create(
                    user=fake.random_element(users),
                    duration=fake.random_int(min=7, max=30),
                    total_price=fake.random_int(min=50, max=500)
                )
                meal_plans.append(meal_plan)

            # Создание тестовых блюд
            meals = []
            for _ in range(15):
                meal = Meals.objects.create(
                    name=fake.word(),
                    description=fake.text(),
                    price=fake.random_int(min=5, max=50),
                    diet_type=fake.random_element(diet_types)
                )
                meals.append(meal)

            # Создание тестовых избранных блюд
            for _ in range(10):
                Favorites.objects.create(
                    user=fake.random_element(users),
                    meal=fake.random_element(meals)
                )

            # Создание тестовых ингредиентов
            ingredients = []
            for _ in range(20):
                ingredient = Ingredients.objects.create(
                    name=fake.word(),
                    price_per_unit=fake.random_int(min=1, max=20),
                    unit=fake.random_element(elements=("kg", "g", "l", "ml")),
                    store_name=fake.company(),
                    valid_from=fake.date_time_this_year()
                )
                ingredients.append(ingredient)

            # Заполнение таблицы MealPlanMeal
            for meal_plan in meal_plans:
                selected_meals = fake.random_elements(elements=meals, length=fake.random_int(min=1, max=5), unique=True)
                meal_plan.meals.add(*selected_meals)

            # Заполнение таблицы MealIngredient
            for meal in meals:
                selected_ingredients = fake.random_elements(elements=ingredients, length=fake.random_int(min=3, max=8), unique=True)
                for ingredient in selected_ingredients:
                    quantity = fake.random_int(min=1, max=10) + fake.random_number(digits=2) / 100
                    MealIngredient.objects.create(
                        meal=meal,
                        ingredient=ingredient,
                        quantity=quantity
                    )

        print("База данных успешно заполнена тестовыми данными!")
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")

if __name__ == "__main__":
    populate_database()