import json
from unittest import TestCase, mock

from parser_fun import parse_json as parjs


class TestMessEval(TestCase):

    def setUp(self):
        self.str_fun = mock.Mock()
        self.json = 'some_string'

    def test_none(self):
        self.assertEqual(parjs(None, self.str_fun), 'json is None')
        self.assertEqual(parjs(self.json, None), 'callback is None')

    def test_none_lists(self):
        self.assertIsNone(parjs(self.json, self.str_fun, keywords=['word1']))
        self.assertIsNone(parjs(self.json, self.str_fun, required_fields=['key1']))

    def test_function(self):
        json_string = json.dumps({'key1': 'word1 word2',
                                  'key2': "word1 word 3",
                                  'key3': 'word4 word1 word5'})
        fields = ['key1', 'key3', 'key8']
        keywords = ['word1', 'word4', 'word5', 'word10']  # дописать 'word10'
        call_list = [mock.call('key1', 'word1'), mock.call('key3', 'word4'),
                     mock.call('key3', 'word1'), mock.call('key3', 'word5')]
        with mock.patch('parser_fun.string_function') as mock_fun:
            parjs(json_string, mock_fun, fields, keywords)
            self.assertEqual(mock_fun.call_count, 4)
            self.assertEqual(mock_fun.call_args_list, call_list)
