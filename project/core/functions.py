from faker import Faker
from django.db.models import Sum
from core.models import (
    User, MealPlans, Meals, Ingredients, MealIngredient,
    DietTypes, Favorites, MealPlanMeal
)
from werkzeug.security import generate_password_hash, check_password_hash
from django.db import transaction

# Создание экземпляра Faker
fake = Faker()


def set_meal_price():
    # Получаем все блюда
    meals = Meals.objects.all()

    for meal in meals:
        # Получаем все ингредиенты для текущего блюда
        meal_ingredients = MealIngredient.objects.filter(meal=meal)

        price = 0
        for meal_ingr in meal_ingredients:
            # Рассчитываем стоимость ингредиента в блюде
            ingredient_price = meal_ingr.ingredient.price_per_unit
            quantity = meal_ingr.quantity
            price += ingredient_price * quantity

        # Устанавливаем рассчитанную стоимость для блюда
        meal.price = price
        meal.save()

    print("Стоимость всех блюд успешно обновлена.")


# Расчёт цен планов питания
def set_mealplan_prices():
    # Получаем все планы питания
    meal_plans = MealPlans.objects.all()

    for plan in meal_plans:
        # Рассчитываем общую стоимость плана питания
        total_price = plan.meals.aggregate(total_price=Sum('price'))['total_price'] or 0

        # Устанавливаем стоимость плана питания
        plan.total_price = total_price
        plan.save()

    print("Стоимость всех планов питания успешно обновлена.")


# Вывод планов питания и их стоимость у конкретного пользователя
def get_user_meals(username):
    # Находим пользователя по username
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"Пользователь с username '{username}' не найден.")
        return

    # Получаем все планы питания пользователя
    meal_plans = MealPlans.objects.filter(user=user)

    if not meal_plans.exists():
        print(f"У пользователя '{username}' нет планов питания.")
        return

    print(f"Планы питания пользователя '{username}':")
    for plan in meal_plans:
        print(f"- План ID: {plan.id}, Длительность: {plan.duration} дней, Стоимость: {plan.total_price}")


# Пример использования функций
if __name__ == "__main__":
    # Обновляем цены блюд
    set_meal_price()

    # Обновляем цены планов питания
    set_mealplan_prices()

    # Выводим планы питания для конкретного пользователя
    get_user_meals('davidreed')

# Функции для User
def create_user(username: str, password: str, email: str, 
                weight: float = None, height: float = None, age: int = None, diet_type_id: int = None):
    user = User.objects.create(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        weight=weight,
        height=height,
        age=age,
        diet_type_id=diet_type_id
    )
    return user

def get_all_users():
    return User.objects.all()

def get_user_by_id(user_id: int):
    return User.objects.filter(id=user_id).first()

def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        user.delete()
        return True
    return False

def verify_user_password(user: User, password: str) -> bool:
    return check_password_hash(user.password_hash, password)

# Функции для MealPlans
def create_meal_plan(user_id: int, duration: int, total_price: float = None):
    meal_plan = MealPlans.objects.create(
        user_id=user_id,
        duration=duration,
        total_price=total_price
    )
    return meal_plan

def get_all_meal_plans():
    return MealPlans.objects.all()

def get_meal_plan_by_id(plan_id: int):
    return MealPlans.objects.filter(id=plan_id).first()

def delete_meal_plan(plan_id: int):
    meal_plan = get_meal_plan_by_id(plan_id)
    if meal_plan:
        meal_plan.delete()
        return True
    return False

# Функции для Favorites
def create_favorite(user_id: int, meal_id: int):
    favorite = Favorites.objects.create(
        user_id=user_id,
        meal_id=meal_id
    )
    return favorite

def get_all_favorites():
    return Favorites.objects.all()

def get_favorite_by_id(favorite_id: int):
    return Favorites.objects.filter(id=favorite_id).first()

def delete_favorite(favorite_id: int):
    favorite = get_favorite_by_id(favorite_id)
    if favorite:
        favorite.delete()
        return True
    return False

# Функции для Meals
def create_meal(name: str, price: float, description: str = None, diet_type_id: int = None):
    meal = Meals.objects.create(
        name=name,
        description=description,
        price=price,
        diet_type_id=diet_type_id
    )
    return meal

def get_all_meals():
    return Meals.objects.all()

def get_meal_by_id(meal_id: int):
    return Meals.objects.filter(id=meal_id).first()

def delete_meal(meal_id: int):
    meal = get_meal_by_id(meal_id)
    if meal:
        meal.delete()
        return True
    return False

# Функции для Ingredients
def create_ingredient(name: str, price_per_unit: float, unit: str,
                      store_name: str = None, valid_from: str = None):
    ingredient = Ingredients.objects.create(
        name=name,
        price_per_unit=price_per_unit,
        unit=unit,
        store_name=store_name,
        valid_from=valid_from
    )
    return ingredient

def get_all_ingredients():
    return Ingredients.objects.all()

def get_ingredient_by_id(ingredient_id: int):
    return Ingredients.objects.filter(id=ingredient_id).first()

def delete_ingredient(ingredient_id: int):
    ingredient = get_ingredient_by_id(ingredient_id)
    if ingredient:
        ingredient.delete()
        return True
    return False

# Функции для DietTypes
def create_diet_type(name: str, is_restricted: bool, description: str = None):
    diet_type = DietTypes.objects.create(
        name=name,
        description=description,
        is_restricted=is_restricted
    )
    return diet_type

def get_all_diet_types():
    return DietTypes.objects.all()

def get_diet_type_by_id(diet_type_id: int):
    return DietTypes.objects.filter(id=diet_type_id).first()

def delete_diet_type(diet_type_id: int):
    diet_type = get_diet_type_by_id(diet_type_id)
    if diet_type:
        diet_type.delete()
        return True
    return False