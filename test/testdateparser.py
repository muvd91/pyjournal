import unittest
from pyjournal.ql import dateparser


class TestDateParser(unittest.TestCase):

    def test_only_hour(self):
        date_str = '20:15'
        result = dateparser.parse_str_date(date_str)
        self.assertEqual(result.hour, 20)
        self.assertEqual(result.minute, 15)

    def test_date(self):
        date_str = '23/04/1985'
        result = dateparser.parse_str_date(date_str)
        self.assertEqual(result.year, 1985)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.day, 23)

    def test_datetime(self):
        date_str = '21:09 23/04/1985'
        result = dateparser.parse_str_date(date_str)
        self.assertEqual(result.year, 1985)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.day, 23)
        self.assertEqual(result.hour, 21)
        self.assertEqual(result.day, 23)
