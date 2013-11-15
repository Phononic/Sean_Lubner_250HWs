AY250 Homework 10
Sean Lubner

Notes:
* Required Modules: Flask, Flask-SQLAlchemy.  

* Make sure to preserve file structure of repo.  

* File uploader checks to make sure that neither that file, nor that user-entered collections name, has been used already.

* Server saves a copy of the file to its uploads folder, in case it ever needs to re-reference it (for design purposes only; for this assignment there is no need for the server to keep the file after it has parsed it into the database, other than to prevent users from re-uploading the same file multiple times and creating duplicate entries in the database).  The server cleans out the uploads folder each time it is launched (would have to be modified for a general server serving multiple people).

