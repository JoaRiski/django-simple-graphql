import os
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_PATH + "/examples/")

DEBUG = os.environ.get("DJANGO_DEBUG", False) in ("True", "true", "1")
SECRET_KEY = 1

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "graphene_django",
    "example",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_URL = "/static/"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    }
]

GRAPHENE = {"SCHEMA": "example.schema.schema"}
ROOT_URLCONF = "example.urls"
