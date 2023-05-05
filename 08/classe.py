# pylint: disable=missing-docstring

import weakref as wr


class GameAccount:

    def __init__(self, nik_name: str, credit: int, func, games: set) -> None:
        self.nik = nik_name
        self.credit = credit
        self.games = games
        self.func = func


class GameAccountSlot:

    __slots__ = ('nik', 'credit', 'games', 'func')

    def __init__(self, nik_name: str, credit: int, func, games: set) -> None:
        self.nik = nik_name
        self.credit = credit
        self.games = games
        self.func = func


class GameAccountWeak:

    def __init__(self, nik_name: str, credit: int, func, games: set) -> None:
        self.nik = nik_name
        self.credit = credit
        self.games = wr.ref(games)
        self.func = wr.ref(func)
