#!/usr/bin/python3
from interactive import interactive
import sys
import persistence.db

if len(sys.argv) > 1:
    args = ''.join(list(filter(lambda e: e[0] == '-', sys.argv)))
    if "v" in args or "--view" in args:
        interactive.exec_query('get all')

else:
    interactive.interactive()
    persistence.db.close_connection()
