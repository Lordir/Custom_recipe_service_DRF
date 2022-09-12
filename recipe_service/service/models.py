from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                max_length=30, unique=True, verbose_name='username')
    password = models.CharField(max_length=128, verbose_name='password')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser status')
    is_active = models.BooleanField(default=True, verbose_name='active')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Recipe(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Автор")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30, verbose_name="Название")
    type_dish = models.CharField(max_length=30, verbose_name="Тип блюда")
    description = models.TextField(max_length=1000, verbose_name="Описание")
    cooking_steps = models.TextField(max_length=1000, verbose_name="Шаги приготовления")
    photo = models.CharField(max_length=50, verbose_name="Фотография")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    is_active = models.BooleanField(default=True, verbose_name="Статус")

    def __str__(self):
        return self.title


class Favorites(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    recipe = models.ForeignKey('Recipe', on_delete=models.PROTECT, verbose_name="Рецепт")

    def __str__(self):
        return self.recipe


class Hashtag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name="Рецепт")
    hashtag = models.CharField(max_length=30, verbose_name="Хэштег")

    def __str__(self):
        return self.hashtag
