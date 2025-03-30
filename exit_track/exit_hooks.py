import sys
import atexit
import signal

EXIT_STATUS = 0
original_exit = sys.exit


def custom_exit(code):
    global EXIT_STATUS
    EXIT_STATUS = code
    original_exit(code)


sys.exit = custom_exit


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
    return {"file name": sys.argv[0], "exit status": EXIT_STATUS}


exit_hooks = ExitHooks()
atexit.register(exit_hooks._run_callbacks)
for sig in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, lambda signum, frame: exit_hooks._run_callbacks())

DEBUG = False
if DEBUG:
    exit_hooks.add_exit_hook(lambda: print(get_exit_info()))

__all__ = ["EXIT_STATUS", "get_exit_info", "exit_hooks"]
