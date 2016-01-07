"""
Implement celery tasks
"""

from celery import shared_task

from .utils import get_storage


@shared_task
def save_to_remote(name):
    """
    Save a file to remote
    """
    # pylint: disable=protected-access
    storage = get_storage()
    buffer_name = storage._get_manifest(name, "buffer_name")
    content = storage._buffer_storage.open(buffer_name)
    remote_name = storage._remote_storage.save(name, content)
    storage._set_manifest(name, "remote_name", remote_name)
    storage._set_manifest(name, "remote_url",
                          storage._remote_storage.url(remote_name))
    # pylint: enable=protected-access


@shared_task
def delete_from_remote(remote_name):
    """
    Save a file to remote
    """
    # pylint: disable=protected-access
    storage = get_storage()
    storage._remote_storage.delete(remote_name)
    # pylint: enable=protected-access
