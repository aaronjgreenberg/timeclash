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
import timecheck

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

        # These two attributes are used to store the original school or course before
        # updating the MySQL database. By using these, it is possible to choose the
        # correct record to update.
        self.school_original = None
        self.course_original = None
        
        # These attributes are used to store the primary keys of a school and course
        # when they are to be updated. This allows the course or school to be
        # specified using a unique primary key, rather than the name.
        self.update_school_id = None
        self.update_course_id = None

        # This attribute stores the name of school when a user edits courses for
        # that school. It's necessary to store this attribute so that when the
        # database is updated, the correct school can be specified for the courses
        # to be updated. The specified school is lost when the new interface is
        # created, because all the widgets are destroyed.
        self.course_edit_school = None
        
        # Assign a suite of methods used for populating the interface with data from
        # the database.
        self.load_schools = functions[0]
        self.load_courses = functions[1]
        self.load_coursenum = functions[2]
        self.load_coursetimes = functions[3]
        self.insert_school = functions[4]
        self.insert_course = functions[5]
        self.update_school = functions[6]
        self.update_course = functions[7]
        self.delete_school = functions[8]
        self.delete_course = functions[9]
        self.get_school_id = functions[10]
        self.get_course_id = functions[11]
        
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
            self.tc_widglist['selected_box'].config(bg = '#DEDEDE')
            course = self.tc_widglist['coursebox'].get(ACTIVE)
            if course == '':
                return
            elif course in self.tc_widglist['selected_box'].get(0, END):
                return
            else:
                self.tc_widglist['selected_box'].insert(END, course)


        # Internal: Remove the selected course from the listbox of courses to
        # time check.
        #
        # Returns nothing.
        def remove_course():
            self.tc_widglist['selected_box'].config(bg = '#DEDEDE')
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
                                                      pady = 8,
                                                      command = self.check_conflicts)

    # Internal: Check the selected courses for time conflicts. Alerts the user
    # if there is a conflict.
    #
    # Returns nothing.
    def check_conflicts(self):
        courses = []
        course_names = self.tc_widglist['selected_box'].get(0, END)
        for i in range(len(course_names)):
            coursename = course_names[i]
            coursetimes = self.load_coursetimes(coursename)
            course = timecheck.Course(coursename, coursetimes)
            courses.append(course)
        if timecheck.timecheck(courses):
            self.tc_widglist['selected_box'].config(bg = '#FF0000')
        else:
            self.tc_widglist['selected_box'].config(bg = '#00FF00')
            


    # Public: Create the widgets that allow a user to edit the list of schools.
    #
    # Returns nothing.
    def edit_schools( self ):
        
        # Internal: Allows a user to add a name to the listbox. >>>Does not change
        # the database!<<<
        #
        # Returns nothing.
        def add_school():
            self.school_original = None
            school_entry = self.school_widglist['school_name_entry']
            school_entry.config(state = NORMAL)
            school_entry.delete(0, END)
            school_entry.insert(0, 'Name Of School')
        
        # Internal: Allows a user to edit the name of a school already in the
        # listbox. >>>Does not change the database!<<<
        #
        # Returns nothing.
        def edit_school_info():
            school_entry = self.school_widglist['school_name_entry']
            self.school_original = self.school_widglist['schoolbox'].get(ACTIVE)
            self.update_school_id = self.get_school_id(self.school_original)
            school_entry.config(state = NORMAL)
            school_entry.delete(0, END)
            school_entry.insert(0, self.school_original)

        # Internal: If the school to be added/edited exists in the database, this
        # method updates the MySQL database. If not, the method adds the school to
        # the database.
        #
        # Returns nothing.
        def save_school_info():
            school_entry = self.school_widglist['school_name_entry']
            entered_text = school = school_entry.get()
            if entered_text == 'Name Of School':
                return
            if entered_text in self.school_widglist['schoolbox'].get(0, END):
                return
            school_entry.config(state = "readonly")
            if self.school_original != None:
                self.update_school(self.update_school_id, school)
                self.school_original = None
            else:
                self.insert_school(school)
            populate_schools()

        # Internal: Remove the course selected in the listbox from the MySQL
        # database.
        #
        # Returns nothing.
        def remove_school():
            school = self.school_widglist['schoolbox'].get(ACTIVE)
            self.delete_school(school)
            populate_schools()

        # Internal: Adds the courses from the MySQL database to the listbox in the
        # Python interface.
        #
        # Returns nothing.
        def populate_schools():
            listbox = self.school_widglist['schoolbox']
            listbox.delete(0, END)
            for item in self.load_schools():
                listbox.insert(END, item)
        
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

        populate_schools()

        self.school_widglist[ 'edcourse_button' ] = self.bu( 
            font = self.font,
            width = 20,
            text = 'Edit Courses\nfor this\nSchool',
            wraplength = 0.2,
            height = 10,
            command = self.edit_courses)

        self.endgr()

        self.school_widglist[ 'schooladd_grid' ] = self.gr( cols = 2 )

        self.school_widglist[ 'schooladd_button' ] = self.bu( font = self.font,
                                                              text = 'Add A School',
                                                              width = 36,
                                                              command = add_school)

        self.school_widglist[ 'schooled_button' ] = self.bu( 
            font = self.font,
            text = 'Edit School Information',
            width = 37,
            command = edit_school_info)

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
                                                         width = 74,
                                                         command = save_school_info)
                                     
        self.school_widglist[ 'schooldel_button' ] = self.bu( 
            font = self.font,
            width = 74,
            text = 'Delete Selected School',
            bg = '#FF0000',
            command = remove_school)

    # Public: Creates the widgets that allow a user to edit the list of courses
    # for each school.
    #
    # Returns nothing.
    def edit_courses(self):
        
        # Internal: Allows a user to add a course to the listbox, to eventually be
        # added to the database. This method should set all the forms in the
        # interface to editable versions, and should clear them. >>> THIS METHOD
        # DOES NOT CHANGE THE MySQL DATABASE! <<<
        #
        # Returns nothing
        def add_course():
            # Should set the forms to NORMAL, editable versions, and clear them.
            self.course_original = None
            widglist = self.course_widglist # ALIAS
            courseno_entry = widglist['courseno_entry'] # ALIAS
            coursename_entry = widglist['coursename_entry'] # ALIAS
            courseno_entry.config(state = NORMAL)
            coursename_entry.config(state = NORMAL)
            courseno_entry.delete(0, END)
            coursename_entry.delete(0, END)
            courseno_entry.insert(0, 'Course Number')
            coursename_entry.insert(0, 'Name Of Course')
            for i in range(1, 5):
                s = str(i)
                widglist['day_box_' + s].delete(0, END)
                widglist['day_box_' + s].insert(0, '--')
                widglist['starthr_' + s].delete(0, END)
                widglist['starthr_' + s].insert(0, '--')
                widglist['startmin_' + s].delete(0, END)
                widglist['startmin_' + s].insert(0, '--')
                widglist['endhr_' + s].delete(0, END)
                widglist['endhr_' + s].insert(0, '--')
                widglist['endmin_' + s].delete(0, END)
                widglist['endmin_' + s].insert(0, '--')

            
        # Internal: Allows a user to edit a course's information, to eventually be
        # added to the database. This method should set all the forms to editable
        # versions and populate them with the information from the course selected
        # from the course ListBox. >>> THIS METHOD DOES NOT CHANGE THE MySQL
        # DATABASE! <<<
        #
        # Returns nothing.
        def edit_course_info():
            widglist = self.course_widglist # ALIAS
            self.course_original = widglist['coursebox'].get(ACTIVE)
            self.update_course_id = self.get_course_id(self.course_original)
            courseno_entry = widglist['courseno_entry'] # ALIAS
            coursename_entry = widglist['coursename_entry'] # ALIAS
            courseno_entry.config(state = NORMAL)
            coursename_entry.config(state = NORMAL)
            courseno_entry.delete(0, END)
            coursename_entry.delete(0, END)
            courseno_entry.insert(0, self.load_coursenum(self.course_original) )
            coursename_entry.insert(0, self.course_original)
            times = self.load_coursetimes(self.course_original)
            for i in range(1, 5):
                s = str(i)
                # times[i] --> Tuple containing the day and times of offering 'i'.
                #              (We use i - 1 b/c the tuple is zero-indexed, but the
                #               range 1, 2, 3, 4.)
                # times[i][0] --> String day of offering 'i'.
                # times[i][1] --> String start hour of offering 'i'.
                # times[i][2] --> String start minute of offering 'i'.
                # times[i][3] --> String end hour of offering 'i'.
                # times[i][4] --> String end minute of offering 'i'.
                widglist['day_box_' + s].delete(0, END)
                widglist['day_box_' + s].insert(0, times[i - 1][0])
                widglist['starthr_' + s].delete(0, END)
                widglist['starthr_' + s].insert(0, times[i - 1][1])
                widglist['startmin_' + s].delete(0, END)
                widglist['startmin_' + s].insert(0, times[i - 1][2])
                widglist['endhr_' + s].delete(0, END)
                widglist['endhr_' + s].insert(0, times[i - 1][3])
                widglist['endmin_' + s].delete(0, END)
                widglist['endmin_' + s].insert(0, times[i - 1][4])


        # Internal: Commits the information in the entry forms to the Course relation
        # of the MySQL database. If the information is for a new course, a course
        # will be inserted. If the info is updated information, the corresponding
        # course will be updated.
        #
        # Returns nothing.
        def save_course_info():
            courseno_entry = self.course_widglist['courseno_entry']
            coursename_entry = self.course_widglist['coursename_entry']
            courseno_entry.config(state = "readonly")
            coursename_entry.config(state = "readonly")
            course_name = coursename_entry.get()
            course_number = courseno_entry.get()
            offer_times = render_times()
            school_id = self.get_school_id(self.course_edit_school)
            if course_name == 'Name Of Course':
                return
            if course_number == 'Course Number':
                return
            if self.course_original != None:
                self.update_course(self.update_course_id, school_id, course_name,
                                   course_number, *offer_times)
                self.course_original = None
            else:
                self.insert_course(school_id, course_name, course_number,
                                   *offer_times)
            populate_courses(self.course_edit_school)
            
            
        # Internal: Deletes the course selected from the listbox from the MySQL
        # database.
        #
        # Returns nothing.
        def remove_course():
            del_course = self.course_widglist['coursebox'].get(ACTIVE)
            self.delete_course(del_course)
            populate_course(self.course_edit_school)

        
        # Internal: Gets the courses for the specified school and adds them to the
        # course listbox.
        #
        # school_name - Specifies which school's courses should be queried.
        #
        # Returns nothing.
        def populate_courses(school_name):
            self.course_widglist['coursebox'].delete(0, END)
            for school in self.load_courses(school_name):
                self.course_widglist['coursebox'].insert(END, school)

        # Internal: Put all the dates/times in the spinboxes in the correct format
        # for entry into the MySQL database.
        #
        # Returns a List of start and end date/times, formatted for MySQL insertion.
        def render_times():
            widglist = self.course_widglist
            day_converter = {'--':'00', 'M':'01', 'T':'02', 'W':'03',
                             'Th':'04', 'F':'05', 'S':'06', 'Su':'07'}
            time_list = []
            for i in range(1, 5):
                s = str(i)
                day = day_converter[widglist['day_box_' + s].get()]
                date = "'1000-01-%s" % (day)
                starthr = widglist['starthr_' + s].get()
                startmin = widglist['startmin_' + s].get()
                endhr = widglist['endhr_' + s].get()
                endmin = widglist['endmin_' + s].get()
                if day == '00' and starthr == '--' and startmin == '--' and\
                        endhr == '--' and endmin == '--':
                    time_list.append('NULL')
                    time_list.append('NULL')
                elif day == '00' or starthr == '--' or startmin == '--' or\
                        endhr == '--' or endmin == '--':
                    print "MISSING TIME OR DATE ENTRY"
                    return
                else:
                    if len(starthr) == 1:
                        starthr = '0' + starthr
                    if len(startmin) == 1:
                            startmin = '0' + startmin
                    if len(endhr) == 1:
                                endhr = '0' + endhr
                    if len(endmin) == 1:
                        endmin = '0' + endmin
                    start_time = "%s:%s:00'" % (starthr, startmin)
                    end_time = "%s:%s:00'" % (endhr, endmin)
                    time_list.append(' '.join( (date, start_time) ) )
                    time_list.append(' '.join( (date, end_time) ) )
            return time_list
        
        self.course_edit_school = self.school_widglist['schoolbox'].get(ACTIVE)

        self.edit_button.config( state = NORMAL, relief = RAISED )

        self.kill_widgets( self.school_widglist )
        self.school_widglist = {}

        self.course_widglist[ 'school_label' ] = self.la( 
            font = ( 'fixedsys', 18 ),
            text = "Courses For\n%s" % (self.course_edit_school) )

        self.course_widglist[ 'coursebox' ] = self.lb( font = self.font,
                                                       width = 74,
                                                       height = 15,
                                                       bg = '#DEDEDE' )

        populate_courses(self.course_edit_school)

        self.course_widglist[ 'edcourse_button_gr' ] = self.gr( cols = 2 )

        self.course_widglist[ 'updatecourse_button' ] = self.bu( 
            font = self.font,
            text = 'Update Course Information',
            width = 36,
            command = edit_course_info)

        self.course_widglist[ 'addcourse_button' ] = self.bu( 
            font = self.font,
            text = 'Add A Course',
            width = 37,
            command = add_course)

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
            width = 74,
            command = save_course_info)

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
