__all__ = ()

import os
import pathlib

import django.urls
import dotenv


dotenv.load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="123456")

DEBUG_ENV = os.getenv("DJANGO_DEBUG", default="False")

DEBUG = DEBUG_ENV.lower() in (
    "true",
    "1",
    "y",
    "yes",
)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(
    ",",
)

INSTALLED_APPS = [
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "vacancies.apps.VacanciesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "sorl.thumbnail",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

ROOT_URLCONF = "hackmate.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hackmate.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth" ".password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth"
            ".password_validation.NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = [
    "users.backends.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_MAIL = os.getenv("DJANGO_MAIL")

MAX_AUTH_ATTEMPTS = os.getenv("DJANGO_MAX_AUTH_ATTEMPS", 5)


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

LOGIN_REDIRECT_URL = django.urls.reverse_lazy("homepage:homepage")
LOGIN_URL = django.urls.reverse_lazy("users:login")
LOGOUT_REDIRECT_URL = django.urls.reverse_lazy("users:login")


if DEBUG:
    DEFAULT_USER_IS_ACTIVE = os.getenv(
        "DJANGO_DEFAULT_USER_IS_ACTIVE",
        default="True",
    )

else:
    DEFAULT_USER_IS_ACTIVE = os.getenv(
        "DJANGO_DEFAULT_USER_IS_ACTIVE",
        default="False",
    )

DEFAULT_USER_IS_ACTIVE = DEFAULT_USER_IS_ACTIVE.lower() in (
    "true",
    "yes",
    "1",
    "y",
    "",
)
