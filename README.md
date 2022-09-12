# Сервис пользовательских рецептов на DRF
Стек технологий:
- Python 3.9.5
- PostgreSQL 14
- Django 4.1
- DRF 3.13.1

Необходимо загрузить все библиотеки из файла requirements.txt

В settings.py в INSTALLED_APPS добавить 'service.apps.ServiceConfig',
    'rest_framework',

Подключение БД:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Настройки rest_framework:
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

Выполнить миграции - python manage.py migrate
 
