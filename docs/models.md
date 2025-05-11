# Документация файла models.py

## Общее описание
Файл `models.py` содержит определения моделей Django для приложения. Модели представляют структуру базы данных и определяют отношения между различными сущностями системы.

## Структура файла

### Импорты
```python
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
```

### DietTypes
```python
class DietTypes(models.Model):
    name = models.TextField(null=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    is_restricted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
```
- Модель для типов диет
- Содержит название, описание и флаг ограничений
- Имеет индекс по названию
- Отслеживает время создания

### User
```python
class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    age = models.PositiveIntegerField(null=True)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True)
```
- Расширяет стандартную модель пользователя Django
- Содержит физические параметры пользователя
- Связана с типом диеты
- Имеет свойства для доступа к email и username

### Profile
```python
class Profile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    site_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
```
- Профиль пользователя
- Связан с пользователем Django и пользователем сайта
- Создается автоматически при создании пользователя

### MealPlans
```python
class MealPlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=1, null=True)
```
- Планы питания пользователей
- Содержит длительность и общую стоимость
- Связан с пользователем

### Meals
```python
class Meals(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True)
```
- Блюда
- Содержит название, описание и цену
- Связано с типом диеты
- Имеет связи многие-ко-многим с планами и ингредиентами

### Ingredients
```python
class Ingredients(models.Model):
    name = models.TextField(null=False)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    unit = models.CharField(max_length=20, null=False)
    store_name = models.TextField(null=True)
    valid_from = models.DateTimeField(null=True)
```
- Ингредиенты
- Содержит название, цену за единицу и единицу измерения
- Включает информацию о магазине и дате начала действия

### Favorites
```python
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
```
- Избранные блюда пользователей
- Имеет уникальное ограничение на пару пользователь-блюдо

### MealPlanMeal
```python
class MealPlanMeal(models.Model):
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    plan = models.ForeignKey(MealPlans, on_delete=models.CASCADE)
```
- Связующая модель для планов питания и блюд
- Имеет уникальное ограничение на пару план-блюдо

### MealIngredient
```python
class MealIngredient(models.Model):
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, null=False)
```
- Связующая модель для блюд и ингредиентов
- Содержит количество ингредиента
- Имеет уникальное ограничение на пару блюдо-ингредиент

## Сигналы
```python
@receiver(post_save, sender=DjangoUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=DjangoUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```
- Автоматически создают и сохраняют профиль при создании пользователя

## Примечания
- Все модели имеют поле created_at для отслеживания времени создания
- Используются каскадные удаления для связанных объектов
- Применяются уникальные ограничения для предотвращения дублирования
- Модели используют различные типы полей для разных данных
- Реализованы связи один-к-одному, один-ко-многим и многие-ко-многим
- Все модели имеют метод __str__ для удобного отображения 