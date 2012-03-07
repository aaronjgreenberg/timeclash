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

CREATED
-------
By: Aaron Greenberg
When: March 2012
*/

CREATE TABLE School (
       SchoolID		INT NOT NULL AUTO_INCREMENT,
       SchoolName 	VARCHAR( 255 ),
       PRIMARY KEY( SchoolID ) );

CREATE TABLE Course (
       CourseID		INT NOT NULL AUTO_INCREMENT,
       SchoolID		INT NOT NULL,
       CourseName	VARCHAR( 255 ),
       OfferTime1	DATETIME,
       OfferTime2	DATETIME,
       OfferTime3	DATETIME,
       OfferTime4	DATETIME,
       OfferTime5	DATETIME,
       CONSTRAINT FK_SchoolID FOREIGN KEY ( SchoolID ) REFERENCES School( SchoolID )
       );