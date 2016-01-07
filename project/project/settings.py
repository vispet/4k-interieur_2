"""
Django settings for goldstar project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.realpath(os.path.dirname(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps
    "feincms",
    "adminsortable",
    "simple_resizer",
    "solo",

    # Homepage app
    "utilities.apps.UtilitiesConfig",
    "about.apps.AboutConfig",
    "configuration.apps.ConfigurationConfig",
    "contact.apps.ContactConfig",
    "home.apps.HomeConfig",
    "news.apps.NewsConfig",
    "portfolio.apps.PortfolioConfig",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
)

ROOT_URLCONF = "project.urls"

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {}
DATABASES["default"] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "nl-be"

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Vo de show (just as dummy)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(ROOT_DIR, ".data/static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, ".data/media")

# Add the general template dir to loader path
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "project.context_processors.google_analytics",
            ],
            "debug": True,
        },
    },
]

# Make the staticfile dirs dependant of env vars
STATICFILES_DIRS = []
if "ASSETS_BUILD_DIR_FULL" in os.environ:
    STATICFILES_DIRS.append(os.environ.get("ASSETS_BUILD_DIR_FULL"))

# Load the google analytics id from env
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID")

# Set the email backend in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MAILGUN_ACCESS_KEY = os.getenv("MAILGUN_ACCESS_KEY")
MAILGUN_SERVER_NAME = os.getenv("MAILGUN_SERVER_NAME")

if MAILGUN_ACCESS_KEY and MAILGUN_SERVER_NAME:
    EMAIL_BACKEND = "django_mailgun.MailgunBackend"

if os.getenv("CONTACT_FORM_SENDER_ADDRESS"):
    CONTACT_FORM_SENDER_ADDRESS = os.getenv("CONTACT_FORM_SENDER_ADDRESS")

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

if os.getenv("RABBITMQ_URL"):
    BROKER_URL = os.getenv("RABBITMQ_URL")
elif os.getenv("BROKER_URL"):
    BROKER_URL = os.getenv("BROKER_URL")
