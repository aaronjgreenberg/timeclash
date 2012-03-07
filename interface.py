"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains the code that creates the user-interface used to access, query,
and update the database that contains the schools and courses.

CREATED
-------
By: Aaron Greenberg
When: March 2012
"""

from Gui import *

# Public: Methods and classes used to create a graphical user Interface to access,
# update, and query a TimeClash database of courses and schools. All methods are
# module methods and should be called on the Interface module.
#
# Examples
#
#   interface = Interface()
#   # => <__main__.Interface instance at 0x00000000>
class Interface( Gui ):

    # Public: Initialize an Interface.
    def __init__( self ):
        Gui.__init__( self )
        self.title( 'TimeClash' )
    
    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
