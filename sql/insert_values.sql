/*
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This SQL script is used to insert a few values into the School and Course tables for
practice and to test the application.

CREATED
-------
By: Aaron Greenberg
When: April 2012
*/

INSERT INTO School(SchoolName) VALUES ('Olin College of Engineering'),
       	    		       	      ('Hong Kong Polytechnic University'),
				      ('Stanford University'),
				      ('Harvard University'),
				      ('Yale University');

INSERT INTO Course(SchoolID, CourseName, CourseNumber, OfferTime1S, OfferTime1E,
       	    		     OfferTime2S, OfferTime2E, OfferTime3S, OfferTime3E,
			     OfferTime4S, OfferTime4E)
	VALUES (1, 'Software Systems', 'ENGR3525', '1000-01-01 10:50:00', '1000-01-01 12:30:00', '1000-01-04 10:50:00', '1000-01-04 12:30:00', '1000-01-01 13:30:00', '1000-01-01 15:10:00', '1000-01-04 13:30:00', '1000-01-04 15:10:00'),
	       (1, 'Human Factors Interface Design', 'ENGR3220', '1000-01-01 15:20:00', '1000-01-01 18:00:00', '1000-01-04 15:20:00', '1000-01-04 18:00:00', NULL, NULL, NULL, NULL),
	       (2, 'Foundations of Database Systems', 'COMP311', '1000-01-01 18:30:00', '1000-01-01 22:00:00', NULL, NULL, NULL, NULL, NULL, NULL),
	       (2, 'Data Structures & Algorithms', 'COMP305', '1000-01-03 18:30:00', '1000-01-03 21:30:00', NULL, NULL, NULL, NULL, NULL, NULL);