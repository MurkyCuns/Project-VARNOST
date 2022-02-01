<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="author" content="Brais Cuns Varela (MurkyCuns)">
	<meta name="description" content="Murky Studios Database">
	<link rel="stylesheet" href="../CSS/index-styles.css">
	<title>Inicio - MurkyVault</title>
</head>
<body>
	<div class="grid-container">
			<header>
			<div id="header-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="header-logo">
			</div>
			<div id="session-container">
				<?php 
					if (isset($_SESSION['username'])) {
						echo "<nav>
								<div id='login-container'>Nombre de Usuario:
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['username'] ."</a></span>
								</div>
							</nav>";
						echo "<nav>
								<div id='login-container'>Base de Datos:
								<span class='login-user'><a class='login-user' href='../HTML/profile.php'>". $_SESSION['database'] ."</a></span>
								</div>
							</nav>";
					} else {
						echo "<nav>
								<div id='login-container'>
								<span class='login-access'><a class='login-access' href='../HTML/index.php''>Iniciar Sesión</a></span>
							</nav>";
					}
				?>
			</div>
		</header>
		<div id="main-logo-container">
			<img src="../images/index/Murky Studios Database.png" alt="" id="main-logo">
		</div>
		<div id="main-login-form-container">
			<form id="main-login-form" action="../PHP/options.php" method="POST">
				<input type="text" id="username" name="username" placeholder="Nombre de Usuario">
				<br>
				<input type="text" id="database" name="database" placeholder="Base de Datos">
				<br>
				<input type="password" id="password" name="password" placeholder="Contraseña">
				<br>
				<input type="text" id="hostname" name="hostname" placeholder="Dirección de Host">
				<br>
				<input type="text" id="port" name="port" placeholder="Puerto">
				<br>
				<input type="submit" id="send-info-button" name="send-info-button" value="Iniciar Sesión">
			</form>
			<?php 
				if (isset($_POST['send-info-button'])) {
					if ($_POST['username'] == '' or $_POST['database'] == '' or $_POST['password'] == '' or $_POST['hostname'] == '' or $_POST['port'] == '') {
						echo '<div class="errorLog">Debe rellenar todos los campos para iniciar sesión.</div>';
					}
				}
			?>
		</div>
		<footer id="footer-container"
		>
			<div id="footer-logo-container">
				<img src="../images/index/header-logo.png" alt="" id="footer-logo">
			</div>
		</footer>
	</div>
</body>
</html>