from .base import Reporter
import functools


def report_func(name, *report_args, condition=None, **report_kwargs):
    # function to return a decorator and using given arguments
    # condition is a callable that returns a boolean based on arguments being
    # passed to the decorated function

    def deco(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            reporter = None
            if len(args) > 0:
                reporter = getattr(args[0], 'reporter', None)
            if reporter and (condition is None or condition(*args, **kwargs)):

                with reporter.report(name, *report_args, **report_kwargs):
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    if callable(name):
        # if used as a decorator directly - ie. no call with name argument
        f = name
        name = name.__name__
        return deco(f)

    return deco