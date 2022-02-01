<?php

	session_start();

 	if (isset($_POST['username']) and isset($_POST['database']) and isset($_POST['password']) and isset($_POST['hostname']) and isset($_POST['port'])) {
 		$_SESSION['username'] = $_POST['username'];
 		$_SESSION['database'] = $_POST['database'];
 		$_SESSION['password'] = $_POST['password'];
 		$_SESSION['hostname'] = $_POST['hostname'];
 		$_SESSION['port'] = $_POST['port'];
 	}

	function MurkySQLConnection($MurkyDBUsername, $MurkyDB, $MurkyDBPassword, $MurkyDBHost, $MurkyDBPort) {

		$MurkyDBConection = mysqli_connect($MurkyDBHost.':'.$MurkyDBPort, $MurkyDBUsername, $MurkyDBPassword, $MurkyDB);

	}

	MurkySQLConnection($_SESSION['username'], $_SESSION['database'], $_SESSION['password'], $_SESSION['hostname'], $_SESSION['port']);

?>

<!DOCTYPE html>
<html lang="e">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="author" content="Brais Cuns Varela (MurkyCuns)">
	<meta name="description" content="Murky Studios Database">
	<link rel="stylesheet" href="../CSS/options-styles.css">
	<title>Inicio - Project: WIRENET</title>
</head>
<body>
	<div class="grid-container">
			<header>
			<div id="header-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="header-logo">
			</div>
			<div id="nav-container">
				<nav id="nav-menu">
					<ul id="nav-menu-list">
						<li class="nav-menu-item"></li>
						<li class="nav-menu-item"></li>
						<li class="nav-menu-item"></li>
					</ul>
				</nav>
			</div>
			<div id="session-container">
				<?php 
					if ($_SESSION['username']) {
						echo "<nav>
								<div id='login-container'>Usuario: 
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['username'] ."</a></span>
								</div>
								<div id='login-container'>Base de Datos: 
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['database'] ."</a></span>
								</div>
							</nav>";
					} else {
					}
				?>
			</div>
		</header>
		<div id="main-container">
			<form action='../PHP/redirect.php' method='POST'>
				<div id='new-table-option-container'>
					<input type='submit' class='option-quote' name='addPassword' value="Nueva contraseña">
					<br>
					<input type='submit' class='option-quote' name='showAllPasswords' value="Mostrar todas las contraseñas">

					<hr class="option-separator">
					<br>
				</div>
				<div id='new-table-option-container-2'>
					<span class="label-quote">Filtrado de campos indicando:</span>
				</div>
				<div id='new-table-option-container-2'>
					<input type='submit' class='option-quote' name='showAllPasswords' value="	-> Sitios Web o Aplicaciones">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Correos Electrónicos">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Nombres de Usuario">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Grupos Asociados">
				</div>
				<div id='new-table-option-container'><hr class="option-separator"></div>
				<div id='new-table-option-container-3'>
					<span class="label-quote">Listado de columnas disponibles:</span>
				</div>
				<div id='new-table-option-container-3'>
					<input type='submit' class='option-quote' name='showAllPasswords' value="	-> Sitios Web o Aplicaciones">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Correos Electrónicos">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Nombres de Usuario">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Grupos Asociados">
				</div>
				<div id='new-table-option-container'><hr class="option-separator"></div>
				<div id='new-table-option-container-2'>
					<span class="label-quote">Modificación de registros:</span>
				</div>
				<div id='new-table-option-container-2'>
					<input type='submit' class='option-quote' name='showAllPasswords' value="	-> Eliminar un registro">
					<br>
					<input type='submit' class='option-quote' name='showRelatedToSite' value="	-> Modificar un registro">
				</div>

				</div>
				<div id='new-table-option-container'><hr class="option-separator"></div>

				<div id='new-table-option-container'>
					<input type='submit' class='option-quote' name='addPassword' value="Modificar la contraseña maestra">
					<br>
					<input type='submit' class='option-quote' name='addPassword' value="Cambiar credenciales de sesión">
				</div>
				
			</form>
		</div>
		<footer id="footer-container">
			<div id="footer-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="footer-logo">
			</div>
		</footer>
	</div>
</body>