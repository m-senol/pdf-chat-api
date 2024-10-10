from cachetools import LFUCache
from .config import MAX_CACHE_SIZE

cache = LFUCache(maxsize=MAX_CACHE_SIZE)
