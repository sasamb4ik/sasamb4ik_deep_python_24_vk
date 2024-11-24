import cProfile
import pstats
from functools import wraps

def profile_deco(func):
    profiler = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result

    def print_stat():
        stats = pstats.Stats(profiler)
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats()

    wrapper.print_stat = print_stat
    return wrapper

@profile_deco
def add(a, b):
    return a + b

@profile_deco
def sub(a, b):
    return a - b

add(1, 2)
add(4, 5)
sub(4, 5)

add.print_stat()
sub.print_stat()
