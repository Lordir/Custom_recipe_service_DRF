from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class GetUserProfile(APIView):
    def get(self, request):
        pk = request.user.pk
        users = User.objects.filter(id=pk)
        recipes = Recipe.objects.filter(author=pk)
        answer = UserSerializer(users, many=True).data
        answer[0].update({'number_of_recipes': len(recipes)})
        return Response(answer)
