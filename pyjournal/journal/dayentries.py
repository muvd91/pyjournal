from datetime import datetime


def get_day_list(entry_list):
    _day = Day()
    day_list = []
    for entry in entry_list:
        if _day.num_entries() == 0:
            _day = Day(entry)
            day_list.append(_day)
        elif not _day.belongs_to_this_day(entry):
            _day = Day(entry)
            day_list.append(_day)
        else:
            _day.add_log(entry)
    return day_list


class Day:
    def __init__(self, initial_entry=None):
        self.entryList = []
        self.date = None
        if initial_entry is None:
            return
        self.date = datetime.fromtimestamp(initial_entry.timestamp)
        self.entryList.append(initial_entry)

    def set_date(self, date):
        self.date = date

    def add_log(self, entry):
        self.entryList.append(entry)
        return True

    def belongs_to_this_day(self, entry):
        if self.date is None:
            return False
        return entry.get_date_from_ts() == (
            self.date.day, self.date.month, self.date.year)

    def num_entries(self):
        return len(self.entryList)
