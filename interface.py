"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains the code that creates the user-interface used to access, query,
and update the database that contains the schools and courses.

TODO
----
* Make it so the user can dynamically change the number of offering times for a
  certain course.

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
    def __init__( self, functions ):
        Gui.__init__( self )
        self.title( 'TimeClash' )
        self.resizable( 0, 0 )
        self.font = ( 'fixedsys', 12 )

        self.tc_widglist = {}
        self.school_widglist = {}
        self.course_widglist = {}
        
        # Assign a suite of methods used for populating the interface with data from
        # the database.
        self.load_schools = functions[0]
        self.load_courses = functions[1]
        
        self.gr( cols = 2 )
        self.tc_button = self.bu( text = 'Time Check',
                                  font = self.font,
                                  width = 36,
                                  command = self.timecheck,
                                  state = DISABLED )

        self.edit_button = self.bu( text = 'Edit Courses or Schools',
                                    font = self.font,
                                    width = 37,
                                    command = self.edit_schools )
                                      
        self.endgr()

        self.timecheck()

    # Public: Create the widgets that allow a user to choose schools and courses
    # to see if they conflict.
    #
    # Returns nothing.
    def timecheck( self ):

        # Internal: Populate the Courses listbox with a list of courses
        # corresponding to the school selected in the Schools listbox.
        #
        # school - The selected school.
        #
        # Returns a list of courses from the database.
        def populate_coursebox(school):
            if self.tc_widglist['coursebox'].get(0, END) != []:
                self.tc_widglist['coursebox'].delete(0, END)
            school = self.tc_widglist['schoolbox'].get(ACTIVE)
            for item in self.load_courses(school):
                self.tc_widglist['coursebox'].insert(END, item)

        # Internal: Add the selected course from the coursebox to the listbox
        # of selected courses for checking times.
        #
        # Returns nothing.
        def select_course():
            course = self.tc_widglist['coursebox'].get(ACTIVE)
            if course in self.tc_widglist['selected_box'].get(0, END):
                return
            else:
                self.tc_widglist['selected_box'].insert(END, course)

        # Internal: Remove the selected course from the listbox of courses to
        # time check.
        #
        # Returns nothing.
        def remove_course():
            self.tc_widglist['selected_box'].delete(ACTIVE)

        self.kill_widgets( self.school_widglist, self.course_widglist )
        self.school_widglist = {}
        self.course_widglist = {}

        self.tc_button.config( state = DISABLED, relief = SUNKEN )
        self.edit_button.config( state = NORMAL, relief = RAISED )

        self.tc_widglist[ 'tc_grid' ] = self.gr( cols = 2, pady = 8 )
        
        self.tc_widglist[ 'schoolbox' ] = self.lb( font = self.font,
                                                   width = 37 )

        for item in self.load_schools():
            self.tc_widglist['schoolbox'].insert(END, item)
        
        # Create event bindings so that the coursebox will update for the selected
        # schools when the user double-clicks or hits "Return."
        self.tc_widglist['schoolbox'].bind("<Double-Button-1>", populate_coursebox)

        self.tc_widglist['schoolbox'].bind("<Return>", populate_coursebox)

        self.tc_widglist[ 'coursebox' ] = self.lb( font = self.font,
                                                   width = 37 )
               
        self.endgr()

        self.tc_widglist[ 'select_button' ] = self.bu( text = 'Add Course',
                                                       font = self.font,
                                                       width = 74,
                                                       command = select_course)

        self.tc_widglist[ 'selected_box' ] = self.lb( font = self.font,
                                                      width = 74,
                                                      height = 5,
                                                      bg = '#DEDEDE',
                                                      pady = 8 )

        self.tc_widglist[ 'delete_button' ] = self.bu( font = self.font,
                                                       width = 74,
                                                       text = 'Remove Course',
                                                       command = remove_course)

        self.tc_widglist[ 'check_button' ] = self.bu( font = ( 'fixedsys', 18 ),
                                                      width = 18,
                                                      text = 'Check Time',
                                                      pady = 8 )

    # Public: Create the widgets that allow a user to edit the list of schools.
    #
    # Returns nothing.
    def edit_schools( self ):
        
        self.kill_widgets( self.tc_widglist, self.course_widglist )
        self.tc_widglist = {}
        self.course_widglist = {}

        self.tc_button.config( state = NORMAL, relief = RAISED )
        self.edit_button.config( state = DISABLED, relief = SUNKEN )

        self.school_widglist[ 'edschool_grid' ] = self.gr( cols = 2 )

        self.school_widglist[ 'schoolbox' ] = self.lb( font = self.font,
                                                       width = 54,
                                                       height = 10,
                                                       bg = '#DEDEDE' )

        self.school_widglist[ 'edcourse_button' ] = self.bu( 
            font = self.font,
            width = 20,
            text = 'Edit Courses\nfor this\nSchool',
            wraplength = 0.2,
            height = 10,
            command = self.edit_courses )

        self.endgr()

        self.school_widglist[ 'schooladd_grid' ] = self.gr( cols = 2 )

        self.school_widglist[ 'schooladd_button' ] = self.bu( font = self.font,
                                                              text = 'Add School',
                                                              width = 36 )

        self.school_widglist[ 'schooled_button' ] = self.bu( 
            font = self.font,
            text = 'Edit School Information',
            width = 37 )

        self.endgr()

        schoolname = StringVar()

        self.school_widglist[ 'school_name_entry' ] = self.en( 
            font = self.font,
            textvariable = schoolname,
            padx = 10,
            pady = 8,
            width = 50 )

        schoolname.set( 'Name Of School' )

        self.school_widglist[ 'save_button' ] = self.bu( font = self.font,
                                                         text = 'Save Information',
                                                         pady = 8,
                                                         width = 74 )
                                     
        self.school_widglist[ 'schooldel_button' ] = self.bu( 
            font = self.font,
            width = 74,
            text = 'Delete Selected School',
            bg = '#FF0000' )

    # Public: Creates the widgets that allow a user to edit the list of courses
    # for each school.
    #
    # Returns nothing.
    def edit_courses( self ):

        self.edit_button.config( state = NORMAL, relief = RAISED )

        self.kill_widgets( self.school_widglist )
        self.school_widglist = {}

        self.course_widglist[ 'school_label' ] = self.la( 
            font = ( 'fixedsys', 18 ),
            text = "Courses For 'School Name Here'" )

        self.course_widglist[ 'coursebox' ] = self.lb( font = self.font,
                                                       width = 74,
                                                       height = 15,
                                                       bg = '#DEDEDE' )

        self.course_widglist[ 'edcourse_button_gr' ] = self.gr( cols = 2 )

        self.course_widglist[ 'updatecourse_button' ] = self.bu( 
            font = self.font,
            text = 'Update Course Information',
            width = 36 )

        self.course_widglist[ 'addcourse_button' ] = self.bu( 
            font = self.font,
            text = 'Add A Course',
            width = 37 )

        self.endgr()

        self.course_widglist[ 'course_entry_grid' ] = self.gr ( cols = 2 )
        
        course_number = StringVar()
        course_name = StringVar()

        self.course_widglist[ 'courseno_entry' ] = self.en( 
            font = self.font,
            textvariable = course_number,
            padx = 5,
            pady = 8,
            width = 15 )

        self.course_widglist[ 'coursename_entry' ] = self.en( 
            font = self.font,
            textvariable = course_name,
            padx = 5,
            pady = 8,
            width = 57 )

        course_number.set( 'Course Number' )
        course_name.set( 'Name Of Course' )

        self.endgr()

        self.course_widglist[ 'offerlabel_grid' ] = self.gr( cols = 4 )

        self.course_widglist[ 'placehold' ] = self.fr()
        self.endfr()

        self.course_widglist[ 'day_label' ] = self.la( font = self.font,
                                                       text = 'Day' )

        self.course_widglist[ 'start_label' ] = self.la( font = self.font,
                                                         text = 'Start Time' )

        self.course_widglist[ 'end_label' ] = self.la( font = self.font,
                                                       text = 'End Time' )

        for i in xrange( 1, 5 ):
            
            s = str(i)

            self.course_widglist[ 'time_label_' + s ] = self.la(
                font = self.font,
                text = 'Offer Time %s' % (s),
                pady = 3,
                padx = 5 )

            self.course_widglist[ 'day_box_' + s ] = self.sp( 
                values = ( '--', 'M', 'T', 'W', 'Th', 'F', 'S', 'Su' ),
                width = 4 )
        
            self.course_widglist[ 'start_timegrid_' + s ] = self.gr( cols = 2, 
                                                                     padx = 145 )
        
            self.course_widglist[ 'starthr_' + s ] = self.sp( 
                values = ['--'] + range( 24 ),
                width = 4 )

            self.course_widglist[ 'startmin_' + s ] = self.sp( 
                values = ['--'] + range( 0, 60, 5 ),
                width = 4 )

            self.endgr()

            self.course_widglist[ 'end_timegrid_' + s ] = self.gr( cols = 2 )

            self.course_widglist[ 'endhr_' + s ] = self.sp( 
                values = ['--'] + range( 24 ),
                width = 4 )

            self.course_widglist[ 'endmin_' + s ] = self.sp( 
                values = ['--'] + range( 0, 60, 5 ),
                width = 4 )

            self.endgr()

        self.endgr()

        self.course_widglist[ 'course_save_button' ] = self.bu( 
            font = self.font,
            text = 'Save Information',
            pady = 8,
            width = 74 )

        self.course_widglist[ 'course_remove_button' ] = self.bu( 
            font = self.font,
            text = 'Delete This Course',
            bg = '#FF0000',
            width = 74 )

    # Public: Destroys (removes from application) all the widgets passed in the
    # List.
    #
    # widget_list - A List of widgets to be destroyed.
    #
    # Returns nothing.
    def kill_widgets( self, widget_dict, second_dict = {} ):
        kill_dict = dict( widget_dict.items() + second_dict.items() )
        for w_key, w_value in kill_dict.iteritems():
            w_value.destroy()
    
    # Public: Run the event loop, wait for user to give input, return output.
    #
    # Returns nothing.
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    interface = Interface()
    interface.run()
