from django.conf import settings
from django.core.cache import cache

from jobs.models import Client


def get_cached_client():
    if settings.CACHE_ENABLED:
        key = 'client_list'
        client_list = cache.get(key)
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
    else:
        client_list = Client.objects.all()

    return client_list
