#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import MySQLdb

def file_buffer(f, chunk_size=50000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk


def upload_file(file):
	try:
		# strip leading path from file name to avoid directory traversal attacks
		fn = os.path.basename(file.filename)
		if fn.end_with(".pdf"):
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
		
		db = MySQLdb.connect(
	   	host="localhost",
	   	user="root",
	   	passwd="",
	   	db=""
		);
		cur=db.cursor();query = "INSERT INTO books (title, filename, author, edition, publication_date, isbn) \
		VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (title, fn.replace(".pdf", ""), author, edition, pub_date, isbn);result = cur.execute(query); 
		if result:
			print "Location: upload.php?success=1"
		else:
	   		print "Location: upload.php?err=0"
	else:
		message = 'No file was uploaded'
		print "Status: 302 Moved"
		print "Location: upload.php?err=1"
	
	
	print """\
Content-type: text/html\n\n
<html><body>
<p>%s, %s, %s, %s, %s, %s</p>
%s
</body></html>
""" % (title, author, edition, pub_date, isbn, message, query)
	
if __name__ == "__main__": main()
