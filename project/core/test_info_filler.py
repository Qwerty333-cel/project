from faker import Faker
from django.utils.timezone import now
from django.db import transaction
from .functions import (
    UserManager, MealPlanManager, MealManager, 
    IngredientManager, DietTypeManager, FavoriteManager,
    PriceManager
)
from .models import DietTypes, User, MealPlans, Meals, Ingredients, Favorites

# Создание экземпляра Faker
fake = Faker()

def demonstrate_user_management():
    """Демонстрация работы с пользователями"""
    print("\n=== Демонстрация управления пользователями ===")
    
    # Создание пользователя
    user = UserManager.create_user(
        username=fake.user_name(),
        password="test123",
        email=fake.email(),
        weight=70.5,
        height=175,
        age=25
    )
    print(f"Создан пользователь: {user.username}")
    
    # Получение всех пользователей
    all_users = UserManager.get_all_users()
    print(f"Всего пользователей: {len(all_users)}")
    
    # Проверка пароля
    is_valid = UserManager.verify_password(user, "test123")
    print(f"Проверка пароля: {'успешно' if is_valid else 'неуспешно'}")

def demonstrate_meal_plan_management():
    """Демонстрация работы с планами питания"""
    print("\n=== Демонстрация управления планами питания ===")
    
    # Создание плана питания
    user = UserManager.get_all_users()[0]  # Берем первого пользователя
    meal_plan = MealPlanManager.create_meal_plan(
        user_id=user.id,
        duration=14,
        total_price=1000.0
    )
    print(f"Создан план питания на {meal_plan.duration} дней")
    
    # Получение всех планов
    all_plans = MealPlanManager.get_all_meal_plans()
    print(f"Всего планов питания: {len(all_plans)}")

def demonstrate_meal_management():
    """Демонстрация работы с блюдами"""
    print("\n=== Демонстрация управления блюдами ===")
    
    # Создание блюда
    meal = MealManager.create_meal(
        name="Салат Цезарь",
        price=15.99,
        description="Классический салат с курицей и сухариками",
        diet_type_id=1
    )
    print(f"Создано блюдо: {meal.name}")
    
    # Получение всех блюд
    all_meals = MealManager.get_all_meals()
    print(f"Всего блюд: {len(all_meals)}")

def demonstrate_ingredient_management():
    """Демонстрация работы с ингредиентами"""
    print("\n=== Демонстрация управления ингредиентами ===")
    
    # Создание ингредиента
    ingredient = IngredientManager.create_ingredient(
        name="Куриная грудка",
        price_per_unit=5.99,
        unit="кг",
        store_name="Ашан",
        valid_from=now()
    )
    print(f"Создан ингредиент: {ingredient.name}")
    
    # Получение всех ингредиентов
    all_ingredients = IngredientManager.get_all_ingredients()
    print(f"Всего ингредиентов: {len(all_ingredients)}")

def demonstrate_diet_type_management():
    """Демонстрация работы с типами диет"""
    print("\n=== Демонстрация управления типами диет ===")
    
    # Создание типа диеты
    diet_type = DietTypeManager.create_diet_type(
        name="Средиземноморская",
        is_restricted=False,
        description="Диета, основанная на традиционной кухне стран Средиземноморья"
    )
    print(f"Создан тип диеты: {diet_type.name}")
    
    # Получение всех типов диет
    all_diet_types = DietTypeManager.get_all_diet_types()
    print(f"Всего типов диет: {len(all_diet_types)}")

def demonstrate_favorite_management():
    """Демонстрация работы с избранными блюдами"""
    print("\n=== Демонстрация управления избранными блюдами ===")
    
    # Создание избранного блюда
    user = UserManager.get_all_users()[0]
    meal = MealManager.get_all_meals()[0]
    favorite = FavoriteManager.create_favorite(
        user_id=user.id,
        meal_id=meal.id
    )
    print(f"Добавлено в избранное: {meal.name}")
    
    # Получение всех избранных
    all_favorites = FavoriteManager.get_all_favorites()
    print(f"Всего избранных блюд: {len(all_favorites)}")

def demonstrate_price_management():
    """Демонстрация работы с ценами"""
    print("\n=== Демонстрация управления ценами ===")
    
    # Обновление цен всех блюд
    PriceManager.update_all_meal_prices()
    print("Цены всех блюд обновлены")
    
    # Обновление цен всех планов питания
    PriceManager.update_all_meal_plan_prices()
    print("Цены всех планов питания обновлены")

def main():
    """Основная функция для демонстрации всех возможностей"""
    try:
        with transaction.atomic():
            demonstrate_user_management()
            demonstrate_meal_plan_management()
            demonstrate_meal_management()
            demonstrate_ingredient_management()
            demonstrate_diet_type_management()
            demonstrate_favorite_management()
            demonstrate_price_management()
            
        print("\nВсе демонстрации успешно завершены!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()