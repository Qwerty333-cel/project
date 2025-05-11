from faker import Faker
from django.db.models import Sum
from core.models import (
    User, MealPlans, Meals, Ingredients, MealIngredient,
    DietTypes, Favorites, MealPlanMeal
)
from django.db import transaction
from typing import Optional, List, Dict, Any
from datetime import datetime
from django.contrib.auth.models import User as DjangoUser

# Инициализация Faker
fake = Faker()


class UserManager:
    """Класс для управления пользователями"""
    
    @staticmethod
    def create_user(
        username: str,
        password: str,
        email: str,
        weight: Optional[float] = None,
        height: Optional[float] = None,
        age: Optional[int] = None,
        diet_type_id: Optional[int] = None
    ) -> User:
        """Создает нового пользователя"""
        # Create Django user first
        django_user = DjangoUser.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Create our custom user
        user = User.objects.create(
            django_user=django_user,
            weight=weight,
            height=height,
            age=age,
            diet_type_id=diet_type_id
        )
        
        # Profile will be created automatically by the signal
        return user

    @staticmethod
    def update_password(user: User, password: str) -> None:
        """Обновляет пароль пользователя"""
        user.django_user.set_password(password)
        user.django_user.save()

    @staticmethod
    def get_all_users() -> List[User]:
        """Возвращает список всех пользователей"""
        return list(User.objects.all())

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Находит пользователя по ID"""
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Удаляет пользователя по ID"""
        user = UserManager.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        """Проверяет пароль пользователя"""
        return user.django_user.check_password(password)


class MealPlanManager:
    """Класс для управления планами питания"""
    
    @staticmethod
    def create_meal_plan(
        user_id: int,
        duration: int,
        total_price: Optional[float] = None
    ) -> MealPlans:
        """Создает новый план питания"""
        return MealPlans.objects.create(
            user_id=user_id,
            duration=duration,
            total_price=total_price
        )

    @staticmethod
    def get_all_meal_plans() -> List[MealPlans]:
        """Возвращает список всех планов питания"""
        return list(MealPlans.objects.all())

    @staticmethod
    def get_meal_plan_by_id(plan_id: int) -> Optional[MealPlans]:
        """Находит план питания по ID"""
        return MealPlans.objects.filter(id=plan_id).first()

    @staticmethod
    def delete_meal_plan(plan_id: int) -> bool:
        """Удаляет план питания по ID"""
        meal_plan = MealPlanManager.get_meal_plan_by_id(plan_id)
        if meal_plan:
            meal_plan.delete()
            return True
        return False

    @staticmethod
    def calculate_plan_price(plan_id: int) -> float:
        """Рассчитывает стоимость плана питания"""
        plan = MealPlanManager.get_meal_plan_by_id(plan_id)
        if not plan:
            return 0.0
        return plan.meals.aggregate(total_price=Sum('price'))['total_price'] or 0.0


class MealManager:
    """Класс для управления блюдами"""
    
    @staticmethod
    def create_meal(
        name: str,
        price: float,
        description: Optional[str] = None,
        diet_type_id: Optional[int] = None
    ) -> Meals:
        """Создает новое блюдо"""
        return Meals.objects.create(
            name=name,
            description=description,
            price=price,
            diet_type_id=diet_type_id
        )

    @staticmethod
    def get_all_meals() -> List[Meals]:
        """Возвращает список всех блюд"""
        return list(Meals.objects.all())

    @staticmethod
    def get_meal_by_id(meal_id: int) -> Optional[Meals]:
        """Находит блюдо по ID"""
        return Meals.objects.filter(id=meal_id).first()

    @staticmethod
    def delete_meal(meal_id: int) -> bool:
        """Удаляет блюдо по ID"""
        meal = MealManager.get_meal_by_id(meal_id)
        if meal:
            meal.delete()
            return True
        return False

    @staticmethod
    def calculate_meal_price(meal_id: int) -> float:
        """Рассчитывает стоимость блюда на основе ингредиентов"""
        meal = MealManager.get_meal_by_id(meal_id)
        if not meal:
            return 0.0
        
        total_price = 0.0
        for meal_ingr in MealIngredient.objects.filter(meal=meal):
            total_price += meal_ingr.ingredient.price_per_unit * meal_ingr.quantity
        return total_price


class IngredientManager:
    """Класс для управления ингредиентами"""
    
    @staticmethod
    def create_ingredient(
        name: str,
        price_per_unit: float,
        unit: str,
        store_name: Optional[str] = None,
        valid_from: Optional[datetime] = None
    ) -> Ingredients:
        """Создает новый ингредиент"""
        return Ingredients.objects.create(
            name=name,
            price_per_unit=price_per_unit,
            unit=unit,
            store_name=store_name,
            valid_from=valid_from
        )

    @staticmethod
    def get_all_ingredients() -> List[Ingredients]:
        """Возвращает список всех ингредиентов"""
        return list(Ingredients.objects.all())

    @staticmethod
    def get_ingredient_by_id(ingredient_id: int) -> Optional[Ingredients]:
        """Находит ингредиент по ID"""
        return Ingredients.objects.filter(id=ingredient_id).first()

    @staticmethod
    def delete_ingredient(ingredient_id: int) -> bool:
        """Удаляет ингредиент по ID"""
        ingredient = IngredientManager.get_ingredient_by_id(ingredient_id)
        if ingredient:
            ingredient.delete()
            return True
        return False


class DietTypeManager:
    """Класс для управления типами диет"""
    
    @staticmethod
    def create_diet_type(
        name: str,
        is_restricted: bool,
        description: Optional[str] = None
    ) -> DietTypes:
        """Создает новый тип диеты"""
        return DietTypes.objects.create(
            name=name,
            description=description,
            is_restricted=is_restricted
        )

    @staticmethod
    def get_all_diet_types() -> List[DietTypes]:
        """Возвращает список всех типов диет"""
        return list(DietTypes.objects.all())

    @staticmethod
    def get_diet_type_by_id(diet_type_id: int) -> Optional[DietTypes]:
        """Находит тип диеты по ID"""
        return DietTypes.objects.filter(id=diet_type_id).first()

    @staticmethod
    def delete_diet_type(diet_type_id: int) -> bool:
        """Удаляет тип диеты по ID"""
        diet_type = DietTypeManager.get_diet_type_by_id(diet_type_id)
        if diet_type:
            diet_type.delete()
            return True
        return False


class FavoriteManager:
    """Класс для управления избранными блюдами"""
    
    @staticmethod
    def create_favorite(user_id: int, meal_id: int) -> Favorites:
        """Добавляет блюдо в избранное"""
        return Favorites.objects.create(
            user_id=user_id,
            meal_id=meal_id
        )

    @staticmethod
    def get_all_favorites() -> List[Favorites]:
        """Возвращает список всех избранных блюд"""
        return list(Favorites.objects.all())

    @staticmethod
    def get_favorite_by_id(favorite_id: int) -> Optional[Favorites]:
        """Находит избранное блюдо по ID"""
        return Favorites.objects.filter(id=favorite_id).first()

    @staticmethod
    def delete_favorite(favorite_id: int) -> bool:
        """Удаляет блюдо из избранного"""
        favorite = FavoriteManager.get_favorite_by_id(favorite_id)
        if favorite:
            favorite.delete()
            return True
        return False


class PriceManager:
    """Класс для управления ценами"""
    
    @staticmethod
    def update_all_meal_prices() -> None:
        """Обновляет цены всех блюд"""
        for meal in MealManager.get_all_meals():
            meal.price = MealManager.calculate_meal_price(meal.id)
            meal.save()
        print("Стоимость всех блюд успешно обновлена.")

    @staticmethod
    def update_all_meal_plan_prices() -> None:
        """Обновляет цены всех планов питания"""
        for plan in MealPlanManager.get_all_meal_plans():
            plan.total_price = MealPlanManager.calculate_plan_price(plan.id)
            plan.save()
        print("Стоимость всех планов питания успешно обновлена.")


# Пример использования
if __name__ == "__main__":
    # Обновляем цены
    PriceManager.update_all_meal_prices()
    PriceManager.update_all_meal_plan_prices()

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