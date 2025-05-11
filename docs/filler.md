# Документация файла filler.py

## Общее описание
Файл `filler.py` - это скрипт для заполнения базы данных тестовыми данными. Он использует библиотеку Faker для генерации реалистичных данных и создает связанные записи в различных таблицах базы данных.

## Структура файла

### Импорты и настройка окружения
```python
import os
import sys
import django
from django.db import transaction
from core.models import DietTypes, User, MealPlans, Meals, Ingredients, Favorites, MealPlanMeal, MealIngredient
from django.contrib.auth.models import User as DjangoUser
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone
```
- Настраивает окружение Django
- Импортирует необходимые модели и утилиты
- Инициализирует Faker с фиксированным seed для воспроизводимости

### Вспомогательные функции

#### Генерация случайной даты
```python
def generate_random_date():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    return fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=timezone.get_current_timezone())
```
- Генерирует случайную дату за последний год
- Учитывает часовой пояс

#### Генерация уникальных данных пользователя
```python
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
```
- Генерируют уникальные username, email и хеш пароля
- Проверяют существование в базе данных

### Основные функции генерации данных

#### Создание типов диет
```python
def create_diet_types():
    diet_types = []
    for _ in range(7):
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
```
- Создает 7 случайных типов диет
- Генерирует название, описание и флаг ограничений

#### Создание пользователей
```python
def create_users(diet_types):
    users = []
    for _ in range(20):
        username = generate_unique_username()
        email = generate_unique_email()
        password = fake.password(length=12)
        
        weight = round(random.uniform(45, 120), 1)
        height = round(random.uniform(150, 200), 1)
        age = random.randint(18, 80)
        
        django_user = DjangoUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        user = User.objects.create(
            django_user=django_user,
            weight=weight,
            height=height,
            age=age,
            diet_type=random.choice(diet_types)
        )
        
        users.append(user)
    return users
```
- Создает 20 пользователей
- Генерирует физические характеристики
- Создает связанные записи в Django и пользовательской модели

#### Создание блюд
```python
def create_meals(diet_types):
    meals = []
    for _ in range(30):
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
```
- Создает 30 случайных блюд
- Генерирует название, описание и цену
- Связывает с типом диеты

#### Создание планов питания
```python
def create_meal_plans(users, meals):
    meal_plans = []
    for _ in range(15):
        duration = random.randint(7, 30)
        total_price = round(random.uniform(50, 500), 2)
        
        meal_plan = MealPlans.objects.create(
            user=random.choice(users),
            duration=duration,
            total_price=total_price
        )
        
        selected_meals = random.sample(meals, k=random.randint(1, 5))
        meal_plan.meals.add(*selected_meals)
        meal_plans.append(meal_plan)
    return meal_plans
```
- Создает 15 планов питания
- Связывает с пользователем и случайными блюдами
- Генерирует длительность и общую стоимость

#### Создание избранных блюд
```python
def create_favorites(users, meals):
    created_pairs = set()
    attempts = 0
    max_attempts = 100
    
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
```
- Создает до 30 уникальных избранных блюд
- Отслеживает уже созданные пары пользователь-блюдо
- Ограничивает количество попыток

#### Создание ингредиентов
```python
def create_ingredients():
    ingredients = []
    for _ in range(40):
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
```
- Создает 40 случайных ингредиентов
- Генерирует название, цену, единицу измерения и магазин
- Устанавливает дату начала действия

#### Создание связей блюд с ингредиентами
```python
def create_meal_ingredients(meals, ingredients):
    for meal in meals:
        selected_ingredients = random.sample(ingredients, k=random.randint(3, 8))
        for ingredient in selected_ingredients:
            if ingredient.unit in ['kg', 'l']:
                quantity = round(random.uniform(0.1, 1.0), 2)
            else:
                quantity = round(random.uniform(1, 10), 2)
                
            MealIngredient.objects.create(
                meal=meal,
                ingredient=ingredient,
                quantity=quantity
            )
```
- Добавляет 3-8 случайных ингредиентов к каждому блюду
- Генерирует количество в зависимости от единицы измерения

### Основная функция
```python
def populate_database():
    try:
        with transaction.atomic():
            # Создание всех данных в правильном порядке
            diet_types = create_diet_types()
            users = create_users(diet_types)
            meals = create_meals(diet_types)
            meal_plans = create_meal_plans(users, meals)
            create_favorites(users, meals)
            ingredients = create_ingredients()
            create_meal_ingredients(meals, ingredients)
            
            # Вывод статистики
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
```
- Координирует создание всех данных
- Использует транзакции для обеспечения целостности
- Выводит статистику созданных данных

## Использование
1. Скрипт может быть запущен напрямую:
   ```bash
   python core/filler.py
   ```
2. Или импортирован и использован в другом коде:
   ```python
   from core.filler import populate_database
   populate_database()
   ```

## Примечания
- Скрипт использует фиксированный seed для Faker, что обеспечивает воспроизводимость данных
- Все операции выполняются в рамках одной транзакции
- При ошибке все изменения откатываются
- Генерируются реалистичные данные с учетом связей между моделями
- Количество создаваемых записей можно легко изменить
- Рекомендуется использовать только в тестовом окружении 