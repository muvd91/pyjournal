import unittest
import time
from datetime import datetime
from pyjournal.journal import dayentries
from pyjournal.journal.dayentries import Day
from pyjournal.journal.entry import Entry


class TestJournal(unittest.TestCase):

    def setUp(self):
        self.t1 = time.mktime(datetime(2017, 5, 20, 15).timetuple())
        self.t2 = time.mktime(datetime(2017, 5, 20, 19).timetuple())
        self.t3 = time.mktime(datetime(2017, 6, 21, 15).timetuple())
        self.t4 = time.mktime(datetime(2017, 7, 20, 15).timetuple())
        self.e1 = Entry({'_id': '1', 'timestamp': self.t1, 'content': '', 'category': '', 'tags': []})
        self.e2 = Entry({'_id': '1', 'timestamp': self.t2, 'content': '', 'category': '', 'tags': []})
        self.e3 = Entry({'_id': '1', 'timestamp': self.t3, 'content': '', 'category': '', 'tags': []})
        self.e4 = Entry({'_id': '1', 'timestamp': self.t4, 'content': '', 'category': '', 'tags': []})

    def test_get_day_list(self):
        entry_list = list()
        entry_list.append(Entry({'_id': '1', 'timestamp': self.t1, 'content': '', 'category': '', 'tags': []}))
        entry_list.append(Entry({'_id': '1', 'timestamp': self.t2, 'content': '', 'category': '', 'tags': []}))
        entry_list.append(Entry({'_id': '1', 'timestamp': self.t3, 'content': '', 'category': '', 'tags': []}))
        entry_list.append(Entry({'_id': '1', 'timestamp': self.t4, 'content': '', 'category': '', 'tags': []}))

        day_list = dayentries.get_day_list(entry_list)
        self.assertEqual(len(day_list), 3, 'Logs are spread in 3 days')

    def test_is_same_day(self):
        day = Day(self.e1)
        self.assertTrue(day.belongs_to_this_day(self.e2))
        self.assertFalse(day.belongs_to_this_day(self.e3))
        self.assertFalse(day.belongs_to_this_day(self.e4))


if __name__ == '__main__':
    unittest.main()
