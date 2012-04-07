"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains the main code of the program. It puts together the front-end user
interface and the back-end, which interfaces with the MySQL database.

CREATED
-------
By:   Aaron Greenberg
When: March 2012
"""

from databaser import Databaser
from interface import Interface
import sys

def main(args):
    if len(args) == 3:
        if args[1].startswith('--user=') and args[2].startswith('--pw='):
            username = args[1].split('=')[1]
            password = args[2].split('=')[1]
            backend = Databaser(u = username, pw = password)
        elif args[1].startswith('--pw=') and args[2].startswith('--user='):
            username = args[2].split('=')[1]
            password = args[1].split('=')[1]
            backend = Databaser(u = username, pw = password)
    elif len(args) == 2:
        raise TypeError, 'You passed timeclash.py 1 argument, but it requires 0 or 2.'
    else:
        backend = Databaser()
    methods = backend.render_functions()
    frontend = Interface(methods)
    frontend.run()

if __name__ == '__main__':
    main(sys.argv)
