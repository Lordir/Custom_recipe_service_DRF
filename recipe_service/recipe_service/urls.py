from django.contrib import admin
from django.urls import path, include

from service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('accounts/profile/', GetUserProfile.as_view()),
    path('api/v1/user_profile/', GetUserProfile.as_view()),
    path('api/v1/top_users/', GetTopUsers.as_view()),
    path('api/v1/top_users_likes/', GetTopUsersLikes.as_view()),
    path('api/v1/add_recipe/', AddRecipe.as_view()),
    path('api/v1/list_recipe/', ListRecipe.as_view()),
    path('api/v1/list_recipe/sort_likes/', ListRecipeSortLikes.as_view()),
    path('api/v1/list_recipe/sort_date/', ListRecipeSortDate.as_view()),
    path('api/v1/list_recipe/sort_name/', ListRecipeSortName.as_view()),
    path('api/v1/get_recipe/<pk>/', GetRecipe.as_view()),
    path('api/v1/get_recipe/<pk>/like/', LikeRecipe.as_view()),
    path('api/v1/get_recipe/<pk>/add_in_favorites/', AddInFavorites.as_view()),
    path('api/v1/get_my_favorites/', GetMyFavoritesList.as_view()),
    path('api/v1/change_username/', UpdateUsername.as_view()),
]
