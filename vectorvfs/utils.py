import time
from contextlib import ContextDecorator


class PerfCounter(ContextDecorator):
    """
    Context manager and decorator to measure elapsed time.

    Usage as a context manager:
        with PerfCounter():
            ...  # code to time

    Usage as a decorator:
        @PerfCounter()
        def foo(...):
            ...

    The elapsed time is printed on exit.
    """
    def __init__(self) -> None:
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end = time.perf_counter()
        self.elapsed = end - self.start
