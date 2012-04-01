"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains class and method definitions that can be used to query and
update the database of schools and courses.

CREATED
-------
By:   Aaron Greenberg
When: March 2012
"""

import MySQLdb
from tablify import tablify

# Public: Methods used for querying and updating a MySQL database. All methods
# are module methods and should be called on the Databaser module.
class Databaser(object):
    
    # Public: Initialize a Databaser.
    #
    # h      - The host machine that the MySQL database runs on.
    # u      - The user to connect to the MySQL database as.
    # schema - The MySQL database to connect to.
    # pw     - The password of the user.
    # p      - The port used for communicating with the MySQL database.
    def __init__(self, h='localhost', u='aaron', schema='TimeClash', pw='COMP311',
                 p=3306):
        
        # Create a connection to the MySQL database.
        self.db = MySQLdb.connect(host = h, user = u, db = schema, passwd = pw,
                                  port = p)
        
        # Create a cursor used for executing queries on the database.
        self.cursor = self.db.cursor()

    # Public: Grab a list of all the schools from the TimeClash database.
    #
    # Examples
    #
    #   self.get_schools()
    #   #=> ['Yale', 'Brown', 'UCLA']
    #
    # Returns a List of Strings representing all the schools in the database.
    def get_schools(self):
        database_command = """SELECT * FROM School;"""
        self.cursor.execute(database_command)
        return [value[1] for value in self.cursor.fetchall()]

    # Public: Grab a list of _all_ courses in the TimeClash database. Note that
    # this does not give courses organized or sorted by school.
    #
    # Examples
    #
    #   self.get_courses()
    #   #=> ['Software Design', 'The Entrepreneurial Initiative']
    #
    # Returns a List of Strings representing all the courses in the database.
    def get_courses(self):
        database_command = """SELECT * FROM Course;"""
        self.cursor.execute(database_command)
        return [value[2] for value in self.cursor.fetchall()]

    # Public: Grab a list of the courses in the TimeClash database that are offered
    # by a particular school.
    #
    # school_name - The name of school used to specify which courses to select.
    #
    # Returns a List of Strings representing all the courses that are offered by
    # the school in school_name.
    def get_coursenames_by_school(self, school_name):
        database_command = """SELECT CourseName FROM School, Course WHERE SchoolName = '%s' AND School.SchoolID = Course.SchoolID;""" % (school_name)
        self.cursor.execute(database_command)
        return [value[0] for value in self.cursor.fetchall()]

    def get_coursenums_by_course(self, course_name):
        database_command = """SELECT CourseNumber FROM Course WHERE CourseName = '%s';""" % (course_name)
        self.cursor.execute(database_command)
        return self.cursor.fetchall()[0]

    def get_coursetimes_by_course(self, course_name):
        database_command = """SELECT OfferTime1S, OfferTime1E, OfferTime2S, OfferTime2E, OfferTime3S, OfferTime3E, OfferTime4S, OfferTime4E FROM Course WHERE CourseName = '%s';""" % (course_name)
        self.cursor.execute(database_command)
        time_list = map(str, [time for time in self.cursor.fetchall()[0] ] )
        return time_list

    # Public: Insert a new school in the School relation of the MySQL database.
    #
    # school_name - The String name of the school to be added.
    #
    # Returns nothing.
    def insert_school(self, school_name):
        database_command = """INSERT INTO School(SchoolName) VALUES('%s')"""\
            % (school_name)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'Something went wrong!'

        # CHECK AUTOINCREMENT BUG #

    # Public: Update school_name information in the School relation of the MySQL
    # database.
    #
    # old_school - The original name of the school to be updated.
    # new_school - The new name to replace the old name in the update.
    #
    # Returns nothing.
    def update_school(self, old_school, new_school):
        pass

    # Public: Delete a school from the MySQL database.
    #
    # school - The name of the school to be deleted.
    #
    # Returns nothing.
    def delete_school(self, school):
        database_command = """DELETE FROM School WHERE SchoolName = '%s';"""\
            % (school)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'Something went wrong!'

        # CHECK AUTOINCREMENT BUG #

    # Internal: Output the suite of methods bound to the Databaser object. This
    # method is intended to be used to pass these function handles to the
    # front-end interface.
    #
    # Returns a Tuple of bound method handles.
    def render_functions(self):
        return (self.get_schools,
                self.get_coursenames_by_school,
                self.get_coursenums_by_course,
                self.insert_school,
                self.update_school,
                self.delete_school)

if __name__ == '__main__':
    db = Databaser()
    times = db.get_coursetimes_by_course('Software Systems')
    print times
    
