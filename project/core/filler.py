import os
import sys
import django # Первичный импорт Django, чтобы потом вызвать setup
# НЕ импортируем модели Django или вашего приложения здесь

# --- НАЧАЛО БЛОКА НАСТРОЙКИ DJANGO ---
# Определяем абсолютный путь к директории, содержащей этот скрипт (filler.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Определяем абсолютный путь к корневой директории вашего Django проекта.
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..')) 

# Добавляем корневую директорию проекта в sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
# ЗАМЕНИТЕ 'config.settings' на ваш актуальный путь к файлу настроек, если он другой.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup() # Инициализируем Django
except Exception as e:
    print(f"Критическая ошибка во время django.setup(): {e}")
    print(f"Рассчитанный project_root: {PROJECT_ROOT}")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print("Убедитесь, что filler.py находится в правильном месте (например, your_project_root/core/filler.py) "
          "и DJANGO_SETTINGS_MODULE указывает на ваш файл настроек.")
    sys.exit(1)
# --- КОНЕЦ БЛОКА НАСТРОЙКИ DJANGO ---

# ТЕПЕРЬ, ПОСЛЕ django.setup(), МОЖНО БЕЗОПАСНО ИМПОРТИРОВАТЬ ВСЕ ОСТАЛЬНОЕ
from django.db import transaction
from django.contrib.auth.models import User as DjangoUser # <--- ПЕРЕНЕСЕНО СЮДА
from faker import Faker
from faker_food import FoodProvider 
import random
from django.utils import timezone
from core.models import ( # <--- ПЕРЕНЕСЕНО СЮДА
    DietTypes, User, MealPlans, Meals, Ingredients, Favorites, 
    MealPlanMeal, MealIngredient
)


# --- Остальная часть вашего скрипта filler.py (функции и т.д.) ---
# (Код функций create_diet_types, create_users, populate_database и if __name__ == "__main__":
#  остается таким же, как в моем предыдущем полном ответе)


# Инициализация Faker
Faker.seed(1234) 
fake = Faker(['en_US']) 
fake.add_provider(FoodProvider) 

def generate_random_date_valid_from():
    """Генерирует случайную дату для поля valid_from (от полугода назад до месяца вперед)."""
    days_offset = random.randint(-180, 30) 
    return timezone.now() + timezone.timedelta(days=days_offset)

def generate_unique_username():
    """Генерирует уникальное имя пользователя, проверяя его отсутствие в DjangoUser."""
    while True:
        username = fake.user_name()
        if len(username) > 150: 
            username = username[:150]
        if not DjangoUser.objects.filter(username=username).exists():
            return username

def generate_unique_email():
    """Генерирует уникальный email, проверяя его отсутствие в DjangoUser."""
    while True:
        email = fake.email()
        if not DjangoUser.objects.filter(email=email).exists():
            return email

def create_diet_types(count=7):
    """Создает указанное количество типов диет с уникальными именами."""
    diet_types_list = []
    existing_names = set(DietTypes.objects.values_list('name', flat=True)) 
    for _ in range(count):
        name = ""
        for _i in range(100): 
            temp_name = fake.word().capitalize() + " Diet" 
            if temp_name not in existing_names: 
                name = temp_name
                break
        if not name: 
            name = f"Diet Type {fake.uuid4()[:8]}" 

        description = fake.sentence(nb_words=10)
        is_restricted = fake.boolean()
        
        diet_type = DietTypes.objects.create(
            name=name,
            description=description,
            is_restricted=is_restricted
        )
        diet_types_list.append(diet_type)
        existing_names.add(name) 
    return diet_types_list

def create_users(diet_types_list, count=20):
    """Создает указанное количество пользователей (DjangoUser и связанных кастомных User)."""
    users_list = []
    
    for _ in range(count):
        username = generate_unique_username()
        email = generate_unique_email()
        password = fake.password(length=random.randint(10,16), special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        weight = round(random.uniform(45.0, 120.0), 1)
        height = round(random.uniform(150.0, 200.0), 1)
        age = random.randint(18, 80)
        
        django_user = DjangoUser.objects.create_user( 
            username=username,
            email=email,
            password=password
        )
        
        chosen_diet_type = random.choice(diet_types_list) if diet_types_list else None
        
        user = User.objects.create( 
            django_user=django_user,
            weight=weight,
            height=height,
            age=age,
            diet_type=chosen_diet_type
        )
        users_list.append(user)
    return users_list

def create_meals(diet_types_list, count=30):
    """Создает указанное количество блюд."""
    meals_list = []
        
    for _ in range(count):
        name = fake.dish()
        if len(name) > 255: 
            name = name[:255] 
        description = fake.dish_description()
        if len(description) > 500: 
            description = description[:500]
        price = round(random.uniform(3.00, 60.00), 2) 
        
        chosen_diet_type = random.choice(diet_types_list) if diet_types_list else None

        meal = Meals.objects.create(
            name=name,
            description=description,
            price=price,
            diet_type=chosen_diet_type
        )
        meals_list.append(meal)
    return meals_list

def create_meal_plans(users_list, meals_list, count=15):
    """Создает планы питания и связывает их с блюдами через MealPlanMeal."""
    meal_plans_list = []
    if not users_list or not meals_list: 
        print("Предупреждение: Невозможно создать планы питания без пользователей или блюд.")
        return meal_plans_list

    for _ in range(count):
        user_for_plan = random.choice(users_list)
        duration_days = random.randint(3, 28) 
        total_plan_price = round(random.uniform(20.0, 600.0), 1) 

        meal_plan = MealPlans.objects.create(
            user=user_for_plan,
            duration=duration_days,
            total_price=total_plan_price 
        )
        
        num_meals_in_plan = 0
        if meals_list: 
            num_meals_in_plan = random.randint(1, min(7, len(meals_list))) 
        
        if num_meals_in_plan > 0:
            selected_meals_for_plan = random.sample(meals_list, k=num_meals_in_plan)
            for meal_item in selected_meals_for_plan:
                try: 
                    MealPlanMeal.objects.create(plan=meal_plan, meal=meal_item)
                except django.db.utils.IntegrityError: 
                    print(f"Блюдо {meal_item.name} уже в плане {meal_plan.id}. Пропускаем.")
                except Exception as e:
                    print(f"Ошибка добавления блюда {meal_item.name} в план {meal_plan.id}: {e}")
        
        meal_plans_list.append(meal_plan)
    return meal_plans_list

def create_favorites(users_list, meals_list, count=30):
    """Создает указанное количество записей в избранном, избегая дубликатов."""
    if not users_list or not meals_list:
        print("Предупреждение: Невозможно создать избранное без пользователей или блюд.")
        return

    created_count = 0
    attempts = 0
    max_total_attempts = count * len(users_list) * len(meals_list) if users_list and meals_list else count * 10
    
    while created_count < count and attempts < max_total_attempts :
        user = random.choice(users_list)
        meal = random.choice(meals_list)
        attempts += 1
        
        try: 
            _, created = Favorites.objects.get_or_create(user=user, meal=meal)
            if created:
                created_count += 1
        except Exception as e: 
            print(f"Ошибка создания избранного для Пользователя {user.id}, Блюда {meal.id}: {e}")
            
    print(f"Создано {created_count} уникальных записей в избранном.")


def create_ingredients(count=40):
    """Создает указанное количество ингредиентов."""
    ingredients_list = []
    for _ in range(count):
        base_word = fake.word().capitalize()
        food_suffix = fake.ingredient()
        if len(food_suffix) > 50:
            food_suffix = food_suffix[:50]  
        name = f"{base_word} {food_suffix}"
        if len(name) > 255 : name = name[:255] 

        price_per_unit = round(random.uniform(0.20, 25.00), 2)
        unit = random.choice(['kg', 'g', 'l', 'ml', 'piece', 'tbsp', 'tsp', 'cup', 'oz'])
        store_name = fake.company() if fake.boolean(chance_of_getting_true=70) else None 
        
        ingredient = Ingredients.objects.create(
            name=name,
            price_per_unit=price_per_unit,
            unit=unit,
            store_name=store_name,
            valid_from=generate_random_date_valid_from() 
        )
        ingredients_list.append(ingredient)
    return ingredients_list

def create_meal_ingredients(meals_list, ingredients_list):
    """Связывает блюда с ингредиентами через MealIngredient, указывая количество."""
    if not meals_list or not ingredients_list:
        print("Предупреждение: Невозможно создать ингредиенты блюд без блюд или ингредиентов.")
        return

    for meal in meals_list:
        if not ingredients_list: continue 

        max_k = min(8, len(ingredients_list)) 
        min_k = min(1, len(ingredients_list)) 
        if min_k > max_k : continue 
        
        num_ingredients_in_meal = random.randint(min_k, max_k)
        
        selected_ingredients_for_meal = random.sample(ingredients_list, k=num_ingredients_in_meal)
        for ingredient in selected_ingredients_for_meal:
            if ingredient.unit in ['kg', 'l']:
                quantity = round(random.uniform(0.05, 0.75), 2) 
            elif ingredient.unit in ['g', 'ml']:
                quantity = round(random.uniform(10, 250), 1)
            elif ingredient.unit == 'piece':
                quantity = random.randint(1, 5)
            else: 
                quantity = round(random.uniform(0.5, 4), 1)
            
            try: 
                MealIngredient.objects.create(
                    meal=meal,
                    ingredient=ingredient,
                    quantity=quantity
                )
            except django.db.utils.IntegrityError: 
                 print(f"Ингредиент {ingredient.name} уже в блюде {meal.name}. Пропускаем.")
            except Exception as e:
                print(f"Ошибка добавления ингредиента {ingredient.name} в блюдо {meal.name}: {e}")

@transaction.atomic 
def populate_database():
    """Основная функция для заполнения базы данных тестовыми данными."""
    print("Запуск процесса заполнения базы данных...")
    
    diet_types = create_diet_types(count=6) 
    print(f"Создано {len(diet_types)} типов диет.")

    users = create_users(diet_types, count=15) 
    print(f"Создано {len(users)} пользователей.")

    meals = create_meals(diet_types, count=40) 
    print(f"Создано {len(meals)} блюд.")
    
    if users and meals: 
        meal_plans = create_meal_plans(users, meals, count=10)
        if meal_plans: 
             print(f"Создано {len(meal_plans)} планов питания.")
        create_favorites(users, meals, count=25) 
    else:
        print("Пропуск создания планов питания и избранного из-за отсутствия пользователей или блюд.")

    ingredients = create_ingredients(count=50) 
    print(f"Создано {len(ingredients)} ингредиентов.")

    if meals and ingredients: 
        create_meal_ingredients(meals, ingredients)
        print("Ингредиенты добавлены к блюдам.")
    else:
        print("Пропуск добавления ингредиентов к блюдам из-за отсутствия блюд или ингредиентов.")

    print("\nПроцесс заполнения базы данных завершен.")
    print(f"Сводка:")
    print(f"- Типы диет: {DietTypes.objects.count()}")
    print(f"- Пользователи (Django): {DjangoUser.objects.count()}")
    print(f"- Пользователи (Кастомные): {User.objects.count()}")
    print(f"- Блюда: {Meals.objects.count()}")
    print(f"- Планы питания: {MealPlans.objects.count()}")
    print(f"- Ингредиенты: {Ingredients.objects.count()}")
    print(f"- Избранное: {Favorites.objects.count()}")
    print(f"- Записи MealPlanMeal: {MealPlanMeal.objects.count()}")
    print(f"- Записи MealIngredient: {MealIngredient.objects.count()}")


if __name__ == "__main__":
    print("Запуск заполнителя базы данных...")
    try:
        populate_database()
        print("\nБаза данных успешно заполнена тестовыми данными!")
    except Exception as e:
        print(f"\nОшибка во время заполнения базы данных: {e}")
        import traceback
        traceback.print_exc() 
    print("Скрипт заполнителя базы данных завершил работу.")