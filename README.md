[![TimeClash](http://dl.dropbox.com/u/2087618/Banners/timeclash.jpg)](http://db.tt/lov8S6kS)

Whenever I'm trying to register for classes, I always find that one of
the hardest parts is picking courses that don't conflict.  At best,
all the courses offered will be displayed on a calendar, which is
usually so cluttered it's nearly impossible to keep track of all of
your options.  At worst, there's no calendar at all, and you need to
keep going back and forth between webpages, comparing offering times
and holding them in your head to make sure you end up with a schedule
that doesn't have time conflicts.  The goal of this application is to
lessen the headache of choosing courses by making clear which ones
conflict, and when.

## Installation

To run this application, you'll need to have
[Python](http://python.org/download/) and
[MySQL](http://www.mysql.com/downloads/) installed on your computer.

Then, run the SQL scripts to create the database and tables,
respectively:

	shell> mysql -u root -p < create_db.sql

To create the database, you'll need to run MySQL as root.  

**NOTE:** The create_db script grants access to 'aaron@localhost' with
password 'COMP311' as defaults.  You can change those by editing the
script, if you care, but you'll also need to pass the new values to
the timeclash.py script so MySQL is able to connect to the database.

After creating the database, create the database tables used to store
the school and course information with the create_tables.sql script
(you can run this script as a normal user):

	shell> mysql -u aaron -p timeclash < create_tables.sql

After creating the database, run the timeclash.py script to launch the
application:

	shell> python timeclash.py
	
If you changed the default username or password, run this:
	
	shell> python timeclash.py --user=alternate_user --pw=alternate_password

## TO DO

* Write a better conflict-checking algorithm that can tell you exactly
  which courses are causing the problems.
* Change the interface so that users can select which specific offering
  they want to use in their schedule.
* Change the interface so that users can dynamically change the number
  of offerings a course has.
    * Is this possible with MySQL? Might need to think of a clever way
      to implement.

## About

I originally started building this application as my final project for
the course COMP311: Foundations of Database Systems at the Hong Kong
Polytechnic University.  The assignment is to create any database
application with a user interface.  I chose to create this application
after spending a frustrating two weeks trying to organize my course
schedule at the beginning of my study abroad semester.

To use this application, you can add your school to the database, and
then populate the school with courses and some information about them,
including the offering times.  Then you can create a schedule with all
your courses, and the application will check if any of them
conflict. It will tell you which do, if any, and when they conflict
and for how long.

If you have any suggestions or recommendations, please don't hesitate
to open an issue.

Thanks!

-Aaron

## Contributors

To create the user interface for this application, I used Allen
Downey's Python module Gui.py, which he makes available under the
terms of the GNU General Public License.
