import unittest
from pyjournal.ql import parser


class TestQL(unittest.TestCase):

    def test_get_all_query(self):
        query = "get all"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 1, "Should contain only 1 members")
        self.assertEqual(template['verb'], 'get', "Query was a GET command")
        query = "get entries"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 1, "Should contain only 1 members")
        self.assertEqual(template['verb'], 'get', "Query was a GET command")

    def test_get_category_query(self):
        query = "get dreams"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 2, "Should contain only 2 members")
        self.assertEqual(template['verb'], 'get', "Query was a GET command")
        self.assertEqual(template['category'], 'dreams', "Query requested dreams")

    def test_edit__query(self):
        query = "edit 258en02ns"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 2, "Should contain only 2 members")
        self.assertEqual(template['verb'], 'edit', "Query was a EDIT command")
        self.assertEqual(template['_id'], '258en02ns', "Should contain specified id")

    def test_write_query(self):
        query = "write"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 1, "Should contain only 1 members")
        self.assertEqual(template['verb'], 'write', "Query is an write command")

    def test_delete_one_query(self):
        query = "delete 50sn437f5573hf94"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 2, "Should contain only 2 members")
        self.assertEqual(template['verb'], 'delete', "Query is a delete command")
        self.assertEqual(template['_id'], '50sn437f5573hf94', "Should contain specified id")

    def test_display_setting(self):
        query = "display byday"
        template = parser.get_query_template(query)
        self.assertEqual(len(template), 2, "Should contain only 2 members")
        self.assertEqual(template['verb'], 'display', "Query is a display configuration")
        self.assertEqual(template['display'], 'byday', "display byday")
