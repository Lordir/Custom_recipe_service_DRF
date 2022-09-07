from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class UsersAdmin(UserAdmin):
    pass


admin.site.register(User, UsersAdmin)
admin.site.register(Recipe)
