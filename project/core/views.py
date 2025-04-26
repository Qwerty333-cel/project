from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import (
    UserManager, MealPlanManager, MealManager,
    IngredientManager, DietTypeManager, FavoriteManager,
    PriceManager
)
from .serializers import (
    UserSerializer, MealPlanSerializer, MealSerializer,
    IngredientSerializer, DietTypeSerializer, FavoriteSerializer
)

# Create your views here.

class UserViewSet(viewsets.ViewSet):
    """API endpoint для управления пользователями"""
    
    def list(self, request):
        """Получить список всех пользователей"""
        users = UserManager.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Создать нового пользователя"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserManager.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                weight=serializer.validated_data.get('weight'),
                height=serializer.validated_data.get('height'),
                age=serializer.validated_data.get('age'),
                diet_type_id=serializer.validated_data.get('diet_type_id')
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном пользователе"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Обновить информацию о пользователе"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """Частично обновить информацию о пользователе"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Удалить пользователя"""
        if UserManager.delete_user(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def verify_password(self, request, pk=None):
        """Проверить пароль пользователя"""
        user = get_object_or_404(User, pk=pk)
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid = UserManager.verify_password(user, password)
        return Response({'is_valid': is_valid})

class MealPlanViewSet(viewsets.ViewSet):
    """API endpoint для управления планами питания"""
    
    def list(self, request):
        """Получить список всех планов питания"""
        meal_plans = MealPlanManager.get_all_meal_plans()
        serializer = MealPlanSerializer(meal_plans, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Создать новый план питания"""
        serializer = MealPlanSerializer(data=request.data)
        if serializer.is_valid():
            meal_plan = MealPlanManager.create_meal_plan(
                user_id=serializer.validated_data['user_id'],
                duration=serializer.validated_data['duration'],
                total_price=serializer.validated_data.get('total_price')
            )
            return Response(MealPlanSerializer(meal_plan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном плане питания"""
        meal_plan = get_object_or_404(MealPlans, pk=pk)
        serializer = MealPlanSerializer(meal_plan)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Удалить план питания"""
        if MealPlanManager.delete_meal_plan(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость плана питания"""
        price = MealPlanManager.calculate_plan_price(pk)
        return Response({'price': price})

class MealViewSet(viewsets.ViewSet):
    """API endpoint для управления блюдами"""
    
    def list(self, request):
        """Получить список всех блюд"""
        meals = MealManager.get_all_meals()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Создать новое блюдо"""
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            meal = MealManager.create_meal(
                name=serializer.validated_data['name'],
                price=serializer.validated_data['price'],
                description=serializer.validated_data.get('description'),
                diet_type_id=serializer.validated_data.get('diet_type_id')
            )
            return Response(MealSerializer(meal).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном блюде"""
        meal = get_object_or_404(Meals, pk=pk)
        serializer = MealSerializer(meal)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Удалить блюдо"""
        if MealManager.delete_meal(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость блюда"""
        price = MealManager.calculate_meal_price(pk)
        return Response({'price': price})

class IngredientViewSet(viewsets.ViewSet):
    """API endpoint для управления ингредиентами"""
    
    def list(self, request):
        """Получить список всех ингредиентов"""
        ingredients = IngredientManager.get_all_ingredients()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Создать новый ингредиент"""
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = IngredientManager.create_ingredient(
                name=serializer.validated_data['name'],
                price_per_unit=serializer.validated_data['price_per_unit'],
                unit=serializer.validated_data['unit'],
                store_name=serializer.validated_data.get('store_name'),
                valid_from=serializer.validated_data.get('valid_from')
            )
            return Response(IngredientSerializer(ingredient).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном ингредиенте"""
        ingredient = get_object_or_404(Ingredients, pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Удалить ингредиент"""
        if IngredientManager.delete_ingredient(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class DietTypeViewSet(viewsets.ViewSet):
    """API endpoint для управления типами диет"""
    
    def list(self, request):
        """Получить список всех типов диет"""
        diet_types = DietTypeManager.get_all_diet_types()
        serializer = DietTypeSerializer(diet_types, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Создать новый тип диеты"""
        serializer = DietTypeSerializer(data=request.data)
        if serializer.is_valid():
            diet_type = DietTypeManager.create_diet_type(
                name=serializer.validated_data['name'],
                is_restricted=serializer.validated_data['is_restricted'],
                description=serializer.validated_data.get('description')
            )
            return Response(DietTypeSerializer(diet_type).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном типе диеты"""
        diet_type = get_object_or_404(DietTypes, pk=pk)
        serializer = DietTypeSerializer(diet_type)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Удалить тип диеты"""
        if DietTypeManager.delete_diet_type(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class FavoriteViewSet(viewsets.ViewSet):
    """API endpoint для управления избранными блюдами"""
    
    def list(self, request):
        """Получить список всех избранных блюд"""
        favorites = FavoriteManager.get_all_favorites()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Добавить блюдо в избранное"""
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            favorite = FavoriteManager.create_favorite(
                user_id=serializer.validated_data['user_id'],
                meal_id=serializer.validated_data['meal_id']
            )
            return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Получить информацию о конкретном избранном блюде"""
        favorite = get_object_or_404(Favorites, pk=pk)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Удалить блюдо из избранного"""
        if FavoriteManager.delete_favorite(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
