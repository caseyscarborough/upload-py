Upload.py
---------

This is a simple CGI script in Python that is used to connect to a MySQL database, and upload a PDF file the user specifies to the filesystem. It is used in conjunction with a HTML form, using POST to send information to the script to perform the upload and insert into the database.

The form that I am using with the script follows this format:
<pre>&lt;form enctype=&quot;multipart/form-data&quot; action=&quot;upload.py&quot; method=&quot;post&quot; id=&quot;form&quot;&gt;
	&lt;input type=&quot;text&quot; name=&quot;title&quot; placeholder=&quot;Title&quot;&gt;
	&lt;input type=&quot;text&quot; name=&quot;author&quot; placeholder=&quot;Author&quot;&gt;
	&lt;input type=&quot;text&quot; name=&quot;edition&quot; placeholder=&quot;Edition&quot;&gt;
	&lt;input type=&quot;date&quot; name=&quot;pub-date&quot;&gt;
	&lt;input type=&quot;text&quot; name=&quot;isbn&quot; placeholder=&quot;ISBN-13&quot;&gt;
	&lt;input type=&quot;file&quot; name=&quot;file&quot;&gt;
	&lt;input type=&quot;file&quot; name=&quot;image&quot;&gt;
	&lt;input type=&quot;submit&quot; value=&quot;Submit&quot;&gt;
&lt;/form&gt;</pre>