import sys
import atexit


class ExitHooks:
    def __init__(self):
        self.callbacks = []

    def add_exit_hook(self, func, *args, **kwargs):
        self.callbacks.append((func, args, kwargs))

    def _run_callbacks(self):
        for func, args, kwargs in reversed(self.callbacks):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Exit hook failed: {e}", file=sys.stderr)


def get_exit_info():
    return f"file name: {sys.argv[0]}"


exit_hooks = ExitHooks()
atexit.register(exit_hooks._run_callbacks)

DEBUG = True
if DEBUG:
    exit_hooks.add_exit_hook(lambda: print(get_exit_info()))

__all__ = ["get_exit_info", "exit_hooks"]
