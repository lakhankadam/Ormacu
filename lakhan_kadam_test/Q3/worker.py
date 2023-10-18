# Worker who cleans the expired keys from cache for all the servers
import threading
import time
class Worker:
    def __init__(self, expiration_time, redis_clients, name):
        self.sorted_set_name = name + "_sorted_set"
        self.hash_set_name = name + "_hash_set"
        self.expiration_time = expiration_time
        self.redis_clients = redis_clients
        self.workers = []
        self.create_workers()
        self.start_workers()

    def create_workers(self):
        for redis_client in self.redis_clients:
            t = threading.Thread(target=self.clear_cache, daemon=True, args=(redis_client,))
            self.workers.append(t)

    def clear_cache(self, redis_client):
        current_time = time.time().__round__()
        keys = redis_client.zrangebyscore(self.sorted_set_name, 0, current_time - self.expiration_time, withscores=False)
        redis_client.zremrangebyscore(self.sorted_set_name, 0, current_time - self.expiration_time)
        print("Deleting keys: ", keys)
        if keys:
            redis_client.hdel(self.hash_set_name, *keys)
    
    
    def start_workers(self):
        while True:
            for i, worker in enumerate(self.workers):
                print("I am worker: ", i + 1)
                worker.start()
                time.sleep(self.expiration_time)
                worker.join()
            self.workers = []
            self.create_workers()

            
        
