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

		mysqli_select_db($MurkyDBConection, $MurkyDB);

		return $MurkyDBConection;
	}

	$MurkyConnection = MurkySQLConnection($_SESSION['username'], $_SESSION['database'], $_SESSION['password'], $_SESSION['hostname'], $_SESSION['port']);

?>

<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="author" content="Brais Cuns Varela (MurkyCuns)">
	<meta name="description" content="Murky Studios Database">
	<link rel="stylesheet" href="../CSS/showAllPasswords-styles.css">
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
		<?php
			echo "<div id='main-container'>";
				$select_query = "SELECT * FROM murkypasswords;";

					$select_result = mysqli_query($MurkyConnection, $select_query);


					if ($select_result) {
						echo "<div id='tableName-container'>Todas las contraseñas</div>";
						echo "<hr class='separator'>";
						echo "<table id='main-table'>";
						echo "<tr>
							<td class='column-field'>Web o App</td>
							<td class='column-field'>Correo Electrónico</td>
							<td class='column-field'>Usuario</td>
							<td class='column-field'>Contraseña</td>
							<td class='column-field'>Grupo Asociado</td>
						</tr>";

		    				while ($rowArray = mysqli_fetch_array($select_result)) {
		    					echo "<tr class='row-row'>";

		    					for ($i=0; $i <= 4; $i++) {
		    						if ($i == 3) {
		    							echo "<td class='row-field'>".base64_decode($rowArray[$i])."</td>";
		    						} else {
		    							echo "<td class='row-field'>".$rowArray[$i]."</td>";
		    						}
		    					}
		    					echo "</tr>";

		    				}
		    				
		    			echo "</table>";
		    			echo "<hr class='separator'>";
		    			echo "</div>";
					} else {
						printf("Error: %s\n", mysqli_error($MurkyConnection));
					}
		?>

		<footer id="footer-container">
			<div id="footer-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="footer-logo">
			</div>
		</footer>

	</div>
</body>
</html>