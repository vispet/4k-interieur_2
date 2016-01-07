"""
General purpose utilities
"""

import os
import pyrax

from django.utils.module_loading import import_string
from django.conf import settings

from .models import ManifestEntryModel


def preload_from_cloudfiles(container_name):
    """
    Preload the manifest file storage from a rackspace container
    """
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credentials(os.getenv("RACKSPACE_USERNAME"),
                          os.getenv("RACKSPACE_API_KEY"))

    container = pyrax.cloudfiles.get_container(container_name)
    if "CONTAINER_URI" in settings.CUMULUS:
        cdn_uri = settings.CUMULUS["CONTAINER_URI"]
    else:
        cdn_uri = container.cdn_uri

    for cloud_obj in container.get_objects(full_listing=True):
        # Map to the manifest name, remote_name and cdn_uri
        if not ManifestEntryModel.objects.filter(name=cloud_obj.name).exists():
            print("Saving \"%s\"" % cloud_obj.name)
            manifest_obj = ManifestEntryModel()
            manifest_obj.name = cloud_obj.name
            manifest_obj.remote_name = cloud_obj.name
            manifest_obj.remote_url = os.path.join(cdn_uri, cloud_obj.name)
            manifest_obj.save()


def get_storage():
    """
    Storage getter
    """
    return import_string("manifest_storage.storage.ManifestStorage")()
