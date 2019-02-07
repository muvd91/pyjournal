import os
import tempfile
import subprocess

yes_no_responses = list()
yes_responses = ['y', 'Y', 'yes', 'Yes', 'yep']
no_responses = ['n', 'N', 'no', 'No', 'nope']
yes_no_responses.extend(yes_responses)
yes_no_responses.extend(no_responses)


def open_document_editor(pre_content=None):
    temp_file = tempfile.NamedTemporaryFile(
        mode='r+', suffix=".tmp", encoding="utf-8")
    editor = os.environ.get("EDITOR", "vimx")
    temp_file.write('#Type your log!. Save and quit when finished.\n'
                    '#Lines starting with # will not be saved on your log!\n')
    if pre_content is not None:
        temp_file.write(pre_content)
    temp_file.flush()
    subprocess.call([editor, temp_file.name])
    temp_file.seek(0)
    file_content = map(lambda e: ''.join(e), temp_file)
    def no_comments(e): return not e[0] == '#'
    file_content = filter(no_comments, file_content)
    content = ''.join(file_content)
    return content


def format_tag(str_input):
    lst = str_input.split(',')
    ls = list(map(lambda e: e.lstrip().rstrip(), lst))
    def no_whitespace(e): return not(e == '\n' or e ==
                                     '\t' or e == '' or ' ' in e or '\t' in e)
    return list(filter(no_whitespace, ls))


def restricted_input(allowed_response=[], msg='', caret='> '):
    response = input(caret)
    while response not in allowed_response:
        print(msg)
        response = input(caret)
    return response


def integer_input(_range=None, msg='', caret='> '):
    while True:
        try:
            response = int(input(caret))
            if _range is not None:
                if response in _range:
                    return response
                else:
                    raise ValueError
            return response
        except ValueError as e:
            print(msg)
            continue


def yes_no_input(msg='', caret='> '):
    response = restricted_input(yes_no_responses, msg, caret)
    return response in yes_responses


def not_empty_input(msg, caret='> '):
    response = input(caret)
    while response.strip() == '':
        print(msg)
        response = input(caret)
    return response


def save_in_file(location, content):
    save_file = open(location, 'a')
    save_file.write(content)
    save_file.write("\n")
    save_file.close()
