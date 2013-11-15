AY250 Homework 10
Sean Lubner

Everything works except getting the SQLAlchemy command to recognize the name of the table ('article'), for some reason...

All HTML browsing works, file uplaod as well as .bib parsing and database creation (and can upload non .bib file types, like pictures, from debugging stage)

The "query" form works, passes the query string, and I can parse and display the imported and parsed .bib file database.

The only problem is that when I try to actually apply the query string to the database itself, it doesn't recognize the table name, in spite of the __table__ = 'article' statement.

If you care to try fixing this (if you know how) to make everything work, I have tagged the two relevant lines with:

#@@@@@@ TAG @@@@@@

(so you can do a ctrl + find on that tag to find the relevant lines).  One tag will take you to where I (attempt to) declare the table name.  The other tag will take you to where I am returning the entire database (instead of the query results -- to demonstrate that I can print out results even if I can't get the query to work).  You can change this line to instead call the run_query() function I have defined, on the query string "query_raw".

Of course, I do not expect you to take the time to debug my code... but I wanted to demonstrate that all aspects except for this one feature work.

Notes:
* Required Modules: Flask, Flask-SQLAlchemy.  

* Make sure to preserve file structure of repo.  

* File uploader checks to make sure that neither the file, nor that user-specified collections name, has already been used before during that session.

* Server saves a copy of the file to its uploads folder.  The server clears out the uploads folder each time it is relaunched.

