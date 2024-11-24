import cProfile
import pstats
from memory_profiler import profile
from weakref_and_slots_comparison import measure_time


@profile
def run_measure_time():
    measure_time()


profiler = cProfile.Profile()

profiler.enable()
run_measure_time()
profiler.disable()

profiler.dump_stats("profiling_results.prof")

with open("profiling_results.txt", "w") as f:
    ps = pstats.Stats(profiler, stream=f)
    ps.sort_stats("cumulative")
    ps.print_stats()
