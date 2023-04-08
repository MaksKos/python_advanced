# pylint: disable=missing-docstring

from unittest import TestCase
from descriptor import RubleConvertation, HumanTemperature, AccountRuletka


class TestRubleConv(TestCase):

    def setUp(self) -> None:
        RubleConvertation._avaible_currency = {
            'RUB': 1,
            'USD': 80,
            'EUR': 90,
        }

        class Bank:

            eur = RubleConvertation('EUR')
            usd = RubleConvertation('USD')

            def __init__(self, money):
                self.eur = money
                self.usd = money

        self.Bank = Bank

    def test_set_curr(self):
        with self.assertRaises(ValueError):
            RubleConvertation(None)
        with self.assertRaises(TypeError) as err:
            RubleConvertation('FR')
        self.assertEqual(str(err.exception), "This currency='FR' is not exist")

    def test_class(self):
        self.assertIsNone(self.Bank.eur)
        self.assertIsNone(self.Bank.usd)

    def test_inst(self):
        alpha = self.Bank(1600)
        self.assertAlmostEqual(alpha.eur, 1600/90)
        self.assertAlmostEqual(alpha.usd, 1600/80)
        alpha.eur = 2450.2
        self.assertAlmostEqual(alpha.eur, 2450.2/90)
        self.assertAlmostEqual(alpha.usd, 1600/80)
        alpha.eur = -100
        self.assertEqual(alpha.eur, 0)
        with self.assertRaises(ValueError) as err:
            alpha.usd = '100'
        self.assertEqual(str(err.exception), "val='100' is not an money!")

    def test_n_inst(self):
        alpha = self.Bank(1000)
        vtb = self.Bank(2000)
        self.assertAlmostEqual(alpha.eur, 1000/90)
        self.assertAlmostEqual(vtb.eur, 2000/90)
        alpha.eur = 632.5
        self.assertAlmostEqual(alpha.eur, 632.5/90)
        self.assertAlmostEqual(vtb.eur, 2000/90)


class TestHumanTemperature(TestCase):

    def setUp(self) -> None:

        class Human:

            temp = HumanTemperature()

            def __init__(self, temp=36.6):
                self.temp = temp

        self.Human = Human

    def test_class(self):
        self.assertIsNone(self.Human.temp)

    def test_inst(self):
        mike = self.Human()
        self.assertEqual(mike.temp, str(36.6) + ' healthy')
        mike.temp = 36.9
        self.assertEqual(mike.temp, str(36.9) + ' healthy')
        mike.temp = 10
        self.assertEqual(mike.temp, str(35) + " weakness")
        mike.temp = 50
        self.assertEqual(mike.temp, str(42) + " call to doctor")
        mike.temp = 38.1
        self.assertEqual(mike.temp, str(38.1) + ' get antipyretic')
        with self.assertRaises(ValueError) as err:
            mike.temp = '40'
        self.assertEqual(str(err.exception), "val='40' is not an temperatue!")


class TestAccountRuletka(TestCase):

    def setUp(self) -> None:
        AccountRuletka._loss = 100

        class Player:

            balance = AccountRuletka(1000)

        self.Player = Player

    def test_init(self):
        with self.assertRaises(ValueError):
            AccountRuletka(None)
        with self.assertRaises(TypeError) as err:
            AccountRuletka('text')
        self.assertEqual(str(err.exception), "This amount='text' is not money")

    def test_class(self):
        self.assertIsNone(self.Player.balance)

    def test_inst(self):
        player = self.Player()
        with self.assertRaises(AttributeError):
            player.balance = 1000
        for i in range(10):
            self.assertEqual(player.balance, 900 - i*100)
        self.assertEqual(player.balance, 0)

    def test_n_inst(self):
        player1 = self.Player()
        player2 = self.Player()
        self.assertEqual(player1.balance, 900)
        self.assertEqual(player2.balance, 800)
