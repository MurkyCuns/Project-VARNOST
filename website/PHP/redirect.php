<?php 

session_start();

if (isset($_POST['showAllPasswords'])) {
	header("Location: ../PHP/showAllPasswords.php", TRUE, 301);
	exit();
}

if (isset($_POST['addPassword'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/addPassword.php", TRUE, 301);
	exit();
}

?>