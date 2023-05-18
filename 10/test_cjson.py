# pylint: disable=missing-docstring

from unittest import TestCase
import json
import cjson


class TestCjson(TestCase):

    def test_dumps(self):
        data = {"key1": "value", "key 2": "value 2 ", "45": 56,
                "temp": 9.76, "5.78": "100"}
        json_test = cjson.dumps(data)
        json_real = json.dumps(data)
        self.assertEqual(json_real, json_test)

    def test_load(self):

        json_str = '{"key1": "value1", "key 2": "value 2 ", "45": 56, "temp": 9.76, "5.78": "100"}'
        data_test = cjson.loads(json_str)
        data_real = json.loads(json_str)
        self.assertEqual(data_real, data_test)
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))

        self.assertEqual(cjson.loads('{ }'), {})

    def test_dump_err(self):

        data_wrong_key = {9: "string"}
        data_wrong_val = {"key": ["val"]}
        with self.assertRaises(TypeError):
            cjson.dumps("str")

        with self.assertRaises(TypeError):
            cjson.dumps(data_wrong_key)

        with self.assertRaises(TypeError):
            cjson.dumps(data_wrong_val)

    def test_load_err(self):

        with self.assertRaises(TypeError):
            cjson.loads(5)

        with self.assertRaises(TypeError):
            cjson.loads("")

        with self.assertRaises(TypeError):
            cjson.loads('some string ')

        with self.assertRaises(TypeError):
            cjson.loads('{"some": "string" ')

        with self.assertRaises(TypeError):
            cjson.loads('"some": "string"}')

        with self.assertRaises(TypeError):
            cjson.loads(' {"some": "string"}')

        with self.assertRaises(TypeError):
            cjson.loads('{"some" "string"}')
