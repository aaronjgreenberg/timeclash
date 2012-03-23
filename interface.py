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
        self.school_widglist = []
        self.course_widglist = []

        self.gr( cols = 2 )
        self.tc_button = self.bu( text = 'Time Check',
                                  font = ( 'fixedsys', 12 ),
                                  width = 36,
                                  command = self.timecheck,
                                  state = DISABLED )

        self.edit_button = self.bu( text = 'Edit Courses or Schools',
                                    font = ( 'fixedsys', 12 ),
                                    width = 37,
                                    command = self.edit_schools )
                                      
        self.endgr()

        self.timecheck()

    # Public: Create the widgets that allow a user to choose schools and courses
    # to see if they conflict.
    #
    # Returns nothing.
    def timecheck( self ):

        self.kill_widgets( self.school_widglist, self.course_widglist )
        self.school_widglist = []
        self.course_widglist = []

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

    # Public: Create the widgets that allow a user to edit the list of schools.
    #
    # Returns nothing.
    def edit_schools( self ):
        
        self.kill_widgets( self.tc_widglist, self.course_widglist )
        self.tc_widglist = []
        self.course_widglist = []

        self.tc_button.config( state = NORMAL, relief = RAISED )
        self.edit_button.config( state = DISABLED, relief = SUNKEN )

        edschool_grid = self.gr( cols = 2 )

        schoolbox = self.lb( font = ( 'fixedsys', 12 ),
                           width = 54,
                           height = 10,
                           bg = '#DEDEDE' )

        edcourse_button = self.bu( font = ( 'fixedsys', 14 ),
                                   width = 20,
                                   text = 'Edit Courses\nfor this\nSchool',
                                   wraplength = 0.2,
                                   height = 10,
                                   command = self.edit_courses )

        self.endgr()

        schooladd_grid = self.gr( cols = 2 )

        schoolname = StringVar()

        school_name_entry = self.en( font = ( 'fixedsys', 14 ),
                                     textvariable = schoolname,
                                     padx = 4,
                                     width = 50 )

        schoolname.set( 'Name Of School' )

        schooladd_button = self.bu( font = ( 'fixedsys', 14 ),
                                    text = 'Add School',
                                    width = 22,
                                    padx = 4,
                                    pady = 8 )

        self.endgr()

        updateinfo_grid = self.gr( cols = 2 )

        editname_button = self.bu( font = ( 'fixedsys', 12 ),
                                   text = 'Edit School Name',
                                   width = 36 )

        updatename_button = self.bu( font = ( 'fixedsys', 12 ),
                                     text = 'Update Information',
                                     width = 37 )

        self.endgr()
                                     
        schooldel_button = self.bu( font = ( 'fixedsys', 14 ),
                                    width = 74,
                                    text = 'Delete Selected School',
                                    pady = 8,
                                    bg = '#FF0000' )

        self.school_widglist.extend( [ edschool_grid,
                                       schoolbox,
                                       edcourse_button,
                                       schooladd_grid,
                                       school_name_entry,
                                       schooladd_button,
                                       updateinfo_grid,
                                       editname_button,
                                       updatename_button,
                                       schooldel_button, ] )

    # Public: Creates the widgets that allow a user to edit the list of courses
    # for each school.
    #
    # Returns nothing.
    def edit_courses( self ):

        self.edit_button.config( state = NORMAL, relief = RAISED )

        self.kill_widgets( self.school_widglist )
        self.school_widglist = []

        school_label = self.la( font = ( 'fixedsys', 18 ),
                                text = "Courses For 'School Name Here'" )

        coursebox = self.lb( font = ( 'fixedsys', 14 ),
                           width = 74,
                           height = 15,
                           bg = '#DEDEDE' )

        edschool_button_gr = self.gr( cols = 2 )

        updateschool_button = self.bu( font = ( 'fixedsys', 12 ),
                                       text = 'Update Course Information',
                                       width = 36 )

        addschool_button = self.bu( font = ( 'fixedsys', 12 ),
                                    text = 'Add A Course',
                                    width = 37 )

        self.endgr()

        self.course_widglist.extend( [ school_label,
                                       coursebox,
                                       edschool_button_gr,
                                       updateschool_button,
                                       addschool_button ] )

    # Public: Destroys (removes from application) all the widgets passed in the
    # List.
    #
    # widget_list - A List of widgets to be destroyed.
    #
    # Returns nothing.
    def kill_widgets( self, widget_list, second_list = [] ):
        kill_list = widget_list + second_list
        for widget in kill_list:
            widget.destroy()

    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
