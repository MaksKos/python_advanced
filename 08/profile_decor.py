# pylint: disable=missing-docstring

import cProfile


def profile_deco(func):

    prof = cProfile.Profile()

    def wrapper(*args, **kwargs):
        retval = prof.runcall(func, *args, **kwargs)
        return retval

    wrapper.print_stat = prof.print_stats
    return wrapper


if __name__ == '__main__':

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
