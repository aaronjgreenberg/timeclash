/*
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This SQL script creates the two database tables that store the information used by
the application.

CREATED
-------
By: Aaron Greenberg
When: March 2012
*/

CREATE TABLE School (
       SchoolID		INT AUTO_INCREMENT PRIMARY KEY,
       SchoolName 	VARCHAR( 255 ),
       SchoolCity 	VARCHAR( 255 ),
       SchoolCountry 	VARCHAR( 255 ) );

CREATE TABLE Course (
       P_ID		INT AUTO_INCREMENT PRIMARY KEY,
       CourseID		VARCHAR( 255 ),
       OfferTime1	DATETIME,
       OfferTime2	DATETIME,
       OfferTime3	DATETIME,
       OfferTime4	DATETIME,
       OfferTime5	DATETIME,
       CourseDept	VARCHAR( 255 ) );