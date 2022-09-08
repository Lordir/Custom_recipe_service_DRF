from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .serializers import *


class GetUserProfile(APIView):
    def get(self, request):
        pk = request.user.pk
        users = User.objects.filter(id=pk)
        recipes = Recipe.objects.filter(author=pk)
        answer = UserSerializer(users, many=True).data
        answer[0].update({'number_of_recipes': len(recipes)})
        return Response(answer)


class GetTopUsers(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        get_data = UserSerializer(users, many=True).data
        index = 0
        for user in users:
            recipes = Recipe.objects.filter(author=user.pk)
            get_data[index].update({'number_of_recipes': len(recipes)})
            index += 1

        # sorting
        for g in range(len(get_data) - 1):
            for h in range(len(get_data) - g - 1):
                if get_data[h]['number_of_recipes'] < get_data[h + 1]['number_of_recipes']:
                    get_data[h], get_data[h + 1] = get_data[h + 1], get_data[h]

        if len(get_data) < 10:
            i = len(get_data)
        else:
            i = 10
        final_list = []
        for item in get_data:
            if i == 0:
                break
            else:
                final_list.append(item)
                i -= 1
        return Response(final_list)


class AddRecipe(APIView):
    def post(self, request):
        serializer = AddRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

        return Response({'recipe': serializer.data})


class ListRecipe(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_active=True)
    serializer_class = ListRecipeSerializer


class ListRecipeSortLikes(APIView, LimitOffsetPagination):
    def get(self, request):
        recipes = Recipe.objects.filter(is_active=True)
        recipes_pagination = self.paginate_queryset(recipes, request, view=self)
        get_data = ListRecipeSerializer(recipes_pagination, many=True).data

        # sorting
        for g in range(len(get_data) - 1):
            for h in range(len(get_data) - g - 1):
                if get_data[h]['likes'] < get_data[h + 1]['likes']:
                    get_data[h], get_data[h + 1] = get_data[h + 1], get_data[h]

        return self.get_paginated_response(get_data)


class ListRecipeSortDate(APIView, LimitOffsetPagination):
    def get(self, request):
        recipes = Recipe.objects.filter(is_active=True)
        recipes_pagination = self.paginate_queryset(recipes, request, view=self)
        get_data = ListRecipeSerializer(recipes_pagination, many=True).data

        # sorting
        for g in range(len(get_data) - 1):
            for h in range(len(get_data) - g - 1):
                if get_data[h]['created_on'] > get_data[h + 1]['created_on']:
                    get_data[h], get_data[h + 1] = get_data[h + 1], get_data[h]

        return self.get_paginated_response(get_data)


class ListRecipeSortName(APIView, LimitOffsetPagination):
    def get(self, request):
        recipes = Recipe.objects.filter(is_active=True)
        recipes_pagination = self.paginate_queryset(recipes, request, view=self)
        get_data = ListRecipeSerializer(recipes_pagination, many=True).data

        # sorting
        for g in range(len(get_data) - 1):
            for h in range(len(get_data) - g - 1):
                if get_data[h]['title'] > get_data[h + 1]['title']:
                    get_data[h], get_data[h + 1] = get_data[h + 1], get_data[h]

        return self.get_paginated_response(get_data)


class GetRecipe(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer
