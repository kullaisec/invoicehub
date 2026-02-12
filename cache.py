_cache = {}

def set_cache(key, value):
    _cache[key] = value

def get_cache(key):
    return _cache.get(key)

def clear_cache():
    _cache.clear()
