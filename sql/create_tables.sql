/*
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This SQL script creates the two database tables that store the information used by
the application.

TO DO
-----
* Fix the tables to contain the correct attributes.
  * The Course table should have a composite key made up of CourseID and SchoolID,
    where, SchoolID is a foreign key that references the School table.
  * Find out how to make the foreign key part of the primary key.
* Add database design section to documentation showing how the tables relate, and
  the ERD.

CREATED
-------
By: Aaron Greenberg
When: March 2012
*/

CREATE TABLE IF NOT EXISTS School (
       SchoolID		INT NOT NULL AUTO_INCREMENT,
       SchoolName 	VARCHAR( 255 ),
       CONSTRAINT PK_SchoolID PRIMARY KEY ( SchoolID ) );

CREATE TABLE IF NOT EXISTS Course (
       CourseID		INT NOT NULL AUTO_INCREMENT,
       SchoolID		INT NOT NULL,
       CourseName	VARCHAR( 255 ),
       CourseNumber	VARCHAR( 255 ),
       OfferTime1S	DATETIME,
       OfferTime1E	DATETIME,
       OfferTime2S	DATETIME,
       OfferTime2E	DATETIME,
       OfferTime3S	DATETIME,
       OfferTime3E	DATETIME,
       OfferTime4S	DATETIME,
       OfferTime4E	DATETIME,
       CONSTRAINT FK_SchoolID FOREIGN KEY ( SchoolID )
       		  	      REFERENCES School( SchoolID ),
       CONSTRAINT PK_CourseID PRIMARY KEY ( CourseID, SchoolID ) );