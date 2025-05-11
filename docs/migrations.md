# Документация миграций базы данных

## Общее описание
Файл `0001_initial.py` содержит начальную миграцию базы данных, которая создает все необходимые таблицы и связи для работы приложения. Миграция была сгенерирована Django 5.0.2 и определяет структуру базы данных для всех моделей приложения.

## Структура миграции

### Зависимости
```python
dependencies = [
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]
```
- Зависит от стандартной модели пользователя Django

### Операции миграции

#### Создание таблицы DietTypes
```python
migrations.CreateModel(
    name='DietTypes',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.TextField(db_index=True)),
        ('description', models.TextField(blank=True, null=True)),
        ('is_restricted', models.BooleanField(default=False)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
    ],
    options={
        'verbose_name': 'Diet Type',
        'verbose_name_plural': 'Diet Types',
        'ordering': ['name'],
    },
)
```
- Создает таблицу для типов диет
- Включает поля: название, описание, флаг ограничений
- Добавляет индекс для поля name
- Устанавливает сортировку по умолчанию

#### Создание таблицы Ingredients
```python
migrations.CreateModel(
    name='Ingredients',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.TextField()),
        ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
        ('unit', models.CharField(max_length=20)),
        ('store_name', models.TextField(blank=True, null=True)),
        ('valid_from', models.DateTimeField(blank=True, null=True)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
    ],
)
```
- Создает таблицу для ингредиентов
- Включает поля: название, цена за единицу, единица измерения, магазин
- Добавляет временные метки для валидности и создания

#### Создание таблицы MealPlans
```python
migrations.CreateModel(
    name='MealPlans',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('duration', models.PositiveIntegerField()),
        ('total_price', models.DecimalField(blank=True, decimal_places=1, max_digits=12, null=True)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
    ],
)
```
- Создает таблицу для планов питания
- Включает поля: длительность, общая стоимость
- Добавляет временную метку создания

#### Создание таблицы MealIngredient
```python
migrations.CreateModel(
    name='MealIngredient',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ingredients')),
    ],
)
```
- Создает таблицу для связи блюд с ингредиентами
- Включает поля: количество, временная метка
- Устанавливает внешний ключ на ингредиент

#### Создание таблицы MealPlanMeal
```python
migrations.CreateModel(
    name='MealPlanMeal',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.mealplans')),
    ],
)
```
- Создает таблицу для связи планов питания с блюдами
- Включает временную метку
- Устанавливает внешний ключ на план питания

#### Создание таблицы Meals
```python
migrations.CreateModel(
    name='Meals',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.TextField()),
        ('description', models.TextField(blank=True, null=True)),
        ('price', models.DecimalField(decimal_places=2, max_digits=10)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('diet_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meals', to='core.diettypes')),
        ('ingredients', models.ManyToManyField(related_name='meals', through='core.MealIngredient', to='core.ingredients')),
        ('meal_plans', models.ManyToManyField(related_name='meals', through='core.MealPlanMeal', to='core.mealplans')),
    ],
)
```
- Создает таблицу для блюд
- Включает поля: название, описание, цена
- Устанавливает связи с типами диет, ингредиентами и планами питания

#### Создание таблицы User
```python
migrations.CreateModel(
    name='User',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('weight', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
        ('height', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
        ('age', models.PositiveIntegerField(blank=True, null=True)),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('diet_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='core.diettypes')),
        ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='custom_user', to=settings.AUTH_USER_MODEL)),
    ],
    options={
        'verbose_name': 'User',
        'verbose_name_plural': 'Users',
        'ordering': ['-created_at'],
    },
)
```
- Создает таблицу для пользователей
- Включает поля: вес, рост, возраст
- Устанавливает связи с типом диеты и стандартным пользователем Django

#### Создание таблицы Profile
```python
migrations.CreateModel(
    name='Profile',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
        ('site_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='core.user')),
    ],
)
```
- Создает таблицу для профилей пользователей
- Устанавливает связи с пользователями Django и приложения

#### Создание таблицы Favorites
```python
migrations.CreateModel(
    name='Favorites',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='core.meals')),
        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='core.user')),
    ],
)
```
- Создает таблицу для избранных блюд
- Устанавливает связи с пользователями и блюдами

### Ограничения уникальности
```python
migrations.AddConstraint(
    model_name='mealplanmeal',
    constraint=models.UniqueConstraint(fields=('meal', 'plan'), name='unique_meal_plan'),
),
migrations.AddConstraint(
    model_name='mealingredient',
    constraint=models.UniqueConstraint(fields=('meal', 'ingredient'), name='unique_meal_ingredient'),
),
migrations.AddConstraint(
    model_name='favorites',
    constraint=models.UniqueConstraint(fields=('user', 'meal'), name='unique_favorite'),
)
```
- Добавляет ограничения уникальности для связей
- Предотвращает дублирование записей

## Использование
1. Применение миграции:
   ```bash
   python manage.py migrate
   ```

2. Откат миграции:
   ```bash
   python manage.py migrate core zero
   ```

## Примечания
- Миграция создает все необходимые таблицы и связи
- Используются каскадные удаления для связанных записей
- Добавлены индексы для оптимизации запросов
- Установлены ограничения уникальности
- Все таблицы включают временные метки
- Используются внешние ключи для обеспечения целостности данных 