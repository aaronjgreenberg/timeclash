"""
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This file contains a class definition for the Course class, which stores the times
for a course to check against the others. It also stores the function that checks
the Courses for time conflicts.

CREATED
-------
By: Aaron Greenberg
When: March 2012
"""

import datetime
import times_mergesort

# Public: A tiny module that represents an offering of a course from the MySQL
# TimeClash database.
class Offering(object):
    
    # Public: Initialize an Offering.
    #
    # day        - The day the course is offered.
    # start_time - The starting time of the course.
    # end_time   - The ending time of the course.
    def __init__(self, day = '', start_time = None, end_time = None):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    # Public: Create a string representation of an Offering.
    def __repr__(self):
        return "%s, %s -- %s" % (self.day, self.start_time, self.end_time)

# Public: A tiny module used to store time information for a certain course grabbed
# from the MySQL TimeClash database.
class Course(object):

    # Public: Initialize a Course.
    #
    # name        - The String name of the course.
    # offer_times - A List of Tuples that store all the offering times and days for
    #               the course.
    def __init__(self, name = '', offer_times = []):
        self.name = name
        self.offering_1 = None
        self.offering_2 = None
        self.offering_3 = None
        self.offering_4 = None
        # Remove all empty offertimes (offertimes with '--')
        offer_times = [otime for otime in offer_times if '--' not in otime]
        offerings = []
        for i in range(len(offer_times)):
            day = offer_times[i][0]
            starthr = int(offer_times[i][1])
            startmin = int(offer_times[i][2])
            endhr = int(offer_times[i][3])
            endmin = int(offer_times[i][4])
            start_time = datetime.time(hour = starthr, minute = startmin)
            end_time = datetime.time(hour = endhr, minute = endmin)
            exec "self.offering_%s = Offering(day, start_time, end_time)" % (i + 1)
            exec "offerings.append(self.offering_%s)" % (i + 1)
        self.offerings = tuple(offerings)
            


# Public: Check to see whether there is a conflict in the offer times of courses.
#   This algorithm works by removing a course from the list of courses, and then
#   checking each of its offerings against each of the offerings for all of the
#   other courses in the list.  If the selected courses offerings fall between
#   another of the courses' offerings, there's a conflict, and if the course is at
#   the same time, there is a conflict.  However, the days must be the same.  We can
#   remove a checked course from the list, because it's already been checked against
#   the other courses, so we don't need to check it again.
#
# courses - A list of Course objects, which will be checked for conflicts.
#
# Returns Boolean True if a conflict is found, Boolean False if none are found.
def timecheck(courses):
    while len(courses) > 1:
        selected_course = courses.pop(0)
        for offering_selected in selected_course.offerings:
            for course in courses:
                for offering in course.offerings:
                    if offering.day != offering_selected.day:
                        continue
                    if offering.start_time < offering_selected.start_time\
                            < offering.end_time:
                        return True
                    if offering.start_time < offering_selected.end_time\
                            < offering.end_time:
                        return True
                    if offering.start_time == offering_selected.start_time and\
                            offering.end_time == offering_selected.end_time:
                        return True
    return False


# Public: A second way to check whether there is a conflict in the offering times of
# the proposed courses.
#
# courses - A list of Course objects.
#
# Returns Boolean True if a conflict is found, Boolean false if not.
def timecheck_2(courses):
    offerings = []
    for course in courses:
        offerings.extend(course.offerings)
    offerings = times_mergesort.sort(offerings)
    for offering in offerings:
        print offering
    for i in range(len(offerings) - 1):
        if offerings[i].day != offerings[i + 1].day:
            continue
        else:
            if offerings[i + 1].start_time < offerings[i].end_time\
                    < offerings[i + 1].end_time:
                return True
            if offerings[i + 1].start_time == offerings[i].start_time and\
                    offerings[i + 1].end_time == offerings[i].end_time:
                return True
    return False

    
    
    
            
            
            

        
    
