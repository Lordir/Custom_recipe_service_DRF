from django.contrib import admin
from django.urls import path, include

from service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('accounts/profile/', GetUserProfile.as_view()),
    path('api/v1/user_profile/', GetUserProfile.as_view()),
    path('api/v1/top_users/', GetTopUsers.as_view()),
]
