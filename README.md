Introduction
============

This is a simple CGI script written in Python 2.6 that is used to connect to a SQLite3 database, and upload a PDF and JPG cover for a book the user specifies to the filesystem. It is used in conjunction with a HTML form, using POST to send information to the script to perform the upload and insert into the database.

The Environment
---------------

The application runs using Python 2.6, Apache (or another webserver using CGI and PHP), CGI (to execute the Python upload script), and PHP5 (for the form). To run the application, you must have the contents above in your public directory for your webserver, and navigate to the upload.php file. If your environment is properly set up, then you should be able to upload books using the form.


The Form
--------

The form that I am using with the script follows this format:
```html
<form enctype="multipart/form-data" action="upload.py" method="post" id="form">
	<p>
		<input type="text" name="title" placeholder="Title"><br>
		<input type="text" name="author" placeholder="Author"><br>
		<input type="text" name="edition" placeholder="Edition"><br>
		<input type="date" name="pub-date"><br>
		<input type="text" name="isbn" placeholder="ISBN-13"><br>
	</p>
		Books must be uploaded in PDF Format.<br>
		<input type="file" name="file"><br><br>
		Images must be uploaded in JPG Format.<br>
		<input type="file" name="image"><br><br>
		<input type="submit" value="Upload">
	</p>
</form>
```


The Database
------------

The database is a SQLite3 database with a table containing seven columns: id, title, filename, author, edition, publication date, and isbn. The database file is included and is called books.db. If you'd like to create the database on your own, you can do so with the following python in the python shell:
<pre>&gt;&gt;&gt; import sqlite3
&gt;&gt;&gt; db = sqlite3.connect(&#39;books.db&#39;)
&gt;&gt;&gt; cursor = db.cursor()
&gt;&gt;&gt; cursor.execute(&#39;create table books (id INTEGER PRIMARY KEY, title TEXT, filename TEXT, author TEXT, edition TEXT, publication_date DATE, isbn TEXT)&#39;)
&gt;&gt;&gt; db.commit()
&gt;&gt;&gt; exit()
</pre>


Troubleshooting
---------------

### Unable to Execute Python CGI Script (500 Error)

Ensure that the permissions on the upload.py file are set to 755.

Ensure that you have Python 2.6 installed and the path to your Python executable in the first line of the upload.py file.

### Python script outputting as plain text

Be sure that you are able to execute CGI scripts in this directory on the web server, or place the file in cgi-bin and adjust path names in the upload.php and upload.py files. To enable CGI execution in this directory (recommended), create an .htaccess file at the root of the directory with the upload.py file with the following content:
<pre>AddHandler cgi-script .cgi .pl
Options +ExecCGI</pre>

### Final Note

I've left cgitb enabled in the upload.py file for error reporting. This should help to describe any other errors. If you are having bigger problems, feel free to contact me at caseyscarborough[at]gmail[dot]com.


