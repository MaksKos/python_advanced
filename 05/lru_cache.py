from collections import deque

class LRUCache:

        def __init__(self, limit=42):
            self.cache = dict()
            self.order = deque() # хранит только ключи
            self.limit = limit

        def get(self, key):
            value = self.cache.get(key)
            if value is None:
                 return None
            # move_ti_end
            return value

        def set(self, key, value):
            self.cache[key] = value
            # move_to_end

            if len(self.cache) >= self.limit:
                 self.cache.pop(self.order.pop())


cache = LRUCache(2)

cache.set("k1", "val1")
cache.set("k2", "val2")

assert cache.get("k3") is None
assert cache.get("k2") == "val2"
assert cache.get("k1") == "val1"

cache.set("k3", "val3")

assert cache.get("k3") == "val3"
assert cache.get("k2") is None
assert cache.get("k1") == "val1"


#Если удобнее, get/set можно сделать по аналогии с dict:
cache["k1"] = "val1"
print(cache["k3"])