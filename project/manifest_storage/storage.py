"""
A helper storage
"""

from django.core.cache import caches
from django.core.files.storage import Storage
from django.utils.module_loading import import_string

from manifest_storage import tasks

from .models import ManifestEntryModel
from . import settings


# pylint: disable=abstract-method
class ManifestStorage(Storage):
    """
    # Theory of operation

    The file storage operates on a manifest in a django cache, thus the storage
    will be as fast as the slowest of the cache or the storage buffer.

    Files will be stored to:
        - The CDN
        - The storage buffer

    A File manifest will be maintained in a cache with no expire. The manifest
    determines the existence and the url of a file.

    Files that are not in the cache, do not exist, regardless of their
    existence on the CDN.

    ## Saving a file

    ### Retrieve a suitable name from the cache

    Since the built in method uses the exists function of the storage,
    nothing should be modified.

    ### Store on the buffer

    Store it on the buffer storage and map the name of the saved file in the
    buffer to the canonical file name in the cache.

    The pattern should be "<file/name>_buffer": "<buffered/file/name>"

    FUTURE: Implement a public/private interface on the buffer, to host the
    files externally or not.

    ### Store on the CDN

    When the file is saved in the fast buffer, start a celery task to save
    the file on the slow remote. Map the remote file name to the canonical file
    name.

    The pattern should be "<file/name>_remote": "<swift/file/name>"

    Map the remote url in the pattern: "<file/name>_remote_url"

    ## Open the file

    Open it from the buffer. Check it's existence from the cache

    ## Size of the file

    Retrieve from buffer

    ## Url

    Retrieve from the cache.

    ## Extra, seed command

    Scans remote
    """

    _cache = None
    _buffer_storage = None
    _remote_storage = None

    def __init__(self, *args, **kwargs):
        """
        Patch constructor
        """
        self._cache = caches[settings.CACHE]
        self._buffer_storage = import_string(settings.BUFFER)(
            **settings.BUFFER_KWARGS)
        self._remote_storage = import_string(settings.REMOTE)()
        super(ManifestStorage, self).__init__(*args, **kwargs)

    def _get_cache_key(self, name, key):  # pylint: disable=no-self-use
        """
        gets a cache key, based on name and property key
        """
        return "%s_%s" % (name, key)

    def _get_manifest(self, name, key):
        """
        Get the cached value
        """
        cached = self._cache.get(self._get_cache_key(name, key))
        if cached is None:
            try:
                entry = ManifestEntryModel.objects.get(name=name)
                cached = getattr(entry, key)
                self._cache.set(self._get_cache_key(name, key), cached)
            except ManifestEntryModel.DoesNotExist:
                return None
        return cached

    def _set_manifest(self, name, key, value):
        """
        Set the cache
        """
        try:
            entry = ManifestEntryModel.objects.get(name=name)
        except ManifestEntryModel.DoesNotExist:
            entry = ManifestEntryModel()
            entry.name = name

        setattr(entry, key, value)
        entry.save()

        self._cache.set(self._get_cache_key(name, key), value)

    def _clear_manifest(self, name):
        """
        Clear keys from cache
        """
        ManifestEntryModel.objects.filter(name=name).delete()
        # pylint: disable=protected-access
        for field in ManifestEntryModel._meta.get_fields():
            self._cache.delete(self._get_cache_key(name, field.name))
        # pylint: enable=protected-access

    def _fetch_from_remote(self, name):
        """
        Copy to buffer from remote
        """
        remote_name = self._get_manifest(name, "remote_name")
        content = self._remote_storage.open(remote_name)
        buffer_name = self._buffer_storage.save(name, content)
        self._set_manifest(name, "buffer_name", buffer_name)
        return buffer_name

    def _open(self, name, mode="rb"):
        """
        Open a file
        """
        buffer_name = self._get_manifest(name, "buffer_name")
        if buffer_name is None or not self._buffer_storage.exists(buffer_name):
            buffer_name = self._fetch_from_remote(name)
        content = self._buffer_storage.open(buffer_name, mode)
        content.storage = self
        return content

    def _save(self, name, content):
        """
        Save in file
        """
        self._set_manifest(name, "buffer_name",
                           self._buffer_storage.save(name, content))

        # Start async task to store on the remote
        tasks.save_to_remote.delay(name)

        return name

    def delete(self, name):
        """
        Delete a file
        """
        remote_name = self._get_manifest(name, "remote_name")
        buffer_name = self._get_manifest(name, "buffer_name")

        self._clear_manifest(name)

        self._buffer_storage.delete(buffer_name)

        # Start task to delete async
        tasks.delete_from_remote.delay(remote_name)

    def exists(self, name):
        """
        A wrapper for an existence test
        """
        if self._get_manifest(name, "name"):
            return True
        return False

    def size(self, name):
        """
        A wrapper that pulls from cache if possible
        """
        buffer_name = self._get_manifest(name, "buffer_name")
        if buffer_name is None or not self._buffer_storage.exists(buffer_name):
            buffer_name = self._fetch_from_remote(name)
        return self._buffer_storage.size(buffer_name)

    def url(self, name):
        """
        Return cached url if possible
        """
        cached = self._get_manifest(name, "remote_url")
        if cached:
            return cached
        buffer_name = self._get_manifest(name, "buffer_name")
        if buffer_name is None or not self._buffer_storage.exists(buffer_name):
            buffer_name = self._fetch_from_remote(name)
        return self._buffer_storage.url(buffer_name)
# pylint: enable=abstract-method
