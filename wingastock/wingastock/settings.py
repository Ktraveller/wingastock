"""
Django settings for wingastock project.

Django 6.0.6
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv(BASE_DIR / ".env")


# ==========================================================
# SECURITY
# ==========================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    os.environ.get(
        "SECRET_KEY",
        "django-insecure-change-this-in-production"
    )
)

# Render should have DEBUG=False
DEBUG = os.environ.get(
    "DEBUG",
    "False"
).lower() == "true"


# Render automatically provides RENDER_EXTERNAL_HOSTNAME
RENDER_EXTERNAL_HOSTNAME = os.environ.get(
    "RENDER_EXTERNAL_HOSTNAME"
)


ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    ""
).split(",")

ALLOWED_HOSTS = [
    host.strip()
    for host in ALLOWED_HOSTS
    if host.strip()
]


# Add Render hostname automatically
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Useful for local development
if DEBUG:
    ALLOWED_HOSTS += [
        "localhost",
        "127.0.0.1",
    ]


# ==========================================================
# CSRF
# ==========================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]


# Automatically trust Render URL
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )


# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Your applications
    "core",
    "administrators",
    "sellers",
    "mails",
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================================
# ROOT URL
# ==========================================================

ROOT_URLCONF = "wingastock.urls"


# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# ==========================================================
# WSGI
# ==========================================================

WSGI_APPLICATION = "wingastock.wsgi.application"


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


if DATABASE_URL:

    # Render PostgreSQL
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }

else:

    # Local development
    DATABASES = {

        "default": {

            "ENGINE":
                "django.db.backends.sqlite3",

            "NAME":
                BASE_DIR / "db.sqlite3",

        }
    }


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ==========================================================
# STATIC FILES
# ==========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# Source static directory during development
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ==========================================================
# CLOUDINARY
# ==========================================================

CLOUDINARY_STORAGE = {

    "CLOUD_NAME":
        os.environ.get(
            "CLOUDINARY_CLOUD_NAME"
        ),

    "API_KEY":
        os.environ.get(
            "CLOUDINARY_API_KEY"
        ),

    "API_SECRET":
        os.environ.get(
            "CLOUDINARY_API_SECRET"
        ),

}


# ==========================================================
# FILE STORAGE
# ==========================================================

STORAGES = {

    # User uploaded files
    # Images / media → Cloudinary

    "default": {

        "BACKEND":
            "cloudinary_storage.storage.MediaCloudinaryStorage",

    },


    # CSS / JS / static images → WhiteNoise

    "staticfiles": {

        "BACKEND":
            "whitenoise.storage.CompressedManifestStaticFilesStorage",

    },

}


# ==========================================================
# MEDIA
# ==========================================================

MEDIA_URL = "/media/"


# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ==========================================================
# PRODUCTION SECURITY
# ==========================================================

if not DEBUG:

    # Render uses HTTPS
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True
