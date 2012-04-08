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


    # Public: Get the course number for a certain course in the database.
    #
    # course_name - The name of the course for which to grab the course number.
    #
    # Returns a String of the course number for the selected course.
    def get_coursenum_by_course(self, course_name):
        database_command = """SELECT CourseNumber FROM Course WHERE CourseName = '%s';""" % (course_name)
        self.cursor.execute(database_command)
        return self.cursor.fetchall()[0]

    # Public: Grab a set of offer times for a specific course from the MySQL
    # database.
    #
    # course_name - The name of the course for which to retrieve the times.
    #
    # Returns a Tuple of Lists of offering times/dates formatted for insertion into
    # the Spinboxes of the interface.
    def get_coursetimes_by_course(self, course_name):
        database_command = """SELECT OfferTime1S, OfferTime1E, OfferTime2S, OfferTime2E, OfferTime3S, OfferTime3E, OfferTime4S, OfferTime4E FROM Course WHERE CourseName = '%s';""" % (course_name)
        self.cursor.execute(database_command)
        sql_time_dump = map(str, [time for time in self.cursor.fetchall()[0] ] )
        time_list = []
        # The join in the following line puts the time dump in the format
        # 'DD HH:MM:SS HH:MM:SS', which represents day, start time, and end time.
        for i in range(0, 8, 2):
            if sql_time_dump[i] == 'None' and sql_time_dump[i + 1] == 'None':
                # If both are None, there's no offering time there.
                time_list.append('--')
            elif sql_time_dump[i] == 'None' or sql_time_dump[i] == 'None':
                # If only one of the two is None, either the class never ends,
                # or the user forgot to input a time or date entry.
                print 'MISSING START OR END TIME'
                return None
            else:
                time_list.append(
                    ' '.join( (sql_time_dump[i][-11:], sql_time_dump[i + 1][-8:]) ) )
                
        day_converter = {'00':'--', '01':'M', '02':'T', '03':'W',
                         '04':'Th', '05':'F', '06':'S', '07':'Su'}
        # Each list in the times Tuple contains 5 values: day, start hr, start min
        # end hr, end min, formatted for insertion into the interface Spinboxes.
        times = ( [], [], [], [] )
        for i in range(4):
            if time_list[i] == '--':
                times[i].extend( ['--', '--', '--', '--', '--'] )
            else:
                offer_times = time_list[i].split(' ') 
                # offer_times format is ['DD', 'HH:MM:SS', 'HH:MM:SS']
                times[i].append(day_converter[offer_times[0]]) # Add day to list
                times[i].extend(offer_times[1].split(':')[0:2]) # Add start hr, min
                times[i].extend(offer_times[2].split(':')[0:2]) # Add end hr, min
        return times
            

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
            print 'SOMETHING WENT WRONG!'


    # Public: Insert a new course into the Course relation of the MySQL database.
    #
    # school_id   - The SchoolID attribute in the MySQL database to which the course
    #               belongs.
    # course_name - The name of the course being updated.
    # course_no   - The course number of the course being offered.
    # offertimeXs - The starting time of the Xth offering of the course.
    # offertimeXe - The ending time of the Xth offering of the course.
    #
    # Returns nothing.
    def insert_course(self, school_id, course_name, course_no,
                      offertime1s, offertime1e, offertime2s, offertime2e,
                      offertime3s, offertime3e, offertime4s, offertime4e):
        database_command = """INSERT INTO Course(SchoolID, CourseName, CourseNumber, OfferTime1S, OfferTime1E, OfferTime2S, OfferTime2E, OfferTime3S, OfferTime3E, OfferTime4S, OfferTime4E) VALUES (%s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s);""" % (school_id, course_name, course_no, offertime1s, offertime1e, offertime2s, offertime2e, offertime3s, offertime3e, offertime4s, offertime4e)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'SOMETHING WENT WRONG!'


    # Public: Update school_name information in the School relation of the MySQL
    # database.
    #
    # old_school - The original name of the school to be updated.
    # new_school - The new name to replace the old name in the update.
    #
    # Returns nothing.
    def update_school(self, school_id, new_school_name):
        database_command = """UPDATE School SET SchoolName = '%s' WHERE SchoolID = %s;""" % (new_school_name, school_id)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'SOMETHING WENT WRONG!'

    # Public: Update course information in the Course relation of the MySQL
    # database.
    #
    # course_id   - The primary key CourseID attribute in the MySQL database.
    # school_id   - The SchoolID attribute in the MySQL database to which the course
    #               belongs.
    # course_name - The name of the course being updated.
    # course_no   - The course number of the course being offered.
    # offertimeXs - The starting time of the Xth offering of the course.
    # offertimeXe - The ending time of the Xth offering of the course.
    #
    # Returns nothing.
    def update_course(self, course_id, school_id, course_name, course_no,
                      offertime1s, offertime1e, offertime2s, offertime2e,
                      offertime3s, offertime3e, offertime4s, offertime4e):
        database_command = """UPDATE Course SET SchoolID = %s, CourseName = '%s', CourseNumber = '%s', OfferTime1S = '%s', OfferTime1E = '%s', OfferTime2S = '%s', OfferTime2E = '%s', OfferTime3S = '%s', OfferTime3E = '%s', OfferTime4S = '%s', OfferTime4E = '%s' WHERE CourseID = %s;""" % (school_id, course_name, course_no, offertime1s, offertime1e, offertime2s, offertime2e, offertime3s, offertime3e, offertime4s, offertime4e)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'SOMETHING WENT WRONG!'


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
            print 'SOMETHING WENT WRONG!'


    # Public: Delete a course from the MySQL database.
    #
    # course - The name of the course to be deleted.
    #
    # Returns nothing.
    def delete_course(self, course):
        database_command = """DELETE FROM Course WHERE CourseName = '%s';"""\
            % (course)
        self.cursor.execute(database_command)
        try: self.db.commit()
        except:
            self.db.rollback()
            print 'SOMETHING WENT WRONG!'


    # Public: Grab the school ID of a certain school, specified by name.
    #
    # school_name - The name of the school with the desired school ID.
    #
    # Returns an Integer specifying the school ID for the requested school.
    def get_school_id(self, school_name):
        database_command = """SELECT SchoolID FROM School WHERE SchoolName = '%s';""" % (school_name)
        self.cursor.execute(database_command)
        return self.cursor.fetchall()[0][0]


    # Public: Grab the course ID of a certain course, specified by name.
    #
    # course_name - The name of the course with the desired course ID.
    #
    # Returns an Integer specifying the course ID for the requested course.
    def get_course_id(self, course_name):
        database_command = """SELECT CourseID FROM Course WHERE CourseName = '%s';""" % (course_name)
        self.cursor.execute(database_command)
        return self.cursor.fetchall()[0][0]

    # Internal: Output the suite of methods bound to the Databaser object. This
    # method is intended to be used to pass these function handles to the
    # front-end interface.
    #
    # Returns a Tuple of bound method handles.
    def render_functions(self):
        return (self.get_schools,
                self.get_coursenames_by_school,
                self.get_coursenum_by_course,
                self.get_coursetimes_by_course,
                self.insert_school,
                self.insert_course,
                self.update_school,
                self.update_course,
                self.delete_school,
                self.delete_course,
                self.get_school_id,
                self.get_course_id)


if __name__ == '__main__':
    db = Databaser()
    db.get_school_id('Stanford University')
    
    
