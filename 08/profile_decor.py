# pylint: disable=missing-docstring

import cProfile, pstats, io
import functools

def profile_deco(func):
    pr = cProfile.Profile()
    #func.print_stat = None
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr) #.sort_stats("cumulative")
        func.print_stat = ps.print_stats
        return result
    #wrapper.print_stat = func.print_stat
    return wrapper

def profileit(func):
    prof = cProfile.Profile()
    s = io.StringIO()
    def wrapper(*args, **kwargs):
        retval = prof.runcall(func, *args, **kwargs)
        ps = pstats.Stats(prof, stream=s)
        s.truncate(0)
        ps.print_stats()
        return retval
    def get():
        print(s.getvalue())
    wrapper.print_stat = get
    return wrapper

def profile(func):
    prof = cProfile.Profile()

    def wrapper(*args, **kwargs):
        
        retval = prof.runcall(func, *args, **kwargs)
        return retval
    
    def get():
        ps = pstats.Stats(prof)
        ps.print_stats()
    wrapper.print_stat = get
    return wrapper


if __name__ == '__main__':

    @profile
    def add(a, b):
        return a + b

    @profile
    def sub(a, b):
        return a - b

    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()    # выводится результат профилирования суммарно по всем вызовам функции add (всего два вызова)
    sub.print_stat()   # выводится результат профилирования суммарно по всем вызовам функции sub (всего один вызов)