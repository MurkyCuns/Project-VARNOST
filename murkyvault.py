import mysql.connector
import base64

print("Bienvenido al gestor de contraseñas de MurkyCuns. El MurkyVault 1.0")
MasterPassword = "passwd"
checkMasterPassword = input("Porfavor, introduzca la clave maestra para entrar al gestor de contraseñas: ")

def encodingPassword(passToEncode):
	encodedPassword = base64.b64encode(passToEncode.encode('utf-8'))
	encodingPassword.variable = encodedPassword

def decodingPassword(passToDecode):
	decodedPassword  = base64.b64decode(passToDecode + '=' * (-len(passToDecode) % 4))
	decodingPassword.variable = decodedPassword

def decodingRow(rowToDecode):
	decodingPassword(rowToDecode)
	decodedMaster = decodingPassword.variable
	decodedResult = decodedMaster.decode('utf-8')
	decodingRow.variable = decodedResult


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
		newUsername = input("Introduzca el nombre de usuario para asociar con este sitio web o aplicación: ")
		newPassword = input("Introduzca la nueva contraseña para este sitio web o aplicación: ")

		if (newPlace and newEmail and newUsername and newPassword):
			print("Todos los parámetros se han introducido correctamente!")

			encodingPassword(newPassword)

			# Query de introducción de los valores pasados por pantalla.
			insertContraseña = ("INSERT INTO murkypasswords (Site, Email, Username, Passwd) VALUES (%s, %s, %s, %s)", (newPlace, newEmail, newUsername, encodingPassword.variable))
			
			# Ejecución y comprobación de que los valores hayan entrado a la DB.
			dbcursor.execute( * insertContraseña)
			MurkyDBConnection.commit()

			print(dbcursor.rowcount, "nueva fila introducida en la tabla de contraseñas")

		else:
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

	def showAllPasswords():
		print("Ha elegido la opción 2. Consultar todas las contraseñas.")

		showTable = "SELECT * FROM murkypasswords"
		dbcursor.execute(showTable)
		resultado = dbcursor.fetchall()

		if resultado:
			for fila in resultado:

				decodingRow(fila[3])

				print("")
				print("-----------------------")
				print("Sitio =", fila[0], )
				print("Email =", fila[1])
				print("Usuario = ", fila[2])
				print("Contraseña =", decodingRow.variable)
				print("-----------------------")
				print("")

		else:
			print("No se encuentran contraseñas guardadas en la Base de Datos")


	def showRelatedToSite():
		print("Ha elegido la opción 3. Consultar la contraseña de un sitio web o aplicación.")

		customPlace = input("¿De qué sitio web o aplicación desea conocer la contraseña? ")

		if (customPlace):
			showTable = "SELECT * FROM murkypasswords WHERE Site = %s"
			dbcursor.execute(showTable, (customPlace,))
			resultado = dbcursor.fetchall()

			if resultado:
				for fila in resultado:

					decodingRow(fila[3])

					print("")
					print("-----------------------")
					print("Sitio =", fila[0], )
					print("Email =", fila[1])
					print("Usuario= ", fila[2])
					print("Contraseña= ", decodingRow.variable)
					print("-----------------------")
					print("")

			else:
				print("No se han encontrado resultados para ese Sitio o Aplicación")

		else:
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

	def showRelatedToEmail():
		print("Ha elegido la opción 4. Consultar todas las contraseñas asociadas a un correo electrónico.")

		customEmail = input("¿De qué dirección de email quieres conocer la contraseñas? ")

		if (customEmail):
			showTable = "SELECT * FROM murkypasswords WHERE Email = %s"
			dbcursor.execute(showTable, (customEmail,))
			resultado = dbcursor.fetchall()

			if resultado:
				for fila in resultado:

					decodingRow(fila[3])

					print("")
					print("-----------------------")
					print("Sitio =", fila[0], )
					print("Email =", fila[1])
					print("Usuario= ", fila[2])
					print("Contraseña= ", decodingRow.variable)
					print("-----------------------")
					print("")

			else:
				print("No se han encontrado resultados asociados a esta dirección de correo electrónica.")

		else:
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

	def showRelatedToUsername():
		print("Ha elegido la opción 5. Consultar todas las contraseñas asociadas a un Nombre de Usuario")

		customUsername = input("¿De qué Nombre de Usuario quieres conocer la contraseñas? ")

		if (customUsername):
			showTable = "SELECT * FROM murkypasswords WHERE Username = %s"
			dbcursor.execute(showTable, (customUsername,))
			resultado = dbcursor.fetchall()

			if resultado:
				for fila in resultado:

					decodingRow(fila[3])
					
					print("")
					print("-----------------------")
					print("Sitio =", fila[0], )
					print("Email =", fila[1])
					print("Usuario= ", fila[2])
					print("Contraseña= ", decodingRow.variable)
					print("-----------------------")
					print("")

			else:
				print("No se han encontrado resultados asociados a este Nombre de Usuario")

		else:
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")
	# Mensaje al usuario
	if (MurkyDBConnection):
		print("Se ha conectado correctamente a la Base de Datos!")
		print("")
		while True:

			print("""
				   a) Ingresar una nueva contraseña.
				   b) Consultar todas las contraseñas existentes en la Base de Datos.
				   c) Consultar la contraseña de un sitio web o aplicación.
				   d) Consultar todos los sitios web o aplicaciones asociadas a un correo electrónico.
				   e) Consultar todos los sitios web o aplicaciones asociadas a un nombre de usuario.
				   f) Salir
				   """)

			option = input("Escoja la opción que desee utilizar: ")
			if (option == "a" or option == "A"):
				addPassword()
				break
			if (option == "b" or option == "B"):
				showAllPasswords()
				break
			if (option == "c" or option == "C"):
				showRelatedToSite()
				break
			if (option == "d" or option == "D"):
				showRelatedToEmail()
				break
			if (option == "e" or option == "E"):
				showRelatedToUsername()
				break
			if (option == "f" or option == "F"):
				break
			if (option != ""):
				print("No se ha elegido ninguna opción correcta. Seleccione una opción de las mostradas en el menú.")			
		
	else:
		print("No se ha podido conectar correctamente a la Base de Datos...")
else:
	print("Contraseña incorrecta...")
	exit()

