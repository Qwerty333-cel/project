# Generated by Django 5.2 on 2025-04-19 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DietTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('is_restricted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=20)),
                ('store_name', models.TextField(blank=True, null=True)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(blank=True, decimal_places=1, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='MealPlanMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.mealplans')),
            ],
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('diet_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meals', to='core.diettypes')),
                ('ingredients', models.ManyToManyField(related_name='meals', through='core.MealIngredient', to='core.ingredients')),
                ('meal_plans', models.ManyToManyField(related_name='meals', through='core.MealPlanMeal', to='core.mealplans')),
            ],
        ),
        migrations.AddField(
            model_name='mealplanmeal',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.meals'),
        ),
        migrations.AddField(
            model_name='mealingredient',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.meals'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.TextField(unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('diet_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='core.diettypes')),
            ],
        ),
        migrations.AddField(
            model_name='mealplans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_plans', to='core.user'),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='core.meals')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='core.user')),
            ],
        ),
        migrations.AddConstraint(
            model_name='mealplanmeal',
            constraint=models.UniqueConstraint(fields=('meal', 'plan'), name='unique_meal_plan'),
        ),
        migrations.AddConstraint(
            model_name='mealingredient',
            constraint=models.UniqueConstraint(fields=('meal', 'ingredient'), name='unique_meal_ingredient'),
        ),
    ]
