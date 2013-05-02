#!/usr/bin/python2.6
'''
.. module:: upload
    :platform: Unix
    :synopsis: 
This is a simple CGI script written in Python 2.6 that 
is used to connect to a SQLite3 database, and upload a 
PDF and JPG cover for a book the user specifies to the 
filesystem. It is used in conjunction with a HTML form, 
using POST to send information to the script to perform 
the upload and insert into the database.


.. moduleauthor:: Casey Scarborough <casey@caseyscarborough.com>

'''

import cgi, os
import cgitb; cgitb.enable()
import sqlite3

database_filename = 'books.db'

# These are the default locations for file uploads.
book_upload_directory = "files/documents/"
image_upload_directory = "files/images/"
upload_form_directory = "./"

class Database:
	'''Class that handles connections to the SQLite3 database.
	It contains two methods, the constructor, and the insert method.

	Attributes:
		filename (str): The filename for the database
		table (str): The table name in the database
	'''

	def __init__(self, **kwargs):
		self.filename = kwargs.get('filename')
		self.table = kwargs.get('table', 'test')
		self._db = sqlite3.connect(self.filename)
		self._db.row_factory = sqlite3.Row
	
	def insert(self, row):
		'''This function handles insertion into the database.

		Args:
			row (dict): The row to be inserted into the database.

		Returns:
			result (str): The result of the function.
		'''
		query = "insert into books (title, filename, author, edition, publication_date, isbn) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (row['title'], row['filename'], row['author'], row['edition'], row['publication_date'], row['isbn'])
		try:
			result = self._db.execute(query) # Execute the query
			self._db.commit()
			return result # Return the result
		except Exception as e:
			print "Location: " + upload_form_directory + "upload.php?err=2"
			print e

	@property
	def filename(self): 
		return self._filename

	@filename.setter
	def filename(self, fn):
		self._filename = fn
		self._db = sqlite3.connect(fn)
		self._db.row_factory = sqlite3.Row

	@filename.deleter
	def filename(self): self.close()

	@property
	def table(self): return self._table
	@table.setter
	def table(self, t): self._table = t
	@table.deleter
	def table(self): self._table = 'test'

	def close(self):
		self._db.close()
		del self._filename

def file_buffer(f, chunk_size=50000):
	'''This function is used as a buffer to read a file in chunks.

	Args:
		f (file): The specified file.
		chunk_size (int): The size of the chunks. The default is 50000.
	'''
	while True:
		chunk = f.read(chunk_size)
		if not chunk: break
		yield chunk

def upload_book(book):
	'''This function handles uploading the file for the module.

	Args:
		book (file): The book file.

	Returns:
		message (str): The result of the function.'''
	message = ''
	try:
		# Strip leading path from filename to avoid directory traversal attacks
		fn = os.path.basename(book.filename)
		# Check if the filename ends with .pdf
		if fn.endswith(".pdf"):
			# Remove the spaces and open the new file
			fn = fn.replace(" ", ".")
			f = open(book_upload_directory + fn, 'wb', 50000)
			# Read the file in chunks and write it to the new file
			for chunk in file_buffer(book.file):
				f.write(chunk)
			f.close()
			message = 'The file "' + fn + '" was uploaded successfully'	
	except:
		message = 'There was a problem uploading the file'
	return message, fn

def upload_image(image, filename):
	'''This function handles uploading images for the module.

	Args:
		image (file): The image file.
		filename (str): The name of the file to be uploaded.

	Returns:
		message (str): The result of the function.'''

	#try:
	f = open(image_upload_directory + filename, 'wb', 50000)
	for chunk in file_buffer(image.file):
		f.write(chunk)
	f.close()
	message = 'The image "' + filename + '" was uploaded successfully'
	#except:
		#message = 'There was a problem uploading the image'
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
		image_message = ''
		# Open a new database connection
		db = Database(filename = database_filename, table = 'books')
		
		if book_fn.endswith(".pdf"): # If filename ends with pdf
			image_fn = book_fn.replace(".pdf", "") + ".jpg"
			if image.filename:
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
				print "Location: " + upload_form_directory + "upload.php?success=1"
			else: # otherwise redirect to error
		   		print "Location: " + upload_form_directory + "upload.php?err=0"
		else:
			print "Location: " + upload_form_directory + "upload.php?err=3"
	else: # If the book doesn't exist redirect to error
		print "Location: " + upload_form_directory + "upload.php?err=1"
	
	# Output some html
	print "Content-type: text/html\n\n<html><body>"
	print "<p>If you see this message, something went wrong!<br>Click <a href=""./upload.php"">here</a> to return to the upload page.</p></body></html>"
	#print book_message
	#print image_message
if __name__ == "__main__": main()
