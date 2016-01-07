"""
Configuration for heroku production
"""

# pylint: disable=wildcard-import,unused-wildcard-import
import os
from .settings import *

DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = False

ALLOWED_HOSTS = [
    "vierk.ribeye.steakaupoivre.be",
    "www.4k-interieur.be",
]

# Add aws s3 to the installed apps
INSTALLED_APPS += (
    "cumulus",
    "manifest_storage.apps.ManifestStorageConfig",
)

DEFAULT_FILE_STORAGE = "manifest_storage.storage.ManifestStorage"
STATICFILES_STORAGE = "cumulus.storage.SwiftclientStaticStorage"

CUMULUS = {
    "USERNAME": os.getenv("RACKSPACE_USERNAME"),
    "API_KEY": os.getenv("RACKSPACE_API_KEY"),
    "PYRAX_IDENTITY_TYPE": "rackspace",
    "CONTAINER": os.getenv("RACKSPACE_MEDIA_CONTAINER"),
    "STATIC_CONTAINER": os.getenv("RACKSPACE_STATIC_CONTAINER"),
    "REGION": os.getenv("RACKSPACE_CDN_REGION"),
    "TTL": 864000,
    "HEADERS": (
        (r'.*\.(eot|otf|woff|ttf)$', {
            'Access-Control-Allow-Origin': '*'
        }),
    ),
}

if os.getenv("RACKSPACE_CDN_ALIAS_MEDIA"):
    CUMULUS["CONTAINER_URI"] = "http://%s" % os.getenv(
        "RACKSPACE_CDN_ALIAS_MEDIA")

if os.getenv("RACKSPACE_CDN_ALIAS_STATIC"):
    CUMULUS["STATIC_CONTAINER_URI"] = "http://%s" % os.getenv(
        "RACKSPACE_CDN_ALIAS_STATIC")

CACHES = {}
CACHES["default"] = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": os.getenv("REDIS_URL"),
    "TIMEOUT": None,
}

MANIFEST_STORAGE_CACHE = "default"

MEDIA_URL = "/media-buffer/"
MEDIA_ROOT = "/media-buffer"
