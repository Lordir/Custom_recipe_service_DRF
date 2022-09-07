from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')

