/*
TimeClash
=========
An application to highlight the conflicts in your proposed semester schedule.

This SQL script creates the TimeClash database for use in the TimeClash application,
and grants privileges to the user.

The default username is 'aaron', and the default password is 'COMP311'. If desired,
you may change the username and password as you see fit. The last two lines of the
GRANT statement may be changed as follows:

    TO your_username@localhost
    IDENTIFIED BY 'your_password'

CREATED
-------
By: Aaron Greenberg
When: March 2012
*/

CREATE DATABASE IF NOT EXISTS TimeClash;

GRANT SELECT, INSERT, UPDATE, DELETE
      ON TimeClash.*
      TO aaron@localhost
      IDENTIFIED BY 'COMP311';