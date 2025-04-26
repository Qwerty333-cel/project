from django.db import models


class DietTypes(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)
    is_restricted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.TextField(unique=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class MealPlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    duration = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"Plan {self.id} for {self.user.username}"


class Meals(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True, blank=True, related_name="meals")

    # Many-to-Many relationships
    meal_plans = models.ManyToManyField(MealPlans, through='MealPlanMeal', related_name="meals")
    ingredients = models.ManyToManyField('Ingredients', through='MealIngredient', related_name="meals")

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.TextField(null=False)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    unit = models.CharField(max_length=20, null=False)
    store_name = models.TextField(null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, related_name="favorites")

    def __str__(self):
        return f"{self.user.username} likes {self.meal.name}"


class MealPlanMeal(models.Model):
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    plan = models.ForeignKey(MealPlans, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meal', 'plan'], name='unique_meal_plan')
        ]

    def __str__(self):
        return f"Meal {self.meal.name} in Plan {self.plan.id}"


class MealIngredient(models.Model):
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meal', 'ingredient'], name='unique_meal_ingredient')
        ]

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.meal.name}"