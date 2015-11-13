import unittest
from pyjournal.utils import jsonTools

foo_json = '{"str_attr": "string", ' \
                        '"list_attr": ["elemOne", "elemTwo"], ' \
                        '"dict_attr": {"pi": 3.1415, "phi": 16180, "e": 2.7182}}'


class TestJsonUtils(unittest.TestCase):

    def test_serialization(self):
        test_obj = Foo()
        serialized = jsonTools.json_serialize(test_obj)
        self.assertEqual(serialized, foo_json)

    def test_deserialization(self):
        test_dict = jsonTools.json_deserialize(foo_json)
        self.assertEqual(test_dict['str_attr'], 'string')
        self.assertEqual(test_dict['list_attr'], ["elemOne", "elemTwo"])
        self.assertEqual(test_dict['dict_attr'], {"pi": 3.1415,
                                                  "phi": 16180,
                                                  "e": 2.7182})


class Foo:
    def __init__(self):
        self.str_attr = 'string'
        self.list_attr = ['elemOne', 'elemTwo']
        self.dict_attr = {'pi': 3.1415, 'phi': 16180, 'e': 2.7182}

if __name__ == '__main__':
    unittest.main()
