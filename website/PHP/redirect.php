<?php 

session_start();

if (isset($_POST['backToIndex'])) {
	session_destroy();
	header("Location: ../PHP/index.php", TRUE, 301);
	exit();
}

if (isset($_POST['showAllPasswords'])) {
	header("Location: ../PHP/showAllPasswords.php", TRUE, 301);
	exit();
}

if (isset($_POST['addPassword'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/addPassword.php", TRUE, 301);
	exit();
}

if (isset($_POST['showRelatedToSite'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/showRelatedToSite.php", TRUE, 301);
	exit();
}

if (isset($_POST['showRelatedToEmail'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/showRelatedToEmail.php", TRUE, 301);
	exit();
}

if (isset($_POST['showRelatedToUsername'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/showRelatedToUsername.php", TRUE, 301);
	exit();
}

if (isset($_POST['showRelatedToClass'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/showRelatedToClass.php", TRUE, 301);
	exit();
}

if (isset($_POST['showAllSites'])) {
	header("Location: ../PHP/showAllSites.php", TRUE, 301);
	exit();
}

if (isset($_POST['showAllEmails'])) {
	header("Location: ../PHP/showAllEmails.php", TRUE, 301);
	exit();
}

if (isset($_POST['showAllUsernames'])) {
	header("Location: ../PHP/showAllUsernames.php", TRUE, 301);
	exit();
}

if (isset($_POST['showAllClasses'])) {
	header("Location: ../PHP/showAllClasses.php", TRUE, 301);
	exit();
}

if (isset($_POST['deleteRow'])) {
	$_SESSION['display'] = 0;
	header("Location: ../PHP/deleteRow.php", TRUE, 301);
	exit();
}

?>