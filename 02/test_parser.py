import json
from unittest import TestCase, mock

from parser_fun import parse_json as parjs


class TestMessEval(TestCase):
    def setUp(self):
        pass

    def test_none(self):
        def fun():
            pass
        self.assertEqual(parjs('str', fun, None, ['word1']), 1)
        self.assertEqual(parjs('str', fun, ['key1'], None), 1)
        self.assertEqual(parjs('str', fun, None, None), 1)

    def test_empty(self):
        def fun():
            pass
        self.assertEqual(parjs('str', fun, [], ['word1']), 2)
        self.assertEqual(parjs('str', fun, ['key1'], []), 2)
        self.assertEqual(parjs('str', fun, [], []), 2)

    def test_function(self):
        json_string = json.dumps({'key1': 'word1 word2',
                                  'key2': "word1 word 3",
                                  'key3': 'word4 word1 word5'})
        fields = ['key1', 'key3', 'key8']
        keywords = ['word1', 'word4', 'word5']
        call_list = [mock.call('word1'), mock.call('word4'),
                     mock.call('word1'), mock.call('word5')]
        with mock.patch('parser_fun.string_function') as mock_fun:
            parjs(json_string, mock_fun, fields, keywords)
            self.assertEqual(mock_fun.call_count, 4)
            self.assertEqual(mock_fun.call_args_list, call_list)
