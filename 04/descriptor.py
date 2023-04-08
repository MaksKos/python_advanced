# pylint: disable=missing-docstring

class RubleConvertation:

    _avaible_currency = {
        'RUB': 1,
        'USD': 81,
        'EUR': 85
    }

    def __set_name__(self, owner, name):
        self.name = "_size" + name

    def __init__(self, currency: str = "RUB") -> None:
        if currency is None:
            raise ValueError
        if currency not in self._avaible_currency:
            raise TypeError(f"This {currency=} is not exist")
        self._coeff = self._avaible_currency[currency]

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return getattr(obj, self.name)/self._coeff

    def __set__(self, obj, val):
        if obj is None:
            return None
        if not isinstance(val, (float, int)):
            raise ValueError(f"{val=} is not an money!")
        val = max(0, val)
        return setattr(obj, self.name, val)


class HumanTemperature:

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        val = getattr(obj, self.name)
        if val < 35.5:
            return str(val) + " weakness"
        if val < 37:
            return str(val) + ' healthy'
        if val < 38.5:
            return str(val) + ' get antipyretic'
        return str(val) + ' call to doctor'

    def __set__(self, obj, val):
        if obj is None:
            return None
        if not isinstance(val, (float, int)):
            raise ValueError(f"{val=} is not an temperatue!")
        val = max(35, val)
        val = min(42, val)
        return setattr(obj, self.name, val)


class AccountRuletka:
    """
    Все игроки (Экземпляры <obj_type>)
    расходуют общий банк размера amount
    """
    _loss = 100

    def __init__(self, amount):
        if amount is None:
            raise ValueError
        if not isinstance(amount, (int, float)):
            raise TypeError(f"This {amount=} is not money")
        self._amount = amount

    def __get__(self, obj, obj_type):
        if obj is None:
            return None
        self._amount -= self._loss
        if self._amount < 0:
            return 0
        return self._amount

    def __set__(self, obj, value):
        raise AttributeError
