import mysql.connector

print("Bienvenido al gestor de contraseñas de MurkyCuns. El MurkyVault 1.0")
MasterPassword = "password"
checkMasterPassword = input("Porfavor, introduzca la clave maestra para entrar al gestor de contraseñas: ")

if (MasterPassword == checkMasterPassword):
	print("Contraseña correcta!")
	print("Se procederá a realizar la conexión a la base de datos.")
	print("Introduzca los siguientes valores: ")

	# Paso de variables por teclado.
	MurkyDB = input("Introduzca el nombre de la Base de Datos: ")
	MurkyDBHost = input("Introduzca el nombre del Host de la Base de Datos: ")
	MurkyDBUsername = input("Introduzca el nombre de Usuario de la Base de Datos: ")
	MurkyDBPassword = input("Introduzca la contraseña de la Base de Datos: ")

	# Conexión a la Base de Datos.
	MurkyDBConnection = mysql.connector.connect(
										user=MurkyDBUsername,
										password=MurkyDBPassword,
										host=MurkyDBHost,
										database=MurkyDB,
										)

	dbcursor = MurkyDBConnection.cursor()

	def addPassword():
		print("Ha elegido la opción 1. Ingresar una nueva contraseña.")

		newPlace = input("Introduzca el sitio web o aplicación al que desee añadir una contraseña: ")
		newEmail = input("Introduzca el email para asociar con este sitio web o aplicación: ")
		newPassword = input("Introduzca la nueva contraseña para este sitio web o aplicación: ")

		if (newPlace and newEmail and newPassword):
			print("Todos los parámetros se han introducido correctamente!")
			insertContraseña = "INSERT INTO murkypasswords (Site, Email, Passwd) VALUES (%s, %s, %s)"
			valoresInsert = (newPlace, newEmail, newPassword)
			dbcursor.execute(insertContraseña, valoresInsert)

			MurkyDBConnection.commit()

			print("Se han insertado correctamente las columnas a la Base de Datos!")

		else:
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

	# Mensaje al usua
	if (MurkyDBConnection):
		print("Se ha conectado correctamente a la Base de Datos!")
		print("")
		while True:

			print("""
				   a) Ingresar una nueva contraseña.
				   b) Consultar la contraseña de un sitio web o aplicación.
				   c) Consultar todos los sitios web o aplicaciones asociadas a un correo electrónico.
				   d) Salir
				   """)

			option = input("Escoja la opción que desee utilizar: ")
			if option == "a" or "A":
				addPassword()
				break
			if option == "2":
				print("Ha elegido la opción 2. Consultar la contraseña de un sitio web o aplicación.")
			if option == "3":
				print("Ha elegido la opción 3. Consultar todos los sitios web o aplicaciones asociadas a un correo electrónico.")
			if option == "4":
				print("Ha elegido la opción 4. Salir de la aplicación.")
			if option != "":
				print("No se ha elegido ninguna opción correcta. Seleccione una opción de las mostradas en el menú.")			
		
	else:
		print("No se ha podido conectar correctamente a la Base de Datos...")
else:
	print("Contraseña incorrecta...")
	exit()

