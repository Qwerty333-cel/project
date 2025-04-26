from django.test import TestCase
from core.models import Meals, Ingredients, MealIngredient
from django.db.models import Sum

def calculate_meal_prices():
    # Получаем все блюда
    meals = Meals.objects.all()

    for meal in meals:
        print(f"Meal {meal.id}")

        # Получаем все ингредиенты для текущего блюда
        meal_ingredients = MealIngredient.objects.filter(meal=meal)

        price = 0
        for meal_ingr in meal_ingredients:
            # Получаем цену за единицу ингредиента
            ingredient_price = meal_ingr.ingredient.price_per_unit

            # Получаем количество ингредиента в блюде
            quantity = meal_ingr.quantity

            # Рассчитываем стоимость ингредиента в блюде
            price += ingredient_price * quantity

        print(price)

        # Устанавливаем рассчитанную стоимость для блюда
        meal.price = price
        meal.save()

    print("Стоимость всех блюд успешно обновлена.")