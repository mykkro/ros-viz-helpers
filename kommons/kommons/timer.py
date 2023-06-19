import time
from contextlib import contextmanager
import timeit
    

# nice way to report running times
@contextmanager
def timer(name):
    t0 = time.time()
    yield
    print(f'[{name}] done in {time.time() - t0:.2f} s')


class Stopwatch(object):
    """\
    Simple Stopwatch (for debugging)
    """

    def __init__(self):
        self.watches = {}

    def start(self, name : str = "default"):
        """\
        Starts a watch with given name.
        """
        self.watches[name] = timeit.default_timer()

    def elapsed(self, name : str = "default") -> float:
        """\
        Returns elapsed time in seconds for a clock with given name.
        """
        time_start = self.watches[name]
        time_end = timeit.default_timer()
        return time_end - time_start

    def report(self, name : str = "default", message : str = ""):
        """\
        Prints out elapsed time with custom text message.
        """
        print(f"[{message}{name}] Elapsed time [s]:", self.elapsed(name))
