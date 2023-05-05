# pylint: disable=missing-docstring

import time
import weakref as wr
import cProfile, pstats, io
from memory_profiler import profile
from classe import GameAccount, GameAccountSlot, GameAccountWeak

# Для cProfile закомментирвать @profile
# Для memory_profile закомментирвать все связанное с cProfile

DEFAULT_GAME = {"GTA", "CS", "BF4"}
GAMES = {'Empire', 'SimCity'}
NAME = 'Alex'
NUM_INST = 10_000


def function():
    """
    Emulate some functuion
    """
    return 5


def another_function():
    """
    Emulate some functuion
    """
    return 6


# @profile
def run_ordinary(n):

    t_start = time.time()
    accounts = [GameAccount(NAME, i, function, DEFAULT_GAME) for i in range(n)]
    t_stop = time.time()
    print(f'\t Create time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        nik = acc.nik
        credit = acc.credit
        func = acc.func
        games = acc.games
    t_stop = time.time()
    print(f'\t Read  time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        acc.nik = 'MOnster2'
        acc.credit += 1
        acc.func = another_function
        acc.games = GAMES
    t_stop = time.time()
    print(f'\t Write  time: {t_stop-t_start}')


# @profile
def run_slots(n):

    t_start = time.time()
    accounts = [GameAccountSlot(NAME, i, function, DEFAULT_GAME) for i in range(n)]
    t_stop = time.time()
    print(f'\t Create time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        nik = acc.nik
        credit = acc.credit
        func = acc.func
        games = acc.games
    t_stop = time.time()
    print(f'\t Read  time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        acc.nik = 'MOnster2'
        acc.credit += 1
        acc.func = another_function
        acc.games = GAMES
    t_stop = time.time()
    print(f'\t Write  time: {t_stop-t_start}')


# @profile
def run_weak(n):

    t_start = time.time()
    accounts = [GameAccountWeak(NAME, i, function, DEFAULT_GAME) for i in range(n)]
    t_stop = time.time()
    print(f'\t Create time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        nik = acc.nik
        credit = acc.credit
        func = acc.func()
        games = acc.games()
    t_stop = time.time()
    print(f'\t Read  time: {t_stop-t_start}')

    t_start = time.time()
    for acc in accounts:
        acc.nik = 'MOnster2'
        acc.credit += 1
        acc.func = wr.ref(another_function)
        acc.games = wr.ref(GAMES)
    t_stop = time.time()
    print(f'\t Write  time: {t_stop-t_start}')


if __name__ == "__main__":

    pr = cProfile.Profile()
    pr.enable()

    print(f'Toatal instance for each class: {NUM_INST}')

    print(f"\nCASE 1: ordinary class <{GameAccount.__name__}>\n")
    run_ordinary(NUM_INST)

    print(f"\nCASE 2: slots class <{GameAccountSlot.__name__}>\n")
    run_slots(NUM_INST)

    print(f"\nCASE 3: weakref class <{GameAccountWeak.__name__}>\n")
    run_weak(NUM_INST)

    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
