#!/usr/bin/python
# filename: upload.py
#
# This is a simple CGI script written in Python 2.6 that 
# is used to connect to a MySQL database, and upload a PDF 
# file the user specifies to the filesystem. It is used in 
# conjunction with a HTML form, using POST to send information 
# to the script to perform the upload and insert into the database.
#
# Written by Casey Scarborough - 2013

import cgi, os
import cgitb; cgitb.enable()
import MySQLdb

# Database class used for connecting to the database and insertion
class Database:
	# Constructor
	def __init__(self, **kwargs):
		self.host = kwargs.get('host')
		self.user = kwargs.get('user')
		self.password = kwargs.get('password')
		self.database = kwargs.get('database')
		
		# Connect to the database
		self._db = MySQLdb.connect(
			host = self.host,
			user = self.user,
			passwd = self.password,
			db = self.database
		)
	
	# This method is used to insert into the database
	def insert(self, row):
		query = "INSERT INTO books (title, filename, author, edition, publication_date, isbn) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (row['title'], row['filename'], row['author'], row['edition'], row['publication_date'], row['isbn'])
		cur = self._db.cursor(); # Create a cursor
		result = cur.execute(query) # Execute the query
		return result # Return the result

# This method is used to read the file in chunks
def file_buffer(f, chunk_size=50000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

# This method is used to upload the specified file
def upload_book(book):
	try:
		# Strip leading path from filename to avoid directory traversal attacks
		fn = os.path.basename(book.filename)
		# Check if the filename ends with .pdf
		if fn.endswith(".pdf"):
			# Remove the spaces and open the new file
			fn = fn.replace(" ", ".")
			f = open(fn, 'wb', 50000)
			
			# Read the file in chunks and write it to the new file
			for chunk in file_buffer(book.file):
				f.write(chunk)
			f.close()
	
			message = 'The file "' + fn + '" was uploaded successfully'	
		else:
			message = 'Improper file format.'
	except:
		message = 'There was a problem uploading the file'
	return message, fn

def upload_image(image, filename):
	try:
		f = open("img/" + filename, 'wb', 50000)
		for chunk in file_buffer(image.file):
			f.write(chunk)
		f.close()
		message = 'The image "' + filename + '" was uploaded successfully'
	except:
		message = 'There was a problem uploading the image'
	return message

def main():
	# Get submitted form data
	form = cgi.FieldStorage()
	
	# Set each field to a variable
	title = form.getfirst('title', 'none')
	author = form.getfirst('author', 'none')
	edition = form.getfirst('edition', 'none')
	pub_date = form.getfirst('pub-date', 'none')
	isbn = form.getfirst('isbn', 'none')
	
	# Create the fn and query variables
	fn = ''; query = '';
	      
	# Get the book from the form data
	book = form['file']
	image = form['image']
	
	if book.filename: # If the book exists
		book_message, book_fn = upload_book(book)
		
		# Open a new database connection
		db = Database(
			host="localhost",
			user="casey",
			password="",
			database="books"
		)
		
		if book_fn.endswith(".pdf"): # If filename ends with pdf
			image_fn = book_fn.replace(".pdf", "") + ".jpg"
			image_message = upload_image(image, image_fn)
			# insert into the db
			result = db.insert(dict(
				title = title,  
				filename = book_fn.replace(".pdf", ""), # strip the pdf from the end
				author = author,
				edition = edition,
				publication_date = pub_date,
				isbn = isbn
			))
		
			if result: # If query executed successfully redirect to success
				print "Location: ./upload.php?success=1"
			else: # otherwise redirect to error
		   		print "Location: ./upload.php?err=0"
	else: # If the book doesn't exist redirect to error
		print "Location: ./upload.php?err=1"
	
	# Output some html
	print "Content-type: text/html\n\n<html><body>"
	print "<p>If you see this message, something went wrong!<br>Click <a href=""./upload.php"">here</a> to return to the upload page.</p></body></html>"
		
if __name__ == "__main__": main()
