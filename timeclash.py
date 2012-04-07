"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains the main code of the program. It puts together the front-end user
interface and the back-end, which interfaces with the MySQL database.

TODO
----
* Make it so the user can specify the user and password from the command line.

CREATED
-------
By:   Aaron Greenberg
When: March 2012
"""

from databaser import Databaser
from interface import Interface

backend = Databaser()
methods = backend.render_functions()
frontend = Interface(methods)
frontend.run()
