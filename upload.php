<?php
	// These are the default location for file uploads.
	// Change them if necessary.
	$book_directory = "files/documents/";
	$image_directory = "files/images/";

	$conn = mysql_connect("127.0.0.1", "root", "root");
	if(!$conn) {
		die("Could not connect to database: " . mysql_error());
	}
	
	$db_select = mysql_select_db("books", $conn);
	if(!$db_select) {
		die("Could not select database: " . mysql_error());
	}

	$query = "SELECT * FROM `books` ";
	$query .= "ORDER BY `id` ASC";
	$book_set = mysql_query($query, $conn);

	if(isset($_GET['success'])) {
		if($_GET['success'] == 1) {
			$message = "File successfully uploaded!";
		}
	} else if (isset($_GET['err'])) {
		if($_GET['err'] == 1) {
			$message = "No file was specified.";
		} else if ($_GET['err'] == 0) {
			$message = "There was a problem inserting into the database.";
		} else if ($_GET['err'] == 2) {
			$message = "There was a problem with one of your fields.";
		}
	}

	function display_list($book_set){
		global $book_directory;
		echo "<div class=\"span12 book\">";
		echo "<table width=\"100%\" style=\"margin:0 auto; padding: 10px;\">";
		echo "<tr style=\"font-weight:bold;\"><td>Title</td><td>Author</td><td>Edition</td><td>Pub. Date</td><td>ISBN-13</td></tr>";
		while ($book = mysql_fetch_array($book_set)) {
			echo "<tr style=\"padding:5px;\"><td><a href=\"" . $book_directory . $book['filename'] . ".pdf\">" . $book['title'] . "</a></td>";
			echo "<td>" . $book['author'] . "</td>";
			echo "<td>" . $book['edition'] . "</td>";
			echo "<td>" . $book['publication_date'] . "</td>";
			echo "<td>" . $book['isbn'] . "</td>";
		}
		echo "</table></div>";
	}

	function display_with_images($book_set){
		global $book_directory, $image_directory;
		while ($book = mysql_fetch_array($book_set)) {
			echo "<br><div class=\"book-img\" style=\"float:left; clear:both; padding: 20px;\">";
			echo "<a href=\"" . $book_directory . $book['filename'] . ".pdf\"><img src=\"" . $image_directory . $book['filename'] . ".jpg\" style=\"height:110px;width:auto;max-width:110px;\" class=\"book-img\"></a>";
			echo "</div><div class=\"book-details\" style=\"margin-left:30px;\"><h4><a href=\"" . $book_directory . $book['filename'] . ".pdf\">" . $book['title'] . "</a></h4>";
			echo "<p style=\"font-size:75%\">" . $book['author'] . "<br>Edition: " . $book['edition'] . "<br>Publication Date: " . $book['publication_date'] . "<br>ISBN-13: " . $book['isbn'] . "</p></div>";
		}
	}
?>
<!doctype html>
<html>
<head>
	<title>Book Upload</title>
</head>
<body>
	<h1>Upload a Book</h1>
	<?php 
		if(isset($message)){
			if(isset($_GET['err'])) {
				echo "<div class=\"alert alert-error\">";
			} else {
				echo "<div class=\"alert alert-success\">";
			}
			echo $message;
			echo "</div>";
		} 
	?>
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
	<div id="book-list"><?php
		display_list($book_set);
		//display_with_images($book_set);
		?>
	</div>
</body>
</html>