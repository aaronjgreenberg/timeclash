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
        self.resizable( 0, 0 )
        self.gr( cols = 2 )
        self.tc_button = self.bu( text = 'Time Check',
                                  font = ( 'fixedsys', 14 ),
                                  width = 36,
                                  command = self.timecheck,
                                  state = DISABLED
                                  )

        self.edit_button = self.bu( text = 'Edit Courses or Schools',
                                   font = ( 'fixedsys', 14 ),
                                   width = 36,
                                   )
        self.endgr()
        self.tc_bool = False
        self.add_bool = False
        self.timecheck()

    # Public: Create the widgets that allow a user to choose schools and courses
    # to see if they conflict.
    #
    # Returns nothing.
    def timecheck( self ):
        self.edit_button.config( state = NORMAL )
        tc_widglist = []
        tc_widglist.append( self.la( text = 'Please select your courses:',
                                     font = ( 'fixedsys', 18, 'bold' ),
                                     pady = 10 ) )

        self.gr( cols = 2, background = 'black' )
        tc_widglist.extend( [ 
                self.mb( text = 'School',
                         font = ( 'fixedsys', 14 ),
                         background = 'white',
                         width = 35,
                         padx = 2,
                         pady = 2,
                         activebackground = '#737373' ),
                self.mb( text = 'Course',
                         font = ( 'fixedsys', 14 ),
                         background = 'white',
                         width = 35,
                         padx = 2,
                         pady = 2,
                         activebackground = '#737373' ),
                self.mb( text = 'School',
                         font = ( 'fixedsys', 14 ),
                         background = 'white',
                         width = 35,
                         padx = 2,
                         pady = 2,
                         activebackground = '#737373' ),
                self.mb( text = 'Course',
                         font = ( 'fixedsys', 14 ),
                         background = 'white',
                         width = 35,
                         padx = 2,
                         pady = 2,
                         activebackground = '#737373' )
                ] )
                       
        self.endgr()

    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
