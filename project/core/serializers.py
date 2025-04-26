from rest_framework import serializers
from .models import User, MealPlans, Meals, Ingredients, DietTypes, Favorites
from .functions import UserManager

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    weight = serializers.FloatField(required=False)
    height = serializers.FloatField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'weight', 'height', 'age', 'diet_type_id']
    
    def create(self, validated_data):
        return UserManager.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            weight=validated_data.get('weight'),
            height=validated_data.get('height'),
            age=validated_data.get('age'),
            diet_type_id=validated_data.get('diet_type_id')
        )
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            UserManager.update_password(instance, validated_data.pop('password'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MealPlanSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = MealPlans
        fields = ['id', 'user_id', 'duration', 'total_price']

class MealSerializer(serializers.ModelSerializer):
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
    user_id = serializers.IntegerField(required=True)
    meal_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Favorites
        fields = ['id', 'user_id', 'meal_id'] 