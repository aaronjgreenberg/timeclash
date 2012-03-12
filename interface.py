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

        self.tc_widglist = []
        self.edit_widglist = []

        self.gr( cols = 2 )
        self.tc_button = self.bu( text = 'Time Check',
                                  font = ( 'fixedsys', 12 ),
                                  width = 36,
                                  command = self.timecheck,
                                  state = DISABLED )

        self.edit_button = self.bu( text = 'Edit Courses or Schools',
                                    font = ( 'fixedsys', 12 ),
                                    width = 37,
                                    command = self.edit )
                                      
        self.endgr()

        self.timecheck()

    # Public: Create the widgets that allow a user to choose schools and courses
    # to see if they conflict.
    #
    # Returns nothing.
    def timecheck( self ):

        self.kill_widgets( self.edit_widglist )
        self.edit_widglist = []

        self.tc_button.config( state = DISABLED, relief = SUNKEN )
        self.edit_button.config( state = NORMAL, relief = RAISED )

        tc_grid = self.gr( cols = 2, pady = 8 )
        
        schoolbox = self.lb( font = ( 'fixedsys', 12 ),
                             width = 37 )
        coursebox = self.lb( font = ( 'fixedsys', 12 ),
                             width = 37 )
               
        self.endgr()

        select_button = self.bu( text = 'Add Course',
                                 font = ( 'fixedsys', 14 ),
                                 width = 74 )

        selected_box = self.lb( font = ( 'fixedsys', 14 ),
                                width = 74,
                                height = 5,
                                bg = '#DEDEDE',
                                pady = 8 )

        delete_button = self.bu( font = ( 'fixedsys', 14 ),
                                 width = 74,
                                 text = 'Remove Course' )

        check_button = self.bu( font = ( 'fixedsys', 18 ),
                                width = 18,
                                text = 'Check Time',
                                pady = 8 )

        self.tc_widglist.extend( [ tc_grid,
                                   schoolbox,
                                   coursebox,
                                   select_button,
                                   selected_box,
                                   delete_button,
                                   check_button ] )

    # Public: Create the widgets that allow a user to edit the school and course
    # options.
    #
    # Returns nothing.
    def edit( self ):
        
        self.kill_widgets( self.tc_widglist )
        self.tc_widglist = []

        self.tc_button.config( state = NORMAL, relief = RAISED )
        self.edit_button.config( state = DISABLED, relief = SUNKEN )

    # Public: Destroys (removes from application) all the widgets passed in the
    # List.
    #
    # widget_list - A List of widgets to be destroyed.
    #
    # Returns nothing.
    def kill_widgets( self, widget_list ):
        for widget in widget_list:
            widget.destroy()

    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
