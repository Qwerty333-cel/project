from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
# get_object_or_404 не всегда нужен, если ModelViewSet.get_object() используется
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User as DjangoUser
# TokenAuthentication не используется, JWTAuthentication используется
# from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import (
    UserManager, MealPlanManager, MealManager # IngredientManager, DietTypeManager, FavoriteManager, PriceManager - если используются ниже
)
from .serializers import (
    UserSerializer, MealPlanSerializer, MealSerializer,
    IngredientSerializer, DietTypeSerializer, FavoriteSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """API endpoint для управления пользователями"""
    queryset = User.objects.all() # Работаем с вашей моделью core.models.User
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        # 'login' не является стандартным действием ModelViewSet. 
        # Предполагается, что для логина используется /api/token/
        if self.action == 'create': # 'create' это регистрация
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        """
        При удалении пользователя (DELETE /api/users/{id}/).
        'instance' здесь - это экземпляр core.models.User.
        Удаляем связанный django.contrib.auth.models.User.
        Каскадное удаление (on_delete=models.CASCADE в User.django_user и Profile.user) 
        позаботится об удалении самого 'instance' (core.models.User) и связанного 'Profile'.
        """
        django_user_to_delete = None
        
        if hasattr(instance, 'django_user') and instance.django_user:
            django_user_to_delete = instance.django_user
        else:
            # Если core.User существует без связанного DjangoUser (не должно быть)
            # Просто удаляем 'instance', если он еще существует.
            if User.objects.filter(pk=instance.pk).exists():
                try:
                    instance.delete()
                except Exception as e:
                    print(f"Error deleting orphaned CoreUser instance ({instance.pk}): {e}")
            return 

        if django_user_to_delete:
            try:
                django_user_to_delete.delete()
                # Каскадное удаление должно удалить 'instance' (core.models.User) и 'Profile'.
            except DjangoUser.DoesNotExist:
                # DjangoUser уже мог быть удален. Проверим и удалим core.User, если он остался.
                if User.objects.filter(pk=instance.pk).exists():
                    try:
                        instance.delete()
                    except Exception as e:
                         print(f"Error deleting CoreUser ({instance.pk}) after DjangoUser was not found: {e}")
            except Exception as e:
                print(f"Error deleting DjangoUser ({django_user_to_delete.pk}) "
                      f"associated with CoreUser ({instance.pk}): {e}")
                # Если удаление DjangoUser не удалось, можно попытаться удалить CoreUser,
                # но это может нарушить целостность. Чтобы DRF вернул корректный 204 
                # (или ошибку, если удаление instance тоже не удалось), 
                # можно перевыбросить ошибку, если это критично.
                # В данном случае, если DjangoUser не удалился, 'instance' не удалится каскадно.
                # Чтобы perform_destroy считался "успешным" с точки зрения DRF 
                # (т.е. instance больше нет), можно попытаться удалить instance отдельно.
                if User.objects.filter(pk=instance.pk).exists():
                    try:
                        instance.delete()
                    except Exception as nested_e:
                         print(f"Additionally failed to delete CoreUser {instance.pk} after DjangoUser deletion error: {nested_e}")
                         raise nested_e # Перевыбрасываем, если и это не удалось
                # Если предыдущий raise не сработал, но мы хотим показать ошибку от DjangoUser.delete()
                # raise e # Раскомментировать, если хотите, чтобы API вернул 500 при ошибке удаления DjangoUser

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_password(self, request, pk=None):
        """Проверить пароль пользователя"""
        user_instance = self.get_object() # user_instance это core.models.User
        
        if not hasattr(user_instance, 'django_user') or not user_instance.django_user:
            return Response(
                {'error': 'Associated DjangoUser not found for this user profile.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # request.user это django.contrib.auth.models.User
        if request.user != user_instance.django_user and not request.user.is_staff:
             return Response(
                 {'error': 'You do not have permission to verify this user\'s password.'}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # UserManager.verify_password ожидает экземпляр core.models.User согласно вашему functions.py
        is_valid = UserManager.verify_password(user_instance, password) 
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
        # Проверяем, что объект существует перед вызовом менеджера
        self.get_object() # Вызовет 404, если не найден
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
        self.get_object() # Вызовет 404, если не найден
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