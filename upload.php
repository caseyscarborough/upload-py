<?php
	if(isset($_GET['success'])) {
		if($_GET['success'] == 1) {
			$message = "File successfully uploaded!";
		}
	} else if (isset($_GET['err'])) {
		if($_GET['err'] == 1) {
			$message = "No file was specified.";
		} else if ($_GET['err'] == 0) {
			$message = "There was a problem inserting into the database.";
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
			<input type="file" name="file" value="Upload Book"><br><br>
			<input type="submit" value="Submit">
		</p>
	</form>
</body>
</html>