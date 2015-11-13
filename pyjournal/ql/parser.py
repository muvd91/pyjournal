commands = ['get', 'write', 'edit', 'delete', 'display', 'use', 'categories']
no_arg_cmds = ['write', 'categories', 'write on file',
               'files', 'delete file', 'rename file',
               'new file', 'open file']


def get_query_template(query):
    template = dict()

    if query in no_arg_cmds:
        template['verb'] = query
        return template

    tokens = query.split(' ')
    previous = None
    for i in range(len(tokens)):
        token = tokens[i]
        template = validator(previous, token, template)
        previous = tokens[i]
    return template


def validator(previous, token, template):

    if previous is None:
        if token not in commands:
            raise ParseValidationError('{} is not a command'.format(token))
        template['verb'] = token

    elif previous == 'get':
        if token != 'all' and token != 'entries':
            template['category'] = token

    elif previous == 'edit':
        template['_id'] = token

    elif previous == 'delete':
        template['_id'] = token

    elif previous == 'display':
        template['display'] = token

    elif previous == 'use':
        template['use'] = token

    return template


class ParseValidationError(Exception):
    pass
