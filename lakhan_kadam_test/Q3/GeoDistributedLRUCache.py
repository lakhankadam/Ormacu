from cache import LeastRecentlyUsedCache
from worker import Worker

class GeoDistributedCache:

    def __init__(self, cache_name, expiration_time, capacity):
        self.lru_cache = LeastRecentlyUsedCache(cache_name, expiration_time, capacity)
        self.connection_pools = self.lru_cache.server_util.connection_pools
    
    def get_key(self, key):
        return self.lru_cache.get(key)
    
    def set_key(self, key, value):
        self.lru_cache.set(key, value)


if __name__ == "__main__":
    set_name = "test"
    expiration_time = 10 #100 seconds
    capacity = 4
    geoDistributedCache = GeoDistributedCache(set_name, expiration_time, capacity)
    #Demo of set and get
    geoDistributedCache.set_key("test1", "test1")
    geoDistributedCache.set_key("test2", "test2")
    geoDistributedCache.set_key("test3", "test3")
    geoDistributedCache.set_key("test4", "test4")
    geoDistributedCache.set_key("test5", "test5")

    print(geoDistributedCache.get_key("test1"))
    print(geoDistributedCache.get_key("test3"))
    worker = Worker(expiration_time, geoDistributedCache.connection_pools.values(), set_name)
