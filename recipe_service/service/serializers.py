from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')


class AddRecipeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        exclude = ('likes', 'is_active')

    # def create(self, validated_data):
    #     return Recipe.objects.create(**validated_data)


class ListRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ('cooking_steps',)


class GetRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
