# pylint: disable=missing-docstring

from unittest import TestCase
from custommeta import CustomMeta

DEFAUL_X = 50
DEFAULT_LINE = 100
DEFAULT_VAL = 95
DEFAUL_TEST = 'test_mess'


class TestCustomList(TestCase):

    def setUp(self) -> None:
        class CustomClass(metaclass=CustomMeta):
            x = DEFAUL_X

            def __init__(self, val=DEFAULT_VAL):
                self.val = val

            def line(self):
                return DEFAULT_LINE

            def __str__(self):
                return "Custom_by_metaclass"

        self.TestClass = CustomClass

    def test_class(self):
        self.assertEqual(self.TestClass.custom_x, DEFAUL_X)
        self.TestClass.custom_x = DEFAUL_TEST
        self.assertEqual(self.TestClass.custom_x, DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            self.TestClass.x

    def test_class_dynamic(self):
        self.TestClass.var = DEFAUL_TEST
        self.assertEqual(self.TestClass.custom_var, DEFAUL_TEST)
        self.TestClass.custom_var = 2*DEFAUL_TEST
        self.assertEqual(self.TestClass.custom_var, 2*DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            self.TestClass.var

    def test_class_dynamic_magic(self):
        self.TestClass.__add__ = DEFAUL_TEST
        self.assertEqual(self.TestClass.__add__, DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            self.TestClass.custom___add__

    def test_class_name_like_prefix(self):
        self.TestClass.custom_ = DEFAUL_TEST
        self.assertEqual(self.TestClass.custom_custom_, DEFAUL_TEST)
        self.TestClass.custom_custom_ = 2*DEFAUL_TEST
        self.assertEqual(self.TestClass.custom_custom_, 2*DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            self.TestClass.custom_

    def test_instance(self):
        inst = self.TestClass()
        self.assertEqual(inst.custom_x, DEFAUL_X)
        self.assertEqual(inst.custom_val, DEFAULT_VAL)
        self.assertEqual(inst.custom_line(), DEFAULT_LINE)
        self.assertEqual(str(inst), "Custom_by_metaclass")
        inst = self.TestClass(640)
        self.assertEqual(inst.custom_val, 640)
        self.assertEqual(self.TestClass.custom_x, DEFAUL_X)

    def test_instance_error(self):
        inst = self.TestClass()
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            inst.yyy

    def test_instance_dynamic(self):
        inst = self.TestClass()
        inst.dynamic = DEFAUL_TEST
        self.assertEqual(inst.custom_dynamic, DEFAUL_TEST)
        inst.custom_dynamic = 2*DEFAUL_TEST
        self.assertEqual(inst.custom_dynamic, 2*DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            inst.dynamic

    def test_instance_dynamic_magic(self):
        inst = self.TestClass()
        inst.__add__ = DEFAUL_TEST
        self.assertEqual(inst.__add__, DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            inst.custom___add__

    def test_instance_name_like_prefix(self):
        inst = self.TestClass()
        inst.custom_ = DEFAUL_TEST
        self.assertEqual(inst.custom_custom_, DEFAUL_TEST)
        inst.custom_custom_ = 2*DEFAUL_TEST
        self.assertEqual(inst.custom_custom_, 2*DEFAUL_TEST)
        with self.assertRaises(AttributeError):
            inst.custom_
