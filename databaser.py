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
    def get_courses_by_school(self, school_name):
        database_command = """SELECT CourseName FROM School, Course WHERE SchoolName = '%s' AND School.SchoolID = Course.SchoolID;""" % (school_name)
        self.cursor.execute(database_command)
        return [value[0] for value in self.cursor.fetchall()]

    # Internal: Output the suite of methods bound to the Databaser object. This
    # method is intended to be used to pass these function handles to the
    # front-end interface.
    #
    # Returns a Tuple of bound method handles.
    def render_functions(self):
        return self.get_schools, self.get_courses_by_school

if __name__ == '__main__':
    db = Databaser()
    print db.get_schools()
    
