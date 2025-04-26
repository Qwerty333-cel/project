from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, MealPlanViewSet, MealViewSet,
    IngredientViewSet, DietTypeViewSet, FavoriteViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('meal-plans', MealPlanViewSet, basename='meal-plan')
router.register('meals', MealViewSet, basename='meal')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('diet-types', DietTypeViewSet, basename='diet-type')
router.register('favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
] 