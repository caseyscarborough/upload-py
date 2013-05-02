<?php
	// These are the default location for file uploads.
	// Change them if necessary.
	$book_directory = "files/documents/";
	$image_directory = "files/images/";

	$conn = new SQLite3('books.db');

	$query = "SELECT * FROM `books` ";
	$query .= "ORDER BY `id` ASC";
	$book_set = $conn->query($query);

	if(isset($_GET['success'])) {
		if($_GET['success'] == 1) {
			$message = "File successfully uploaded!";
		}
	} else if (isset($_GET['err'])) {
		if($_GET['err'] == 1) {
			$message = "No book was specified.";
		} else if ($_GET['err'] == 0) {
			$message = "There was a problem inserting into the database.";
		} else if ($_GET['err'] == 2) {
			$message = "There was a problem with one of your fields.";
		} else if ($_GET['err'] == 3) {
			$message = "Improper file format.";
		}
	}

	function display_list($book_set){
		global $book_directory;
		echo "<div class=\"span12 book\">";
		echo "<table width=\"100%\" style=\"margin:0 auto; padding: 10px;\">";
		echo "<tr style=\"font-weight:bold;\"><td>Title</td><td>Author</td><td>Edition</td><td>Pub. Date</td><td>ISBN-13</td></tr>";
		while ($book = $book_set->fetchArray()) {
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
		echo "<div class=\"books\">";
		while ($book = $book_set->fetchArray()) {
			echo "<br><div style=\"float:left; clear:both;\">";
			echo "<a href=\"" . $book_directory . $book['filename'] . ".pdf\"><img src=\"" . $image_directory . $book['filename'] . ".jpg\" style=\"height:110px;width:auto;max-width:110px;\" class=\"book-img\"></a>";
			echo "</div><div class=\"book-details\" style=\"margin-left:30px;\"><h4><a href=\"" . $book_directory . $book['filename'] . ".pdf\">" . $book['title'] . "</a></h4>";
			echo "<p style=\"font-size:75%\">" . $book['author'] . "<br>Edition: " . $book['edition'] . "<br>Publication Date: " . $book['publication_date'] . "<br>ISBN-13: " . $book['isbn'] . "</p></div>";
		} echo "</div>";
	}
?>
<!doctype html>
<html>
<head>
	<title>Book Upload</title>
	<link href="css/bootstrap.min.css" type="text/css" rel="stylesheet">
	<link href="css/main.css" type="text/css" rel="stylesheet">
	<link href="css/bootstrap-responsive.min.css" type="text/css" rel="stylesheet">
	<script src="http://code.jquery.com/jquery-latest.js"></script>
	<script src="http://ajax.aspnetcdn.com/ajax/jquery.validate/1.9/jquery.validate.min.js"></script>
	<script>
	function fade(){
		$('#error').hide().fadeIn(400);
	  	$('#error').delay(4000).fadeOut(500);
	}

	$(document).ready(function(){
		fade();
	});
	</script>
</head>
<body>
<div class="container">
<div class="row-fluid">
	<div class="span6 offset3 mainarticle">
		<h1>Upload a Book</h1><br>
		<?php 
			if(isset($message)){
				if(isset($_GET['err'])) {
					echo "<div id=\"error\" style=\"display:none\" class=\"alert alert-error\">";
				} else {
					echo "<div id=\"error\" style=\"display:none\" class=\"alert alert-success\">";
				}
				echo $message;
				echo "</div>";
			} 
		?>
		<form enctype="multipart/form-data" action="upload.py" method="post" id="upload-form" novalidate="novalidate">
			<fieldset>
				<input type="text" name="title" placeholder="Title" style="width:75%">
				<input type="text" name="author" placeholder="Author" style="width:75%">
				<input type="text" name="edition" placeholder="Edition" style="width:75%">
				<input type="date" name="pub-date" style="width:75%">
				<input type="text" name="isbn" placeholder="ISBN-13" style="width:75%">
			</p><br>
			<div id="file-upload">Files must be uploaded in PDF Format.<br>
			<input type="file" name="file" class="upload" value="Upload Book"></div><br>
			<div id="image-upload">Images must be in JPG Format<br>
			<input type="file" name="image" class="upload" value="Upload Image"></div>
			<div id="submit-upload" style="clear:both;"><br><p style="text-align:center"><br>
			<input type="submit" value="Upload" class="btn btn-success btn-large"></div>
			</fieldset>
		</form><br>
		<hr>
		<div id="book-list"><br>
			<h3>Book List</h3><br>
			<?php
				//display_list($book_set);
				display_with_images($book_set);
			?>
		</div>
	</div>
	</div>
</div>
</div>

<script>
(function($,W,D) {
    var jquery = {};

    jquery.util = {
        setupFormValidation: function() {
            //form validation rules
            $("#upload-form").validate({
                rules: {
                    title: "required",
                    author: "required",
                    edition: "required",
                    date: "required",
                    isbn: "required",
                    file: "required"
                },
                messages: {
                    title: "Please enter a title",
                    author: "Please enter an author",
                    edition: "Please enter an edition",
                    date: "Please enter a valid date",
                    isbn: "Please enter an ISBN, or enter 'None'",
                    file: "Please select a file"
                },
                submitHandler: function(form) {
                    form.submit();
                }
            });
        }
    }

    //when the dom has loaded setup form validation rules
    $(document).ready(function($) {
        jquery.util.setupFormValidation();
    });

})(jQuery, window, document);
</script>
</body>
</html>