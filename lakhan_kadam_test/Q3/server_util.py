#Read servers.yaml file and return a list of servers

class ServerUtil:
    def __init__(self):
        self.servers = self.get_servers()
        self.connection_pools = self.create_connection_pools(self.servers)
    
    def get_servers(self):
        import yaml
        with open("servers.yaml", "r") as f:
            servers = yaml.safe_load(f)
        return servers.values()

    def create_connection_pools(self, servers):
        import redis
        connection_pools = {}
        for server in servers:
            redis_client = server["redis_client"]
            connection_pools[server["ip_address"]] = redis.Redis(host= redis_client["host"], port = redis_client["port"], db=0)
        return connection_pools

    def close_connection_pools(self, connection_pools):
        for connection_pool in connection_pools:
            connection_pool.disconnect()

    #Get my IP address
    def get_my_ip_address(self):
        import socket
        return socket.gethostbyname(socket.gethostname())

    #Get longitude and latitude of a given IP address
    def get_location(self, ip_address):
        import requests
        from ip2geotools.databases.noncommercial import DbIpCity
        data = DbIpCity.get(ip_address, api_key='free')
        return data.longitude, data.latitude

    #Get distance between two points based on longitude and latitude
    def get_distance(self, lon1, lat1, lon2, lat2):
        import math
        radius = 6371
        dlon = math.radians(lon2 - lon1)
        dlat = math.radians(lat2 - lat1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c
        return distance

    def get_nearest_server(self):
        min_distance = float("inf")
        nearest_server = None
        my_longitude, my_latitude = self.get_location(self.get_my_ip_address())
        for server in self.servers:
            server_longitude, server_latitude = self.get_location(server["ip_address"])
            server["distance"] = self.get_distance(my_longitude, my_latitude, server_longitude, server_latitude)
            if server["distance"] < min_distance:
                min_distance = server["distance"]
                nearest_server = server
        if nearest_server is None:
            raise Exception("No server found")
        return server
    
    def get_redis_client(self, server):
        return self.connection_pools[server["ip_address"]]
