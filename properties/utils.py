import logging

from django.core.cache import cache
from django_redis import get_redis_connection

from .models import Property


logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get("all_properties")

    if not properties:
        properties = Property.objects.all()
        cache.set("all_properties", properties, 3600)  # 1 hour

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and compute hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info()

    hits = int(info.get("keyspace_hits", 0))
    misses = int(info.get("keyspace_misses", 0))

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }

    logger.info(
        "Redis cache metrics - hits=%s misses=%s hit_ratio=%.4f",
        hits,
        misses,
        hit_ratio,
    )

    return metrics
