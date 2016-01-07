"""
Settings
"""

from django.conf import settings


def _load(name, default, prefix="MANIFEST_STORAGE_"):
    """
    Load from settings or default in a prefixed way
    """
    return getattr(settings, "%s%s" % (prefix, name), default)

CACHE = _load("CACHE", "default")
BUFFER = _load("BUFFER", "django.core.files.storage.FileSystemStorage")
REMOTE = _load("REMOTE", "cumulus.storage.SwiftclientStorage")

BUFFER_KWARGS = _load("BUFFER_KWARGS", {
    "file_permissions_mode": 0o777,
    "directory_permissions_mode": 0o777,
})
