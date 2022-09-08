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


class UsersForListRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_active')


class ListRecipeSerializer(serializers.ModelSerializer):
    author = UsersForListRecipeSerializer()

    class Meta:
        model = Recipe
        exclude = ('cooking_steps',)


class GetRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class LikeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
