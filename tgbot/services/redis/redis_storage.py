import asyncio
from json import dumps, loads

from redis.asyncio import Redis

from tgbot import config


class RedisStorage:
   def __init__(self, loop):
       # self.loop = asyncio.get_event_loop()
       print(config.load_config('.env').redis.dsn())
       self.loop = loop
       self.store = Redis().from_url(config.load_config('.env').redis.dsn())
       self.hash_name = config.load_config('.env').redis.redis_hash_name

   async def set(self,item):
        await self.store.hset(self.hash_name, f'{(*item,)[0]}:{(*item,)[1]}', dumps(item))
        # self.loop.run_until_complete(self.store.hset(self.hash_name, f'{(*item,)[0]}:{(*item,)[1]}', dumps(item)))
   def set_list(self, dicts: list):
        # print(*d)
        for item in dicts:
            print(item)
            # keys = item.keys()
            print((*item,)[0])
            i = (*item,)
            # print(i["a"])
            self.loop.run_until_complete(self.store.hset(self.hash_name,f'{(*item,)[0]}:{(*item,)[1]}', dumps(item)))
   def get(self,item):
        stuff =  self.loop.run_until_complete(self.store.hget(self.hash_name, f'{(*item,)[0]}:{(*item,)[1]}'))
        return loads(stuff)
   def remove(self):
        self.loop.run_until_complete(self.store.delete(self.hash_name))

   def close_con(self):
       self.loop.run_until_complete(self.store.close())