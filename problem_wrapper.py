"""
Support for exam problems as functions
"""
import sys

# From http://code.activestate.com/recipes/577283-decorator-to-expose-local-variables-of-a-function-/
# persistent_locals2 has been co-authored with Andrea Maffezzoli
class wrapped_problem(object):
    def __init__(self, func):
        self._locals = {}
        self.func = func
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        def tracer(frame, event, arg):
            if event=='return':
                self._locals = frame.f_locals.copy()

        # tracer is activated on next call, return or exception
        sys.setprofile(tracer)
        try:
            # trace the function call
            res = self.func(*args, **kwargs)
        finally:
            # disable tracer and replace with old one
            sys.setprofile(None)
        return res

    def clear_locals(self):
        self._locals = {}

    @property
    def locals(self):
        return self._locals
