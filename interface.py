"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains the code that creates the user-interface used to access, query,
and update the database that contains the schools and courses.

TODO
----
* Make it so the user can dynamically add or remove the number of courses they
  are taking.

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
                                  font = ( 'fixedsys', 12 ),
                                  width = 36,
                                  command = self.timecheck,
                                  state = DISABLED )

        self.edit_button = self.bu( text = 'Edit Courses or Schools',
                                    font = ( 'fixedsys', 12 ),
                                    width = 37 )
                                  
        self.endgr()

        self.tc_widglist = []
        self.add_widglist = []
        self.timecheck()

    # Public: Create the widgets that allow a user to choose schools and courses
    # to see if they conflict.
    #
    # Returns nothing.
    def timecheck( self ):
        self.tc_button.config( state = DISABLED )
        self.edit_button.config( state = NORMAL )

        main_label = self.la( text = 'Please select your courses:',
                              font = ( 'fixedsys', 18, 'bold' ),
                              pady = 10 )


        self.gr( cols = 2 )
        
        schoolbox = self.lb( font = ( 'fixedsys', 12 ),
                             width = 37 )
        coursebox = self.lb( font = ( 'fixedsys', 12 ),
                             width = 37 )
               
        self.endgr()

        course_select = self.bu( text = 'Add course',
                                 font = ( 'fixedsys', 14 ),
                                 width = 74,
                                 pady = 5 )

        label_selected = self.la( text = 'Selected courses:',
                                  font = ( 'fixedsys', 17 ),
                                  pady = 8 )

        selected_box = self.lb( font = ( 'fixedsys', 12 ),
                                width = 74,
                                height = 5,
                                bg = '#DEDEDE' )
                            

    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
