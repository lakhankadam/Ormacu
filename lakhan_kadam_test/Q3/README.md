"""
Question C 

At Ormuco, we want to optimize every bits of software we write. Your goal is to write a new library that can be integrated to the Ormuco stack.
Dealing with network issues everyday, latency is our biggest problem.
Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration.
This library will be used extensively by many of our services so it needs to meet the following criteria: 

    1 - Simplicity. Integration needs to be dead simple. 

    2 - Resilient to network failures or crashes. 

    3 - Near real time replication of data across Geolocation. Writes need to be in real time. 

    4 - Data consistency across regions 

    5 - Locality of reference, data should almost always be available from the closest region 

    6 - Flexible Schema 

    7 - Cache can expire  
"""
I have implemented a Geo Distributed LRU cache with time expiration in Python with Redis as the database.
The code is in the file GeoDistributedLRUCache.py.
The above criteria are met as follows:
1. Simplicity: I have seperated the cache, server utility, servers yaml and GeoDistributedCache classes into seperate files. This ensures that new cache classes can be added
    and server utility can be changed. The servers yaml file can be changed to add new servers. The GeoDistributedCache class can be used to create a new cache object.
2. Resilient to network failures or crashes: The cache is resilient to network failures or crashes as the cache is stored in a Redis database. Redis takes snapshots of the database at regular intervals and stores it in a dump.rdb file. This file can be used to restore the database in case of a crash. Redis also has a replication feature which can be used to replicate the database to other servers. This ensures that the database is not lost in case of a crash.
3. Near real time replication of data across Geolocation. Writes need to be in real time: Once, a key is written in one of the redis servers, it is replicated to the other servers in real time. The cache.py file has a function called replicate which is used to replicate the data in case of delete, update and insert operations.
4. Data consistency across regions: The data is consistent across regions as the data is replicated in real time. The data is also consistent as the cache is stored in a Redis database.
5. Locality of reference, data should almost always be available from the closest region: server_util.py ensures that we get the nearest server and it's redis database based on client's ip address. Using the ip adrress, we get the longitude and latitude of the client. We then calculate the distance between the client and the servers and return the nearest server.
6. Flexible schema: The schema is flexible as the workers, cache, server utils and servers yaml can be scaled independently. Moreover, a new cache scheme or new server utility or new worker schema can be added without affecting the other components.
7. Cache can expire: Redis by default provides cache expiration. But since we are using least recently used cache expiry scheme, I have used sorted sets and hashmap in redis to implement that. I am using a worker deamon process that works in the background and deletes the least recently used keys from the cache with a periodicity equal to expiration time. This ensures that we delete the expired keys from the cache.

LRU Cache Implementation:
1. Insertion: A key with current timestamp is inserted in sorted sets in redis with current timestamp as the key and the actual key as the value. We also insert the key in a hashmap with the key value pair as key and value respectively. Sorted set ensures that our keys are sorted by time. Hashmap ensures that we can access the key value pair in O(1) time.
2. Update: We update the key in the hashmap and sorted set with the new value. We also update the timestamp of the key in the sorted set by first deleting the key from the sorted set and then inserting the key with the new timestamp.
3. Delete: We delete the least recently used key from the sorted set and then delete the key from the hashmap when the capacity of the cache is full. We also delete the key from the hashmap and sorted set and the worker deamon process deletes the key from the cache when the key expires periodically.
4. Get: We get the key from the hashmap and update the timestamp of the key in the sorted set by first deleting the key from the sorted set and then inserting the key with the new timestamp. This ensures that the key is the most recently used key in the sorted set.
5. We are replicating above steps for all redis servers in real time.

#Demo
In the demo we have kept cache capacity as 4.
We are inserting 6 elements sequentially in lru cache.
Now, once we move to 5th and 6th element, we see that the first two elements are deleted from the cache as the capacity is full.
Then after current_time + expiration_time we also delete keys that are expired.

#Missing Features
1. The cache is not persistent. We can make the cache persistent by using Redis RDB persistence. We can also use Redis AOF persistence. Or we can use another SQL or NoSQL database to make the cache persistent.
2. We can add workers that will replicate the data in the background. This will ensure that the data is replicated in the background and the client does not have to wait for the data to be replicated.
3. We can add a load balancer that will distribute the load among the servers. This will ensure that the servers are not overloaded.
4. We can have a master slave architecture where the master will be used for read and write operations and the slave will be used for read operations. This will ensure that the master is not overloaded.


