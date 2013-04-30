Upload.py
=========

This is a simple CGI script written in Python 2.6 that is used to connect to a MySQL database, and upload a PDF file the user specifies to the filesystem. It is used in conjunction with a HTML form, using POST to send information to the script to perform the upload and insert into the database.

The Form
--------

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

The Database
------------

The database is a MySQL database with a table containing seven columns: id, title, filename, author, edition, publication date, and isbn. You can create the database on your own using the following query:
<pre>DROP TABLE IF EXISTS `books`;
CREATE TABLE IF NOT EXISTS `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `author` varchar(100) NOT NULL,
  `edition` varchar(3) NOT NULL,
  `publication_date` date NOT NULL,
  `isbn` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=38 ;</pre>