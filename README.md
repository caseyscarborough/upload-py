Upload.py
---------

This is a simple CGI script in Python that is used to connect to a MySQL database, and upload a PDF file the user specifies to the filesystem. It is used in conjunction with a HTML form, using POST to send information to the script to perform the upload and insert into the database.

The form that I am using with the script follows this format:
<pre><form enctype="multipart/form-data" action="upload.py" method="post" id="form">
	<input type="text" name="title" placeholder="Title">
	<input type="text" name="author" placeholder="Author">
	<input type="text" name="edition" placeholder="Edition">
	<input type="date" name="pub-date">
	<input type="text" name="isbn" placeholder="ISBN-13">
	<input type="file" name="file">
	<input type="file" name="image">
	<input type="submit" value="Submit">
</form></pre>