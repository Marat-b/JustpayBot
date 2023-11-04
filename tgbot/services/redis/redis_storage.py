import asyncio
from json import dumps, loads

from redis import Redis

from tgbot import config


class RedisStorage:
    def __init__(self):
        print(config.load_config('.env').redis.dsn())
        self.is_connected = False
        self.store = Redis(host=config.load_config('.env').redis.redis_host, port=config.load_config(
            '.env').redis.redis_port)  # .from_url(config.load_config('.env').redis.dsn())
        self.hash_name = config.load_config('.env').redis.redis_hash_name
        try:
            self.store.ping()
            self.is_connected = True
        except Exception:
            print("Redis is not connected")
            self.store.close()

    def __del__(self):
        self.store.close()

    def set(self, item):
        if self.is_connected:
            values = list(item.values())
            print(f'item={values[0]}')
            self.store.hset(self.hash_name, f'{values[0]}:{values[1]}', dumps(item))

    def set_list(self, dicts: list):
        if self.is_connected:
            # print(*d)
            for item in dicts:
                print(item)
                # keys = item.keys()
                print((*item,)[0])
                i = (*item,)
                values = list(item.values())
                # print(i["a"])
                self.store.hset(self.hash_name, f'{values[0]}:{values[1]}', dumps(item))

    def get(self, item):
        values = list(item.values())
        stuff = self.store.hget(self.hash_name, f'{values[0]}:{values[1]}')
        return loads(stuff)

    def remove(self):
        if self.is_connected:
            self.store.delete(self.hash_name)

    def close_con(self):
        self.store.close()
