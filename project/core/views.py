from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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

class UserViewSet(viewsets.ModelViewSet):
    """API endpoint для управления пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def verify_password(self, request, pk=None):
        """Проверить пароль пользователя"""
        user = get_object_or_404(User, pk=pk)
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid = UserManager.verify_password(user, password)
        return Response({'is_valid': is_valid})

class MealPlanViewSet(viewsets.ModelViewSet):
    """API endpoint для управления планами питания"""
    queryset = MealPlans.objects.all()
    serializer_class = MealPlanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость плана питания"""
        price = MealPlanManager.calculate_plan_price(pk)
        return Response({'price': price})

class MealViewSet(viewsets.ModelViewSet):
    """API endpoint для управления блюдами"""
    queryset = Meals.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def calculate_price(self, request, pk=None):
        """Рассчитать стоимость блюда"""
        price = MealManager.calculate_meal_price(pk)
        return Response({'price': price})

class IngredientViewSet(viewsets.ModelViewSet):
    """API endpoint для управления ингредиентами"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class DietTypeViewSet(viewsets.ModelViewSet):
    """API endpoint для управления типами диет"""
    queryset = DietTypes.objects.all()
    serializer_class = DietTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class FavoriteViewSet(viewsets.ModelViewSet):
    """API endpoint для управления избранными блюдами"""
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
