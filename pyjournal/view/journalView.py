import curses
import shutil
from bson import ObjectId
from datetime import datetime
from journal.dayentries import Day
from persistence import entry_collection

MONTHS = ["n/a", "January", "February", "March", "April",
          "May", "June", "July", "August",
          "September", "October", "November", "December"]

DAYS = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]

date_format = """{0} {1} {2}, {3}"""

header_format = """{hdr_char:{hdr_char}>100}
{date:^100}
{hdr_char:{hdr_char}>100}
"""

entry_by_day_format = """>{hour:>02}:{minute:>02}
id: {id}
category: {category}
tags: {tags}
 {entry_content}"""

entry_format = """{hdr_char:{hdr_char}>100}
> {weekday} {day}, {month} {year} at {hour:>02}:{minute:>02}
id: {id}
category: {category}
tags: {tags}
{hdr_char:{hdr_char}>100}
 {entry_content}"""


def get_hdr_view(day):
    date_view = date_format.format(
        DAYS[day.date.weekday()],
        MONTHS[day.date.month],
        day.date.day,
        day.date.year
    )
    return header_format.format(date=date_view, hdr_char='-')


def get_entry_by_day_view(entry):
    entry_date = datetime.fromtimestamp(entry.timestamp)
    return entry_by_day_format.format(
        id=entry._id,
        hour=entry_date.hour,
        minute=entry_date.minute,
        category=entry.category,
        tags=entry.tags,
        entry_content=entry.content
    )


def get_entry_view(entry):
    entry_date = datetime.fromtimestamp(entry.timestamp)
    return entry_format.format(
        id=entry._id,
        hour=entry_date.hour,
        minute=entry_date.minute,
        weekday=DAYS[entry_date.weekday()],
        day=entry_date.day,
        month=MONTHS[entry_date.month],
        year=entry_date.year,
        category=entry.category,
        tags=entry.tags,
        entry_content=entry.content,
        hdr_char='-'
    )


class JournalView:
    def __init__(self, entry_list):
        self.entry_list = entry_list

    def print_all_days(self):
        day = Day()
        for entry in self.entry_list:
            if not day.belongs_to_this_day(entry):
                day.set_date(datetime.fromtimestamp(entry.timestamp))
                hdr_view = get_hdr_view(day)
                print(hdr_view)
            entry_view = get_entry_by_day_view(entry)
            print(entry_view)

    def print_plain(self):
        for entry in self.entry_list:
            entry_view = get_entry_view(entry)
            print(entry_view)

    def print_with_pager(self):
        curses.wrapper(func=self.curses_pager)

    def curses_pager(self, win):
        i = 0
        entry_list = self.entry_list
        entry_info_str = "Entry {} [h]previous; [l]next; [d]elete\n"

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        t_cols = shutil.get_terminal_size()[0]
        t_rows = shutil.get_terminal_size()[1]

        entry_pad = curses.newpad(t_rows, t_cols)
        entry_pad.bkgd(curses.color_pair(1))
        entry_pad.nodelay(False)
        entry_list_delimiter = 0
        entry_pad.clear()
        entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)

        entry_changed = True
        num_lines = 0

        while True:
            if entry_changed:
                entry_pad.clear()
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                if len(entry_list) == 0:
                    empty_msg = "No entries found"
                    entry_pad.addstr(0, 0, empty_msg)
                    entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                    key = entry_pad.getkey()
                    break

                current_entry = entry_list[i]
                entry_view = get_entry_view(entry_list[i])
                entry_lines = entry_view.splitlines(keepends=True)
                entry_lines.insert(0, entry_info_str.format(i))

                num_lines = len(entry_lines)
                if num_lines <= (t_rows - 1):
                    entry_pad.addstr(entry_info_str.format(i))
                    entry_pad.addstr(entry_view)
                else:
                    for j in range(0, (t_rows - 1)):
                        entry_pad.addstr(entry_lines[j])
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                entry_list_delimiter = 0
                entry_changed = False

            key = entry_pad.getkey()
            if key == 'l' and i + 1 in range(len(entry_list)):
                i = i + 1
                entry_changed = True
            elif key == 'h' and i - 1 in range(len(entry_list)):
                i = i - 1 if i - 1 >= 0 else i
                entry_changed = True
            elif key == 'L':
                i = len(entry_list) - 1
                entry_changed = True
            elif key == 'H':
                i = 0
                entry_changed = True
            elif key == 'j' and num_lines > (t_rows - 1) and (t_rows - 1) + entry_list_delimiter + 1 <= num_lines:
                entry_list_delimiter += 1
                entry_pad.clear()
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                for j in range(entry_list_delimiter,
                               (t_rows - 1) + entry_list_delimiter):
                    entry_pad.addstr(entry_lines[j])
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                continue
            elif key == 'k' and num_lines > (t_rows - 1) and entry_list_delimiter - 1 >= 0:
                entry_list_delimiter -= 1
                entry_pad.clear()
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                for j in range(entry_list_delimiter,
                               (t_rows - 1) + entry_list_delimiter):
                    entry_pad.addstr(entry_lines[j])
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                continue
            elif key == 'd' and entry_list_delimiter == 0:
                msg = "Are you sure you want to delete this entry? [Y/n]"
                entry_pad.addstr(0, 0, msg)
                entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                while True:
                    confirm = entry_pad.getkey()
                    if confirm == 'Y':
                        _entry_collection = entry_collection.EntryCollection()
                        _entry_collection.delete_one(
                            {'_id': ObjectId(current_entry._id)})
                        entry_list.pop(i)
                        i = len(entry_list) - 1 if i == len(entry_list) else i
                        entry_changed = True
                        break
                    elif confirm == 'n' or 'N':
                        entry_pad.addstr(0, 0, entry_lines[0])
                        entry_pad.refresh(0, 0, 0, 0, t_rows, t_cols)
                        entry_changed = False
                        break
            if key == 'q':
                break
