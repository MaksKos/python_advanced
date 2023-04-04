from unittest import TestCase
from customlist import CustomList


class TestCustomList(TestCase):

    def setUp(self) -> None:
        self.cust = CustomList([-4, 5, 7, 9])
        self.list1 = [5, 8, -9]
        self.list2 = [0, 6, -3, 7, 3, 8]

    def test_print(self):
        self.assertEqual(str(self.cust), '[-4, 5, 7, 9] sum = 17')

    def test_lt_le(self):
        self.assertTrue(CustomList([5, 3]) < CustomList([9, 0]))
        self.assertFalse(CustomList([5, 3]) < CustomList([2, 1, 3]))
        self.assertTrue(CustomList([5, 3]) <= CustomList([9, 0]))
        self.assertFalse(CustomList([5, 3]) <= CustomList([2, 1, 3]))
        self.assertTrue(CustomList([5, 3]) <= CustomList([4, 3, 1]))

    def test_gt_ge(self):
        self.assertFalse(CustomList([5, 3]) > CustomList([9, 0]))
        self.assertTrue(CustomList([5, 3]) > CustomList([2, 1, 3]))
        self.assertFalse(CustomList([5, 3]) >= CustomList([9, 0]))
        self.assertTrue(CustomList([5, 3]) >= CustomList([2, 1, 3]))
        self.assertTrue(CustomList([5, 3]) >= CustomList([4, 3, 1]))

    def test_eq_ne(self):
        self.assertTrue(CustomList() == CustomList())
        self.assertTrue(CustomList([4, 7, 9]) == CustomList([4, 7, 9]))
        self.assertTrue(CustomList([4, 7, 9]) == CustomList([20]))
        self.assertFalse(CustomList([4, 7, 9]) == CustomList([4, 7, 10]))
        self.assertFalse(CustomList() != CustomList())
        self.assertFalse(CustomList([4, 7, 9]) != CustomList([4, 7, 9]))
        self.assertFalse(CustomList([4, 7, 9]) != CustomList([20]))
        self.assertTrue(CustomList([4, 7, 9]) != CustomList([4, 7, 10]))

    def test_add_custom(self):
        test1 = self.cust + CustomList(self.list1)
        self.assertTrue(isinstance(test1, CustomList))
        self.assertEqual(test1, CustomList([1, 13, -2, 9]))
        self.assertEqual(self.cust + CustomList(), self.cust)

    def test_add_list(self):
        test1 = self.cust + self.list1  # len(cust) >
        test2 = self.cust + self.list2  # len(cust) <
        self.assertIsInstance(test1, CustomList)
        self.assertEqual(test1, CustomList([1, 13, -2, 9]))
        self.assertEqual(test2, CustomList([-4, 11, 4, 16, 3, 8]))
        self.assertEqual(self.cust + [], self.cust)
        self.assertEqual(self.cust + None, self.cust)

    def test_radd(self):
        test1 = self.list1 + self.cust  # len(a) >
        test2 = self.list2 + self.cust  # len(a) <
        self.assertIsInstance(test1, CustomList)
        self.assertEqual(test1, CustomList([1, 13, -2, 9]))
        self.assertEqual(test2, CustomList([-4, 11, 4, 16, 3, 8]))
        self.assertEqual(None + self.cust, self.cust)

    def test_sub_custom(self):
        test1 = self.cust - CustomList(self.list1)
        test2 = self.cust - CustomList(self.list2)
        self.assertIsInstance(test1, CustomList)
        self.assertEqual(test1, CustomList([-9, -3, 16, 9]))
        self.assertEqual(test2, CustomList([-4, -1, 10, 2, -3, -8]))
        self.assertEqual(self.cust - CustomList(), self.cust)
        self.assertEqual(CustomList() - self.cust, CustomList([4, -5, -7, -9]))

    def test_sub_list(self):
        test1 = self.cust - self.list1
        test2 = self.cust - self.list2
        self.assertIsInstance(test1, CustomList)
        self.assertEqual(test1, CustomList([-9, -3, 16, 9]))
        self.assertEqual(test2, CustomList([-4, -1, 10, 2, -3, -8]))
        self.assertEqual(self.cust - [], self.cust)
        self.assertEqual(self.cust - None, self.cust)

    def test_rsub(self):
        test1 = self.list1 - self.cust
        test2 = self.list2 - self.cust
        self.assertIsInstance(test1, CustomList)
        self.assertEqual(test1, CustomList([9, 3, -16, -9]))
        self.assertEqual(test2, CustomList([4, 1, -10, -2, 3, 8]))
        self.assertEqual([] - self.cust, CustomList([4, -5, -7, -9]))
        self.assertEqual(None - self.cust, CustomList([4, -5, -7, -9]))
