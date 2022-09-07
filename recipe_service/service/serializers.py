from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')


class AddRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ('likes', 'is_active', 'author')

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)
