import mysql.connector
import base64
from prettytable import PrettyTable
import getpass
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()


print("Bienvenido al gestor de contraseñas de MurkyCuns. El MurkyVault 1.0")

print()
print("Intentando conexión con la Base de Datos de MySQL...")
print()
print("Introduzca los siguientes valores: ")
print()

# Paso de variables relacionadas con la conexión a la Base de Datos por teclado:
MurkyDB = input("Introduzca el Nombre de la Base de Datos: ")
MurkyDBHost = input("Introduzca la direción Host de la Base de Datos: ")
MurkyDBUsername = input("Introduzca el Nombre de Usuario de la Base de Datos: ")
MurkyDBPassword = getpass.getpass("Introduzca la Contraseña de la Base de Datos: ")

# Conexión a la Base de Datos:
MurkyDBConnection = mysql.connector.connect(
									user=MurkyDBUsername,
									password=MurkyDBPassword,
									host=MurkyDBHost,
									database=MurkyDB,									
									)

dbcursor = MurkyDBConnection.cursor()
clearConsole

if MurkyDBConnection:

	# Comprobación de la existencia de las tablas necesarias para realizar las operaciones de la aplicación:
	createMasterPassTable = "CREATE TABLE IF NOT EXISTS masterpass (masterpass varchar(255))"
	dbcursor.execute(createMasterPassTable)

	createStoreTable = "CREATE TABLE IF NOT EXISTS murkypasswords (Site varchar(255), Email varchar(255), Username varchar(255), Passwd varchar(255))"
	dbcursor.execute(createStoreTable)

	# Comprobación de la existencia de la Clave Maestra dentro de la tabla destinada a su almacenamiento:
	checkMasterPass = "SELECT * FROM masterpass"
	dbcursor.execute(checkMasterPass)
	checkMasterPassResult = dbcursor.fetchone()

	# Si no existe esta clave, se pedirá al usuario que la indique, mediante un paso por teclado y se almacenará en la tabla indicada:
	if not checkMasterPassResult:
		insertMasterPassQuery = "INSERT INTO masterpass (masterpass) VALUES (%s)"
		insertMasterPass = getpass.getpass("No se ha introducido ningunha clave maestra. Por favor, introduce una a continuación: ")
		masterPassToInsert = (insertMasterPass,)
		dbcursor.execute(insertMasterPassQuery, masterPassToInsert)
		MurkyDBConnection.commit()

	else:
		print()
	
	# Paso de contraseña por teclado:
	checkMasterPassword = getpass.getpass("Porfavor, introduzca la clave maestra para entrar al gestor de contraseñas: ")

	checkMasterPasswordQuery = "SELECT * FROM masterpass;"
	dbcursor.execute(checkMasterPasswordQuery)
	Masterresultado = dbcursor.fetchone()

	for masterPasswordRow in Masterresultado:
		pass
	
	# Definición de un Menú alternativo utilizado para realizar acciones secundarias después de la primera seleccionada en el Menú Principal:
	def showSelectedMenu(option):
		while True:

			if option:
				pass
			else:
				option = input("Escoja la opción que quieres utilizar: ")

			if (option == "1"):
				addPassword()
			if (option == "2"):
				showAllPasswords()
			if (option == "3"):
				showRelatedToSite()
			if (option == "4"):
				showRelatedToEmail()
			if (option == "5"):
				showRelatedToUsername()
			if (option == "6"):
				deleteRow()
			if (option == "7"):
				modifyRow()
			if (option == "0"):
				print()
				print("Gracias por utilizar MurkyVault!")
				print()
				exit()
			if (option != ""):
				print("No se ha elegido ninguna opción correcta. Seleccione una opción de las mostradas en el menú.")

	# Funciones destinadas a encriptar y desencriptar las contraseñas que introduzca el usuario dentro de la Base de Datos.
	# Se encriptan las contraseñas para que estas no sean visibles como texto plano dentro de la Base de Datos y se desencriptarán a la hora de ser consultadas mediante las opciones del menú:
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

	# Se comprueba que la contraseña maestra introducida por el usuario coincide con la contraseña maestra almacenada en la Base de Datos:
	if (checkMasterPassword == masterPasswordRow):

		# Función destinada para agregar nuevas contraseñas a la Base de Datos:
		def addPassword():
			print()
			print("Ha elegido la opción 1. Ingresar una nueva contraseña.")
			print()

			# Se definen variables mediante paso por teclado:
			newPlace = input("Introduzca el sitio web o aplicación al que desee añadir una contraseña: ")
			newEmail = input("Introduzca el email para asociar con este sitio web o aplicación: ")
			newUsername = input("Introduzca el nombre de usuario para asociar con este sitio web o aplicación: ")
			newPassword = getpass.getpass("Introduzca la nueva contraseña para este sitio web o aplicación: ")

			# Se comprueban que todas las variables existen, no se permiten entradas vacías:
			if (newPlace and newEmail and newUsername and newPassword):
				print()
				print("Todos los parámetros se han introducido correctamente!")

				# Si todas las variables se han introducido, la contraseña se encripta llamando a la función destinada a ello:
				encodingPassword(newPassword)

				# Se define la consulta de MySQL con los valores guardados en las variables que ha indicado el usuario:
				insertContraseña = ("INSERT INTO murkypasswords (Site, Email, Username, Passwd) VALUES (%s, %s, %s, %s)", (newPlace, newEmail, newUsername, encodingPassword.variable))
				
				# Ejecución y comprobación de que los valores hayan entrado a la tabla indicada y que esta se actualice:
				dbcursor.execute( * insertContraseña)
				MurkyDBConnection.commit()
				print()

				print(dbcursor.rowcount, "nueva fila introducida en la tabla de contraseñas.")

				print()

				# Si el usuario quiere volver a utilizar esta misma opción, puede realizarlo mediante esta característica, sin volver al menú principal:
				anotherTry = input("Quieres introducir una nueva contraseña para un Sitio Web o una Aplicación?	Si / No: ")

				# En caso positivo, se llamará a la función del Menú Secundario, al cuál se le pasará por parámetro el número de opción del menú que quiere repetir el usuario.
				if (anotherTry == "Si" or anotherTry == "si"):
					clearConsole()
					showSelectedMenu("1")

				# En caso negativo, se le preguntará si quiere utilizar otra opción de las listadas en el menú:
				elif (anotherTry == "No" or anotherTry == "no"):
					anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")
					
					# En caso positivo, se lanzará el menú principal:
					if (anotherOption == "Si" or anotherOption == "si"):
						clearConsole()
						showMenu()

					# En caso negativo, se llamará a la función del Menú Secundario con el paso por parámetro indicado para salir del programa:
					else:
						showSelectedMenu("0")

			else:
				print()
				print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

		# Función destinada a mostrar por pantalla todas las contraseñas almacenadas en la Base de Datos:
		def showAllPasswords():
			print()
			print("Ha elegido la opción 2. Consultar todas las contraseñas.")
			print()

			# Se lanza una consulta global sobre la tabla de contraseñas:
			showTable = "SELECT * FROM murkypasswords"
			dbcursor.execute(showTable)
			resultado = dbcursor.fetchall()

			# Se comprueba que tenga datos en su interior:
			if resultado:

				# Opciones de "styling" del resultado de las consultas mediante tablas:
				printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"]

				for fila in resultado:

					# Se desencriptan los valores que contienen las contraseñas del usuario llamando a la función destinada a ello y se muestran los datos por pantalla:
					decodingRow(fila[3])

					printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

				print(printTable)

				# Se limpian las tablas mostradas previamente. NECESARIO si el usuario quiere realizar nuevas consultas sin cerrar la aplicación:
				printTable.clear_rows()

				print()

				# Repetición de característica. Consultar el comentario de la función addPassword().
				anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

				if (anotherOption == "Si" or anotherOption == "si"):
					clearConsole()
					showMenu()

				else:
					showSelectedMenu("0")

			else:
				print()
				print("No se encuentran contraseñas guardadas en la Base de Datos")


		# Función destinada a mostrar todas las contraseñas que se asocien con un Sitio Web o Aplicación concreto:
		def showRelatedToSite():
			print()
			print("Ha elegido la opción 3. Consultar la contraseña de un sitio web o aplicación.")
			print()

			# Se le pide al usuario que indique el Sitio Web o la Aplicación del que quiere conocer sus contraseñas:
			customPlace = input("¿De qué sitio web o aplicación desea conocer la contraseña? ")

			# Si se ha introducido un Sitio Web o App, se realizará la consulta necesaria para sacar los valores que correspondan con ese lugar:
			if (customPlace):
				showTable = "SELECT * FROM murkypasswords WHERE Site = %s"
				dbcursor.execute(showTable, (customPlace,))
				resultado = dbcursor.fetchall()

				# Si el resultado existe, se estiliza la tabla, se desencripta la contraseña y se muestra por pantalla, al igual que en la función showPasswords():
				if resultado:

					printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"] 

					for fila in resultado:

						decodingRow(fila[3])

						printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

					print(printTable)

					printTable.clear_rows()

					print()

					# Repetición de característica. Consultar el comentario de la función addPassword().
					anotherTry = input("Quieres consultar las contraseñas de otro Sitio Web o Aplicación?	Si / No: ")

					if (anotherTry == "Si" or anotherTry == "si"):
						clearConsole()
						showSelectedMenu("3")

					elif (anotherTry == "No" or anotherTry == "no"):
						anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

						if (anotherOption == "Si" or anotherOption == "si"):
							clearConsole()
							showMenu()

						else:
							showSelectedMenu("0")

				else:
					print()
					print("No se han encontrado resultados para ese Sitio o Aplicación")

			else:
				print()
				print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

		# Función destinada a mostrar todas las contraseñas que se asocien con una cuenta de Correo Electrónico concreto:
		def showRelatedToEmail():
			print()
			print("Ha elegido la opción 4. Consultar todas las contraseñas asociadas a un correo electrónico.")
			print()

			# Al igual que en la función showRelatedToSite() se pide al usuario que introduzaca la Cuenta de Email de la que desea conocer las contraseñas, se realiza la consulta,
			# se estiliza la tabla, se desencriptan las contraseñas y se imprime por pantalla.
			customEmail = input("¿De qué dirección de email quieres conocer la contraseñas? ")

			if (customEmail):
				showTable = "SELECT * FROM murkypasswords WHERE Email = %s"
				dbcursor.execute(showTable, (customEmail,))
				resultado = dbcursor.fetchall()

				if resultado:

					printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"]

					for fila in resultado:

						decodingRow(fila[3])

						printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

					print(printTable)

					printTable.clear_rows()

					print()

					# Repetición de característica. Consultar el comentario de la función addPassword().
					anotherTry = input("Quieres consultar las contraseñas asociadas a otra cuenta de Correo Electrónico?	Si / No: ")

					if (anotherTry == "Si" or anotherTry == "si"):
						clearConsole()
						showSelectedMenu("4")

					elif (anotherTry == "No" or anotherTry == "no"):
						anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

						if (anotherOption == "Si" or anotherOption == "si"):
							clearConsole()
							showMenu()

						else:
							showSelectedMenu("0")

				else:
					print()
					print("No se han encontrado resultados asociados a esta dirección de correo electrónica.")

			else:
				print()
				print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

		# Función destinada a mostrar todas las contraseñas que se asocien con un Nombre de Usuario concreto:
		def showRelatedToUsername():
			print()
			print("Ha elegido la opción 5. Consultar todas las contraseñas asociadas a un Nombre de Usuario")
			print()

			# Al igual que en la función showRelatedToSite() se pide al usuario que introduzaca el Nombre de Usuario del que desea conocer las contraseñas, se realiza la consulta,
			# se estiliza la tabla, se desencriptan las contraseñas y se imprime por pantalla.
			customUsername = input("¿De qué Nombre de Usuario quieres conocer la contraseñas? ")

			if (customUsername):
				showTable = "SELECT * FROM murkypasswords WHERE Username = %s"
				dbcursor.execute(showTable, (customUsername,))
				resultado = dbcursor.fetchall()

				if resultado:

					printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"] 

					for fila in resultado:

						decodingRow(fila[3])
						
						printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

					print(printTable)

					printTable.clear_rows()

					print()

					# Repetición de característica. Consultar el comentario de la función addPassword().
					anotherTry = input("Quieres consultar las contraseñas asociadas a otro Nombre de Usuario?	Si / No: ")

					if (anotherTry == "Si" or anotherTry == "si"):
						clearConsole()
						showSelectedMenu("5")

					elif (anotherTry == "No" or anotherTry == "no"):
						anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

						if (anotherOption == "Si" or anotherOption == "si"):
							clearConsole()
							showMenu()

						else:
							clearConsole()
							showSelectedMenu("0")

				else:
					print()
					print("No se han encontrado resultados asociados a este Nombre de Usuario")

			else:
				print()
				print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

		# Función destinada al Borrado de una fila de contraseñas con sus respectivos campos indicada por el Sitio Web o Aplicación:
		def deleteRow():
			print()
			print("Ha elegido la opción 6. Eliminar una contraseña de un sitio Web o Aplicación")
			print()

			# Se le pide al usuario que indique como identificador principal el Sitio Web o Aplicación del que quiere eliminar sus contraseñas:
			customPlace = input("¿De qué Sitio Web o Aplicación quieres eliminar la contraseña? ")

			if (customPlace):
				showTable = "SELECT * FROM murkypasswords WHERE Site = %s"
				dbcursor.execute(showTable, (customPlace,))
				resultado = dbcursor.fetchall()

				# Si el sitio indicado existe, se mostrará al usuario los campos que este contiene en su interior para que pueda comprobarlos antes de proceder a eliminarlos:
				if resultado:

					print()
					print("El Sitio Web o Aplicación de nombre: '" + customPlace + "' contiene los siguientes campos: ")
					print()

					printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"] 

					for fila in resultado:

						decodingRow(fila[3])

						printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

					print(printTable)

					printTable.clear_rows()

					print()

					# Se le pedirá confirmación adiccional al usuario para evitar posibles borrados accidentales:
					confirmDelete = input("Estás seguro de que quieres eliminar esta fila de la tabla de contraseñas?	Si / No: ")

					# En caso positivo, se lanzará una consulta MySQL para eliminar todos los campos de las filas cuyo Sitio Web o APP sea el indicado por el usuario:
					if (confirmDelete == "Si" or confirmDelete == "si"):
						deleteQuery = "DELETE FROM murkypasswords WHERE Site = %s"
						dbcursor.execute(deleteQuery, (customPlace,))
						MurkyDBConnection.commit()

						print()
						print("La contraseña del Sitio Web o Aplicación: '" + customPlace + "', se ha eliminado correctamente.")
						print()

						# Repetición de característica. Consultar el comentario de la función addPassword().
						anotherTry = input("Quieres eliminar la contraseña de otro Sitio Web o Aplicación?	Si / No: ")

						if (anotherTry == "Si" or anotherTry == "si"):
							clearConsole()
							showSelectedMenu("6")

						elif (anotherTry == "No" or anotherTry == "no"):
							anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

							if (anotherOption == "Si" or anotherOption == "si"):
								clearConsole()
								showMenu()

							else:
								clearConsole()
								showSelectedMenu("0")

					# En caso negativo, se cancelará esta operación y se le brindará al usuario la opción secundaria de escoger otro sitio a eliminar si quiere:
					else:

						# Repetición de característica. Consultar el comentario de la función addPassword().
						anotherTry = input("Quieres eliminar la contraseña de otro Sitio Web o Aplicación?	Si / No: ")

						if (anotherTry == "Si" or anotherTry == "si"):
							clearConsole()
							showSelectedMenu("6")

						elif (anotherTry == "No" or anotherTry == "no"):
							anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

							if (anotherOption == "Si" or anotherOption == "si"):
								clearConsole()
								showMenu()

							else:
								clearConsole()
								showSelectedMenu("0")

		# Función destinada a la modificación de los campos de una fila indicada mediante el Sitio Web o App como identificador:
		def modifyRow():
			print()
			print("Ha elegido la opción 6. Modificar el registro de un sitio Web o Aplicación")
			print()

			customPlace = input("¿De qué Sitio Web o Aplicación quieres modificar el registro? ")

			# Si el sitio indicado existe, se mostrará al usuario los campos que este contiene en su interior para que pueda comprobarlos antes de proceder a modificarlos:
			if (customPlace):
				showTable = "SELECT * FROM murkypasswords WHERE Site = %s"
				dbcursor.execute(showTable, (customPlace,))
				resultado = dbcursor.fetchall()

				if resultado:

					print()
					print("El Sitio Web o Aplicación de nombre: '" + customPlace + "' contiene los siguientes campos: ")
					print()

					printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"] 

					for fila in resultado:

						decodingRow(fila[3])

						printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

					print(printTable)

					printTable.clear_rows()

					print()

					# Se le pedirá confirmación adiccional al usuario para evitar posibles modificaciones accidentales:
					confirmDelete = input("Estás seguro de que quieres modificar este registro de la tabla de contraseñas?	Si / No: ")

					#En caso positivo, se le preguntará por los nuevos valores que quiere introducir en cada campo, se encriptará la contraseña y se actualizarán los valores en la tabla correspondiente:
					if (confirmDelete == "Si" or confirmDelete == "si"):

						print()
						print("Introduzca nuevos valores para los siguientes campos del registro del Sitio Web o Aplicación: '" + customPlace)
						print()

						newPlace = input("Sitio Web o Aplicación: ")
						newEmail = input("Correo Electrónico: ")
						newUsername = input("Nombre de Usuario: ")
						newPassword = getpass.getpass("Contraseña: ")

						encodingPassword(newPassword)

						modifyQuery = ("UPDATE murkypasswords SET Site = %s, Email = %s, Username = %s, Passwd = %s WHERE Site = %s", (newPlace, newEmail, newUsername, encodingPassword.variable, customPlace))
				
						# Ejecución y comprobación de que los valores hayan entrado a la Base de Datos:
						dbcursor.execute( * modifyQuery)
						MurkyDBConnection.commit()

						print()
						print("El registro del Sitio Web o Aplicación: '" + customPlace + "', se ha modificado correctamente.")
						print()

						anotherTry = input("Quieres modificar el registro de otro Sitio Web o Aplicación?	Si / No: ")

						# Repetición de característica. Consultar el comentario de la función addPassword().
						if (anotherTry == "Si" or anotherTry == "si"):
							clearConsole()
							showSelectedMenu("7")

						elif (anotherTry == "No" or anotherTry == "no"):
							anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

							if (anotherOption == "Si" or anotherOption == "si"):
								clearConsole()
								showMenu()

							else:
								clearConsole()
								showSelectedMenu("0")

					# En caso negativo, se cancelará la operación y se le preguntará al usuario si quiere realizar modificaciones en otro Sitio Web o App:
					else:

						# Repetición de característica. Consultar el comentario de la función addPassword().
						anotherTry = input("Quieres modificar el registro de otro Sitio Web o Aplicación?	Si / No: ")

						if (anotherTry == "Si" or anotherTry == "si"):
							clearConsole()
							showSelectedMenu("f")

						elif (anotherTry == "No" or anotherTry == "no"):
							anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

							if (anotherOption == "Si" or anotherOption == "si"):
								clearConsole()
								showMenu()

							else:
								clearConsole()
								showSelectedMenu("0")

				

		# Se comprueba que la contraseña maestra introducida por el usuario coincide con la contraseña maestra almacenada en la Base de Datos:
		if (checkMasterPassword == masterPasswordRow):
			clearConsole()

			# Función destinada a mostrar por pantalla el Menú Principal con las diferentes opciones del usuario:
			def showMenu():
				while True:
					print("""
	-----------------------------------------------------------------------------------

	Bienvenido al Gestor de Contraseñas de MurkyCuns. MurkyVault 1.0.

	-----------------------------------------------------------------------------------
	OPCIONES DE CONSULTA DE TABLAS DE LA BASE DE DATOS DE CONTRASEÑAS DEL USUARIO.
	-----------------------------------------------------------------------------------

	1) Ingresar una nueva contraseña.
	2) Consultar todas las contraseñas existentes en la Base de Datos.
	3) Consultar la contraseña de un Sitio web o Aplicación.
	4) Consultar todos los sitios web o aplicaciones asociadas a un correo electrónico.
	5) Consultar todos los sitios web o aplicaciones asociadas a un nombre de usuario.

	-----------------------------------------------------------------------------------
	OPCIONES DE MODIFICACIÓN DE TABLAS DE LA BASE DE DATOS DE CONTRASEÑAS DEL USUARIO.
	-----------------------------------------------------------------------------------

	6) Eliminar la contraseña de un Sitio Web o Aplicación.
	7) Modificar el registro de un Sitio Web o Aplicación.

	-----------------------------------------------------------------------------------

	0) Salir del Gestor de Contraseñas.

	-----------------------------------------------------------------------------------
						   """)

					option = input("Escoja la opción que quieres utilizar: ")

					if (option == "1"):
						clearConsole()
						addPassword()
					if (option == "2"):
						clearConsole()
						showAllPasswords()
					if (option == "3"):
						clearConsole()
						showRelatedToSite()
					if (option == "4"):
						clearConsole()
						showRelatedToEmail()
					if (option == "5"):
						clearConsole()
						showRelatedToUsername()
					if (option == "6"):
						clearConsole()
						deleteRow()
					if (option == "7"):
						clearConsole()
						modifyRow()
					if (option == "0"):
						clearConsole()
						print()
						print("Gracias por utilizar MurkyVault!")
						print()
						exit()
					if (option != ""):
						print()
						print("No se ha elegido ninguna opción correcta. Selecciona una opción de las mostradas en el menú.")
						print()

			showMenu()				
			
		else:
			print()
			print("La clave maestra introducida no es correcta.")
	else:
		print()
		print("La clave maestra introducida no es correcta.")
		exit()
else:
	print()
	print("No se ha podido realizar la conexión con la Base de Datos.")
	exit()

# EOF