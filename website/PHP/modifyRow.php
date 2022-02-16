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
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="author" content="Brais Cuns Varela (MurkyCuns)">
	<meta name="description" content="Murky Studios Database">
	<link rel="stylesheet" href="../CSS/modifyRow-styles.css">
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
						<li class="nav-menu-item"><a class="current" class="nav-menu-item" href="../HTML/index.php"></a></li>
						<li class="nav-menu-item"><a class="nav-menu-item" href="../HTML/addTable.php"></a></li>
						<li class="nav-menu-item"><a class="nav-menu-item" href="../HTML/contact.php"></a></li>
					</ul>
				</nav>
			</div>
			<div id="session-container">
				<?php 
					if ($_SESSION['username']) {
						echo "<nav>
								<div id='login-container'>Usuario:
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['username'] ."</a></span>
								<div id='login-container'>Base de Datos: 
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['database'] ."</a></span>
								</div>
							</nav>";
					} else {
						echo "<nav>
								<div id='login-container'>
								<span class='login-access'><a class='login-access' href='../HTML/index.php'>Iniciar Sesión</a></span>
								</div>
							</nav>";
					}
				?>
			</div>
		</header>
		<div id="main-container">
			<?php

				if ($_SESSION['display'] == 0) {
					
					echo "<form action='../PHP/modifyRow.php' method='POST' id='main-form-container'>
							<div class='form-input-quote'>Indica el <span class='selectedSite'>Sitio Web o App</span> que quieres modificar:</div>
							<br>
							<input type='text' name='selectedSite' class='form-input-col' placeholder='Modificar: Sitio Web o APP'>

							<input type='submit' name='send-site-button' value='Consultar' id='send-cols-button'>
							<br>
							<input type='submit' name='back-button' value='Volver atrás' id='send-back-button'>
						</form>";

					if (isset($_POST['send-site-button'])) {
						$_SESSION['selectedSite'] = $_POST['selectedSite'];
						$_SESSION['display'] = 1;
						header("Location: ../PHP/modifyRow.php", TRUE, 301);
						exit();
					}

					if (isset($_POST['back-button'])) {
						$_SESSION['display'] = 0;
						header("Location: ../PHP/options.php", TRUE, 301);
						exit();
					}

				} elseif ($_SESSION['display'] == 1) {

					mysqli_select_db($MurkyConnection, $_SESSION['database']);
					$select_query = "SELECT * FROM murkypasswords WHERE Site = '".$_SESSION['selectedSite']."';";

					$select_result = mysqli_query($MurkyConnection, $select_query);


					if ($select_result) {
						echo "<div id='tableName-container'>Contraseña/s de: <span class='selectedSite'>". $_SESSION['selectedSite'] ."</span></div>";
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

		    			echo "<div class='form-input-quote'>¿Quieres modificar este registro?";

						echo "<form action='../PHP/modifyRow.php' method='POST'>";

						echo "<div id='confirmButtonContainer'>";
							echo "<input type='submit' class='confirmButton' name='confirmButton' value='Si'>";
							echo "<input type='submit' class='denyButton' name='denyButton' value='No'>";
						echo "</div>";

						echo "</form></div>";

						if (isset($_POST['confirmButton'])) {
							$_SESSION['display'] = 2;		
							header("Location: ../PHP/modifyRow.php", TRUE, 301);
							exit();
						}

						if (isset($_POST['denyButton'])) {
							$_SESSION['display'] = 0;		
							header("Location: ../PHP/options.php", TRUE, 301);
							exit();
						}
		
			    	}
			    } elseif ($_SESSION['display'] == 2) {

					echo "<div class='form-input-quote'>Introduzca los campos a modificar:</div>";

					echo "<form action='../PHP/modifyRow.php' method='POST' id='newDataForm'>";

					mysqli_select_db($MurkyConnection, $_SESSION['database']);
					$select_query = "SELECT * FROM murkypasswords;";

					$select_result = mysqli_query($MurkyConnection, $select_query);

					if ($select_result) {
						echo "<table id='newDataTable'>";
						echo "<tr class='column-row'>";
				    	echo "<th class='column-field'>Sitio Web o App</th>";
				    	echo "<th class='column-field'>Email</th>";
				    	echo "<th class='column-field'>Usuario</th>";
				    	echo "<th class='column-field'>Contraseña</th>";
				    	echo "<th class='column-field'>Grupo Asociado</th>";
				    	echo "</tr>";

				    	$countColumns_query = "

						SELECT count(*)
						FROM information_schema.columns
						WHERE  table_name = 'murkypasswords'
						AND table_schema = '".$_SESSION['database']."'"

						;

				    	for ($i=0; $i < 1; $i++) { 
				    		echo "<tr>";
				    		$countColumns_result = mysqli_query($MurkyConnection, $countColumns_query);
							$fila = $countColumns_result->fetch_row();
	                			
				    		for ($j=1; $j <= $fila[0]; $j++) {
				    			echo "<td><input type='text' name='newPasswords".$j."' class='newDataInput'></td>";
				    		}
				    		echo "</tr>";
				    	}		
				    		echo "</table>";
				    		
					} else {
						printf("Error: %s\n", mysqli_error($UserDBConection));
					}

					echo "<input type='submit' name='sendNewPasswords' value='Modificar Datos' class='button'>";
					echo "<br><br>";
					echo "<input type='submit' name='backToTables' value='Volver atrás' class='button'>";
					echo "</form>";

					if (isset($_POST['sendNewPasswords'])) {

						$countColumns_query = "

						SELECT count(*)
						FROM information_schema.columns
						WHERE  table_name = 'murkypasswords'
						AND table_schema = '".$_SESSION['database']."'"

						;

				    	$countColumns_result = mysqli_query($MurkyConnection, $countColumns_query);
						$fila = $countColumns_result->fetch_row();

				    	$_POST['newPasswords'.'4'] = base64_encode($_POST['newPasswords'.'4']);
				    	$insert_query = "UPDATE murkypasswords SET Site = '" .$_POST['newPasswords'."1"]. "', Email = '" .$_POST['newPasswords'."2"]. "', Username = '" .$_POST['newPasswords'."3"]. "', Passwd = '" .$_POST['newPasswords'."4"]. "', Class = '" .$_POST['newPasswords'."5"]. "';";

				    	$insert_result = mysqli_query($MurkyConnection, $insert_query);

				    	$_SESSION['display'] = 3;
				    	header("Location: ../PHP/modifyRow.php", TRUE, 301);
						exit();
			    		
					}

					if (isset($_POST['backToTables'])) {
						$_SESSION['display'] = 0;
						header("Location: ../PHP/options.php", TRUE, 301);
						exit();
					}

			    } elseif ($_SESSION['display'] == 3) {
			    	echo "<div class='form-input-quote'>El registro indicado se ha modificado.";
			    	echo "<form action='../PHP/modifyRow.php' method='POST' id='newDataForm'>";
			    	echo "<input type='submit' name='backToTables' value='Volver atrás' class='button'>";
					echo "</form>";

					if (isset($_POST['backToTables'])) {
						$_SESSION['display'] = 0;
						header("Location: ../PHP/options.php", TRUE, 301);
						exit();
					}
			    }

			?>

		</div>

		<footer id="footer-container">
			<div id="footer-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="footer-logo">
			</div>
		</footer>

	</div>
</body>
</html>