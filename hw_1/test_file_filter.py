from unittest import TestCase
from io import StringIO

from file_filter import file_filter


class TestMessEval(TestCase):

    def setUp(self):
        self.file = StringIO()

    def test_list(self):
        with self.assertRaises(ValueError) as err:
            gen = file_filter(self.file, [])
            next(gen)
        self.assertEqual(str(err.exception), 'Empty list')

    def test_seek(self):
        self.file.write('some text')
        gen = file_filter(self.file, ['text'])
        self.assertEqual(next(gen), 'some text')

    def test_generator_case(self):
        str_1 = "This text is very important\n"
        str_2 = "this TeXt is very imporTant\n"
        self.file.write(str_1)
        self.file.write(str_2)
        self.file.write("This texting is not important\n")
        gen = file_filter(self.file, ['text'])
        self.assertEqual(next(gen), str_1)
        self.assertEqual(next(gen), str_2)
        with self.assertRaises(StopIteration):
            next(gen)

        gen = file_filter(self.file, ['texts'])
        with self.assertRaises(StopIteration):
            next(gen)

    def test_generator_words(self):
        words = ['type', 'sim']
        str_1 = 'The Type of object\n'
        str_2 = 'this SIM is you\n'
        str_3 = 'type of sim\n'

        self.file.write(str_1)
        self.file.write(str_2)
        self.file.write(str_3)

        gen = file_filter(self.file, words)
        self.assertEqual(next(gen), str_1)
        self.assertEqual(next(gen), str_2)
        self.assertEqual(next(gen), str_3)

    def tearDown(self):
        self.file.close()
