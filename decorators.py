import time

def timer(func):
    def wrapper(*a, **kw):
        t1 = time.time()
        result = func(*a, **kw)
        t2 = time.time()
        print('{} took {}'.format(func.__name__, t2 - t1))
        return result
    return wrapper