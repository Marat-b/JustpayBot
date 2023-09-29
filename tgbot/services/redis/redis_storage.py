import asyncio
from json import dumps, loads

from redis import Redis

from tgbot import config


class RedisStorage:
   def __init__(self):
       print(config.load_config('.env').redis.dsn())
       self.store = Redis() #.from_url(config.load_config('.env').redis.dsn())
       self.hash_name = config.load_config('.env').redis.redis_hash_name

   def set(self,item):
       values = list(item.values())
       print(f'item={values[0]}')
       self.store.hset(self.hash_name, f'{values[0]}:{values[1]}', dumps(item))
   def set_list(self, dicts: list):
        # print(*d)
        for item in dicts:
            print(item)
            # keys = item.keys()
            print((*item,)[0])
            i = (*item,)
            values = list(item.values())
            # print(i["a"])
            self.store.hset(self.hash_name, f'{values[0]}:{values[1]}', dumps(item))
   def get(self,item):
       values = list(item.values())
       stuff = self.store.hget(self.hash_name, f'{values[0]}:{values[1]}')
       return loads(stuff)
   def remove(self):
        self.store.delete(self.hash_name)

   def close_con(self):
       self.store.close()