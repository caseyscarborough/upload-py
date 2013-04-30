#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import MySQLdb

print "Content-type: text/html\n\n<html><body>"

class Database:
	def __init__(self, **kwargs):
		self.host = kwargs.get('host')
		self.user = kwargs.get('user')
		self.password = kwargs.get('password')
		self.database = kwargs.get('database')
		
		self._db = MySQLdb.connect(
			host = self.host,
			user = self.user,
			passwd = self.password,
			db = self.database
		)
	
	def insert(self, row):
		query = "INSERT INTO books (title, filename, author, edition, publication_date, isbn) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (row['title'], row['filename'], row['author'], row['edition'], row['publication_date'], row['isbn'])
		return query
	
def file_buffer(f, chunk_size=50000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk


def upload_file(file):
	try:
		# strip leading path from file name to avoid directory traversal attacks
		fn = os.path.basename(file.filename)
		if fn.endswith(".pdf"):
			fn = fn.replace(" ", "_")
			f = open(fn, 'wb', 50000)
			
			# Read the file in chunks
			for chunk in file_buffer(file.file):
				f.write(chunk)
			f.close()
	
			message = 'The file "' + fn + '" was uploaded successfully'
		else:
			message = 'The book must be a PDF file.'
	except:
		message = 'There was a problem uploading the file'
	return message, fn

def main():
	form = cgi.FieldStorage()
	
	title = form.getfirst('title', 'none')
	author = form.getfirst('author', 'none')
	edition = form.getfirst('edition', 'none')
	pub_date = form.getfirst('pub-date', 'none')
	isbn = form.getfirst('isbn', 'none')
	fn = ''
	query = ''
	      
	book = form['file']
	
	if book.filename:
		message, fn = upload_file(book)
		
		db = Database(
			host="localhost",
			user="casey",
			password="",
			database="books"
		)
		
		if fn.endswith(".pdf"):
			result = db.insert(dict(
				title=title,
				filename=fn.replace(".pdf", ""),
				author=author,
				edition=edition,
				publication_date=pub_date,
				isbn=isbn
			))
		
			if result:
				print "Location: upload.php?success=1"
				print result
			else:
		   		print "Location: upload.php?err=0"
	else:
		message = 'No file was uploaded'
		print "Status: 302 Moved"
		print "Location: upload.php?err=1"
	
	print "<p>%s, %s, %s, %s, %s, %s</p></body></html>" % (title, author, edition, pub_date, isbn, message)
	
if __name__ == "__main__": main()
