import os
import ql.dateparser
from ql.parser import ParseValidationError
from utils import interactiveutils
from interactive import file_interactive_crud

from datetime import datetime

from pymongo.errors import ConnectionFailure

from journal.entry import Entry
from persistence.entry_collection import EntryCollection
from persistence.file_collection import FileCollection
from utils import jsonTools
from view.journalView import JournalView

# Globals
DATA_DIR = os.path.expandvars('${HOME}/pyjournal/data/journal.json')

entry_collection = None

try:
    entry_collection = EntryCollection()
    file_collection = FileCollection()
    print("You've logged {} entries!".format(entry_collection.count()))
except ConnectionFailure:
    print("We couldn't find a mongod instance.")


def insert_or_update(query=None, is_file_entry=False):
    global DATA_DIR
    global entry_collection

    file_id = None
    # Set file id
    if is_file_entry:
        all_files = file_collection.get_all_files()
        _file = interactiveutils.print_and_select_files(all_files)
        file_id = _file['_id']

    # Set Content
    if query is None:
        entry_obj = Entry()
        entry_content = interactiveutils.open_document_editor()
    else:
        entry_obj = entry_collection.find_one(query)
        entry_content = interactiveutils.open_document_editor(
            entry_obj.content)

    entry_obj.set_content(entry_content)

    # Set Category
    while True:
        print("Enter the category of this entry")
        category_input = interactiveutils.not_empty_input(
            "Category cannot be empty", "category > ")
        categories = get_categories()
        if category_input not in categories:
            print("This is a new category, do you want to continue?")
            confirm = interactiveutils.yes_no_input("Type yes or no", 'y/N > ')
            if confirm:
                break
        else:
            break
    entry_obj.set_category(category_input)

    # Set tags
    print("Tags: Comma-separated. Enter when finished")
    old_tags = ','.join(entry_obj.tags)
    print(old_tags)
    tag_input = interactiveutils.format_tag(input("tags > "))
    entry_obj.set_tag(tag_input)

    # Set Timestamp
    while True:
        if query is None:
            default_date = datetime.now()
        else:
            default_date = datetime.fromtimestamp(entry_obj.timestamp)
        print("Enter entry date. Supported formats samples: '20:23' or '23/02/2005' or '20:23 23/02/2005'")
        print("No input defaults to {}".format(default_date.strftime('%c')))
        input_date_str = input("date > ")
        if input_date_str != '':
            try:
                input_date = ql.dateparser.parse_str_date(input_date_str)
            except ParseValidationError as e:
                print("{}: Try again.".format(e))
                continue
        else:
            input_date = default_date
        print("Entry will be saved with datetime {}".format(
            input_date.strftime('%c')))
        print("Is this correct?")
        confirm = interactiveutils.yes_no_input("Type yes or no.", "y/N > ")
        if confirm:
            entry_obj.timestamp = input_date.timestamp()
            break

    # Insert in db or save to local file
    try:
        if query is None:
            entry_collection.insert(entry_obj)
        else:
            entry_collection.update_one(query, entry_obj)
        json_obj = jsonTools.json_serialize(entry_obj)
    except ConnectionFailure:
        print("An error occurred while saving your log in the Database. Saving log in local file")
        interactiveutils.save_in_file(DATA_DIR, json_obj)
    print(json_obj)


def read(query):
    entries = entry_collection.find(query)
    if len(entries) == 0:
        print("No entries found")
        return
    view = JournalView(entries)
    view.print_with_pager()


def delete(query):
    entry = entry_collection.find_one(query)
    if entry is None:
        print("No entry found with id {}".format(query['_id']))
        return
    print("Are you sure you want to delete this log?")
    print("category: " + entry.category)
    longer_content = "..." if len(entry.content) > 20 else ""
    print("content: {0} {1}".format(entry.content[:20], longer_content))
    response = interactiveutils.yes_no_input("Yes or No", "y/N > ")
    if response:
        count = entry_collection.delete_one(query)
        print("{} document deleted".format(count))


def get_categories():
    categories = set()
    for _entry in entry_collection.find_with_projection(dict(), ['category']):
        categories.add(_entry['category'])
    return categories


def get_file_entries():
    files = file_collection.get_all_files()
    file = file_interactive_crud.print_and_select_files(files)
    read({'file_id': file['_id']})
