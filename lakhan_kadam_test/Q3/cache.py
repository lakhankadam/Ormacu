#Implementing LRU cache using Redis

from server_util import ServerUtil
import time
class LeastRecentlyUsedCache:
    def __init__(self, name, expiration_time, capacity):
        self.sorted_set_name = name + "_sorted_set"
        self.hash_set_name = name + "_hash_set"
        self.expiration_time = expiration_time
        self.capacity = capacity
        self.server_util = ServerUtil()
        self.curr_server = self.server_util.get_nearest_server()
        self.redis_client = self.server_util.get_redis_client(self.curr_server)
    
    def get(self, key, redis_client=None):
        if redis_client is None:
            curr_redis_client = self.redis_client
        else:
            curr_redis_client = redis_client
        if curr_redis_client.hexists(self.hash_set_name, key):
            #Remove key from sorted set
            curr_redis_client.zrem(self.sorted_set_name, key)
            #Add key to sorted set with current time
            current_time = time.time().__round__()
            curr_redis_client.zadd(self.sorted_set_name, {key: current_time})
            #Replicate data across regions only if redis_client is current redis_client
            if redis_client == None:
                self.replicate_action_across_servers("get", key)
            val = curr_redis_client.hget(self.hash_set_name, key)
            #Check utf-8 encoding
            if val:
                return val.decode("utf-8")
        return None
    
    def delete(self, redis_client=None):
        if redis_client is None:
            curr_redis_client = self.redis_client
        else:
            curr_redis_client = redis_client
        keys = curr_redis_client.zrange(self.sorted_set_name, 0, 0)
        #Remove keys from sorted set
        curr_redis_client.zremrangebyrank(self.sorted_set_name, 0, 0)
        #Remove keys from hash set
        curr_redis_client.hdel(self.hash_set_name, *keys)
    
    def set(self, key, value, redis_client=None):
        if redis_client is None:
            curr_redis_client = self.redis_client
        else:
            curr_redis_client = redis_client
        sorted_set_capacity = curr_redis_client.zcard(self.sorted_set_name)
        if sorted_set_capacity == self.capacity:
            self.delete(curr_redis_client)
            if redis_client == None:
                self.replicate_action_across_servers("delete")
        #If key already exists, delete it from hash set and sorted set
        if curr_redis_client.hexists(self.hash_set_name, key):
            curr_redis_client.hdel(self.hash_set_name, key)
            #Remove key from sorted set
            curr_redis_client.zrem(self.sorted_set_name, key)
        #Insert into sorted set
        curr_redis_client.hset(self.hash_set_name, key, value)
        current_time = time.time().__round__()
        curr_redis_client.zadd(self.sorted_set_name, {key: current_time})
        #Replicate data across regions only if redis_client is current redis_client
        if redis_client == None:
            self.replicate_action_across_servers("set", key, value)
    
    def replicate_action_across_servers(self, action, key=None, value=None):
        for server in self.server_util.servers:
            if server["ip_address"] != self.curr_server["ip_address"]:
                redis_client = self.server_util.get_redis_client(server)
                if action == "set":
                    self.set(key, value, redis_client)
                elif action == "delete":
                    self.delete(key, redis_client)
                elif action == "get":
                    redis_client.zrem(self.sorted_set_name, key)
                    current_time = time.time().__round__()
                    redis_client.zadd(self.sorted_set_name, {key: current_time})