from django.db.models import F
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .permissions import CheckIsActive
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
    permission_classes = (CheckIsActive,)

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


# class AddRecipe(APIView):
#     def post(self, request):
#         serializer = AddRecipeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(author=self.request.user)
#
#         return Response({'recipe': serializer.data})


class AddRecipe(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = AddRecipeSerializer
    permission_classes = (CheckIsActive,)


class ListRecipe(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_active=True)
    serializer_class = ListRecipeSerializer
    permission_classes = (CheckIsActive,)


class ListRecipeSortLikes(APIView, LimitOffsetPagination):
    permission_classes = (CheckIsActive,)

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
    permission_classes = (CheckIsActive,)

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
    permission_classes = (CheckIsActive,)

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
    permission_classes = (CheckIsActive,)


class LikeRecipe(APIView):
    permission_classes = (CheckIsActive,)

    def get(self, request, **kwargs):
        recipes = Recipe.objects.filter(id=self.kwargs['pk'])
        Recipe.objects.filter(id=self.kwargs['pk']).update(likes=F('likes') + 1)
        get_data = LikeRecipeSerializer(recipes, many=True).data
        get_data[0]['likes'] += 1

        return Response(get_data)


class GetTopUsersLikes(APIView):
    permission_classes = (CheckIsActive,)

    def get(self, request):
        users = User.objects.filter(is_active=True)
        get_data = UserSerializer(users, many=True).data
        index = 0
        for user in users:
            recipes = Recipe.objects.filter(author=user.pk)
            get_data[index].update({'number_of_recipes': len(recipes)})
            number_of_likes = 0
            for recipe in recipes:
                number_of_likes += recipe.likes
            get_data[index].update({'number_of_likes': number_of_likes})
            index += 1

        # sorting
        for g in range(len(get_data) - 1):
            for h in range(len(get_data) - g - 1):
                if get_data[h]['number_of_likes'] < get_data[h + 1]['number_of_likes']:
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


class AddInFavorites(APIView):
    permission_classes = (CheckIsActive,)

    def get(self, request, **kwargs):
        recipe = Recipe.objects.filter(id=self.kwargs['pk'])
        favorites = Favorites.objects.filter(user=request.user)
        flag = True

        for i in range(len(favorites)):
            if favorites[i].recipe == recipe[0]:
                flag = False
                break
        if flag:
            Favorites.objects.create(user=request.user, recipe=recipe[0])

        return Response({'user': request.user.username, 'recipe': recipe[0].title})


class GetMyFavoritesList(APIView, LimitOffsetPagination):
    permission_classes = (CheckIsActive,)

    def get(self, request):
        favorites = Favorites.objects.filter(user=request.user)
        get_data = FavoritesListSerializer(favorites, many=True).data

        return Response(get_data)


class UpdateUsername(APIView):
    permission_classes = (CheckIsActive,)

    def put(self, request, *args, **kwargs):
        pk = request.user
        serializer = RenameSerializer(pk, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

