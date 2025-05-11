from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class DietTypes(models.Model):
    name = models.TextField(null=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    is_restricted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']
        verbose_name = 'Diet Type'
        verbose_name_plural = 'Diet Types'

    def __str__(self):
        return self.name


class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='custom_user')
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.django_user.username

    @property
    def email(self):
        return self.django_user.email

    @property
    def username(self):
        return self.django_user.username


class Profile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    site_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=DjangoUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=DjangoUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MealPlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    duration = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Plan {self.id} for {self.user.username}"


class Meals(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    diet_type = models.ForeignKey(DietTypes, on_delete=models.SET_NULL, null=True, blank=True, related_name="meals")
    created_at = models.DateTimeField(default=timezone.now)

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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'meal'], name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.meal.name}"


class MealPlanMeal(models.Model):
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    plan = models.ForeignKey(MealPlans, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

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
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meal', 'ingredient'], name='unique_meal_ingredient')
        ]

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.meal.name}"
