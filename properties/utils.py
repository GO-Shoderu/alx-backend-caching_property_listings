import logging

from django.core.cache import cache
from django_redis import get_redis_connection

from .models import Property


logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get("all_properties")

    if not properties:
        properties = Property.objects.all()
        cache.set("all_properties", properties, 3600)

    return properties


def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()

    hits = int(info.get("keyspace_hits", 0))
    misses = int(info.get("keyspace_misses", 0))

    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    logger.error(
        "Redis cache metrics: hits=%s, misses=%s, hit_ratio=%s",
        hits,
        misses,
        hit_ratio,
    )

    return {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }
