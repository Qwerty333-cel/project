from rest_framework import serializers
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import UserManager # UserManager используется

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True) # Это будет username от DjangoUser через property
    email = serializers.EmailField(required=True)   # Это будет email от DjangoUser через property
    
    # diet_type_id нужно, если вы хотите передавать ID при создании/обновлении User
    # Если DietTypes сериализуется целиком, то поле diet_type можно определить как вложенный сериализатор
    # или оставить diet_type_id, если ваш UserManager.create_user и update ожидают ID.
    # Судя по UserManager.create_user, он ожидает diet_type_id.
    diet_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DietTypes.objects.all(), 
        source='diet_type', # Связывает с полем diet_type в модели User
        allow_null=True,    # Если diet_type может быть null
        required=False      # Если diet_type не обязателен при создании/обновлении
    )
    
    class Meta:
        model = User # Ваша модель core.models.User
        # Поля username и email в fields будут использовать properties из модели User,
        # которые, в свою очередь, берут данные из django_user.
        # При создании (create), UserManager.create_user получит 'username' и 'email' из validated_data
        # и создаст DjangoUser.
        fields = ['id', 'username', 'password', 'email', 'weight', 'height', 'age', 'diet_type_id']
        # 'django_user' не включаем в fields, так как он управляется внутренне.
    
    def create(self, validated_data):
        # validated_data['diet_type'] теперь будет экземпляром DietTypes из-за PrimaryKeyRelatedField
        # UserManager ожидает diet_type_id
        diet_type_instance = validated_data.pop('diet_type', None)
        diet_type_id_val = diet_type_instance.id if diet_type_instance else None

        return UserManager.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            weight=validated_data.get('weight'),
            height=validated_data.get('height'),
            age=validated_data.get('age'),
            diet_type_id=diet_type_id_val # Передаем ID
        )
    
    def update(self, instance, validated_data):
        # instance здесь - это core.models.User
        if 'password' in validated_data:
            # UserManager.update_password ожидает core.models.User
            UserManager.update_password(instance, validated_data.pop('password'))
        
        # Обновляем поля DjangoUser, если они пришли
        django_user = instance.django_user
        if 'username' in validated_data:
            django_user.username = validated_data.pop('username')
        if 'email' in validated_data:
            django_user.email = validated_data.pop('email')
        django_user.save() # Сохраняем изменения в DjangoUser

        # Обновляем остальные поля core.models.User
        # Учтем, что diet_type_id может прийти как diet_type (экземпляр)
        diet_type_instance = validated_data.pop('diet_type', None)
        if diet_type_instance is not None: # Если diet_type был передан
            instance.diet_type = diet_type_instance
        elif 'diet_type_id' in validated_data and validated_data['diet_type_id'] is None: 
            # Если явно передали null для diet_type_id, чтобы его сбросить
            instance.diet_type = None


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save() # Сохраняем изменения в core.models.User
        return instance

class MealPlanSerializer(serializers.ModelSerializer):
    # user_id здесь указывает на ID вашего кастомного User (core.models.User)
    # Это соответствует полю user в модели MealPlans, которое ForeignKey к User
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user' # Указывает на поле 'user' в модели MealPlans
    ) 
    
    class Meta:
        model = MealPlans
        fields = ['id', 'user_id', 'duration', 'total_price']

class MealSerializer(serializers.ModelSerializer):
    diet_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DietTypes.objects.all(),
        source='diet_type',
        allow_null=True,
        required=False
    )
    class Meta:
        model = Meals
        fields = ['id', 'name', 'description', 'price', 'diet_type_id']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'price_per_unit', 'unit', 'store_name', 'valid_from']

class DietTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietTypes
        fields = ['id', 'name', 'description', 'is_restricted']

class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    meal_id = serializers.PrimaryKeyRelatedField(queryset=Meals.objects.all(), source='meal')
    
    class Meta:
        model = Favorites
        fields = ['id', 'user_id', 'meal_id'] 