import mysql.connector
import base64
from prettytable import PrettyTable
import getpass
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()


print("Bienvenido al gestor de contraseñas de MurkyCuns. El MurkyVault 1.0")
MasterPassword = "passwd"
# checkMasterPassword = getpass.getpass("Porfavor, introduzca la clave maestra para entrar al gestor de contraseñas: ")
checkMasterPassword = "passwd"

printTable = PrettyTable()

def showSelectedMenu(option):
	while True:

		if option:
			pass
		else:
			option = input("Escoja la opción que desee utilizar: ")

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
	print()
	print("Se procederá a realizar la conexión a la base de datos.")
	print()
	print("Introduzca los siguientes valores: ")
	print()

	# Paso de variables por teclado.
	MurkyDB = input("Introduzca el nombre de la Base de Datos: ")
	MurkyDBHost = input("Introduzca el nombre del Host de la Base de Datos: ")
	MurkyDBUsername = input("Introduzca el nombre de Usuario de la Base de Datos: ")
	MurkyDBPassword = getpass.getpass("Introduzca la contraseña de la Base de Datos: ")

	# Conexión a la Base de Datos.
	MurkyDBConnection = mysql.connector.connect(
										user=MurkyDBUsername,
										password=MurkyDBPassword,
										host=MurkyDBHost,
										database=MurkyDB,									
										)

	dbcursor = MurkyDBConnection.cursor()

	def addPassword():
		print()
		print("Ha elegido la opción 1. Ingresar una nueva contraseña.")
		print()

		newPlace = input("Introduzca el sitio web o aplicación al que desee añadir una contraseña: ")
		newEmail = input("Introduzca el email para asociar con este sitio web o aplicación: ")
		newUsername = input("Introduzca el nombre de usuario para asociar con este sitio web o aplicación: ")
		newPassword = getpass.getpass("Introduzca la nueva contraseña para este sitio web o aplicación: ")

		if (newPlace and newEmail and newUsername and newPassword):
			print()
			print("Todos los parámetros se han introducido correctamente!")

			encodingPassword(newPassword)

			# Query de introducción de los valores pasados por pantalla.
			insertContraseña = ("INSERT INTO murkypasswords (Site, Email, Username, Passwd) VALUES (%s, %s, %s, %s)", (newPlace, newEmail, newUsername, encodingPassword.variable))
			
			# Ejecución y comprobación de que los valores hayan entrado a la DB.
			dbcursor.execute( * insertContraseña)
			MurkyDBConnection.commit()
			print()

			print(dbcursor.rowcount, "nueva fila introducida en la tabla de contraseñas")

			print()

			anotherTry = input("Quieres introducir una nueva contraseña para un Sitio Web o una Aplicación?	Si / No: ")

			if (anotherTry == "Si" or anotherTry == "si"):
				clearConsole()
				showSelectedMenu("1")

			elif (anotherTry == "No" or anotherTry == "no"):
				anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

				if (anotherOption == "Si" or anotherOption == "si"):
					clearConsole()
					showMenu()

				else:
					showSelectedMenu("0")

		else:
			print()
			print("No se han introducido todos los parámetros, no se admiten entradas vacías...")

	def showAllPasswords():
		print()
		print("Ha elegido la opción 2. Consultar todas las contraseñas.")
		print()

		showTable = "SELECT * FROM murkypasswords"
		dbcursor.execute(showTable)
		resultado = dbcursor.fetchall()

		if resultado:

			printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"]

			for fila in resultado:

				decodingRow(fila[3])

				printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

			print(printTable)

			printTable.clear_rows()

			anotherOption = input("Quieres escoger otra opción del menú de selección?	Si / No: ")

			if (anotherOption == "Si" or anotherOption == "si"):
				clearConsole()
				showMenu()

			else:
				showSelectedMenu("0")

		else:
			print()
			print("No se encuentran contraseñas guardadas en la Base de Datos")


	def showRelatedToSite():
		print()
		print("Ha elegido la opción 3. Consultar la contraseña de un sitio web o aplicación.")
		print()

		customPlace = input("¿De qué sitio web o aplicación desea conocer la contraseña? ")

		if (customPlace):
			showTable = "SELECT * FROM murkypasswords WHERE Site = %s"
			dbcursor.execute(showTable, (customPlace,))
			resultado = dbcursor.fetchall()

			if resultado:

				printTable.field_names = ["Web o Aplicación", "Correo Electrónico", "Nombre de Usuario", "Contraseña"] 

				for fila in resultado:

					decodingRow(fila[3])

					printTable.add_row([fila[0], fila[1], fila[2], decodingRow.variable])

				print(printTable)

				printTable.clear_rows()

				print()

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

	def showRelatedToEmail():
		print()
		print("Ha elegido la opción 4. Consultar todas las contraseñas asociadas a un correo electrónico.")
		print()

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

	def showRelatedToUsername():
		print()
		print("Ha elegido la opción 5. Consultar todas las contraseñas asociadas a un Nombre de Usuario")
		print()

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

	def deleteRow():
		print()
		print("Ha elegido la opción 6. Eliminar una contraseña de un sitio Web o Aplicación")
		print()

		customPlace = input("¿De qué Sitio Web o Aplicación quieres eliminar la contraseña? ")

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

				confirmDelete = input("Estás seguro de que quieres eliminar esta fila de la tabla de contraseñas?	Si / No: ")

				if (confirmDelete == "Si" or confirmDelete == "si"):
					deleteQuery = "DELETE FROM murkypasswords WHERE Site = %s"
					dbcursor.execute(deleteQuery, (customPlace,))
					MurkyDBConnection.commit()

					print()
					print("La contraseña del Sitio Web o Aplicación: '" + customPlace + "', se ha eliminado correctamente.")
					print()

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
				else:
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

	def modifyRow():
		print()
		print("Ha elegido la opción 6. Modificar el registro de un sitio Web o Aplicación")
		print()

		customPlace = input("¿De qué Sitio Web o Aplicación quieres modificar el registro? ")

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

				confirmDelete = input("Estás seguro de que quieres modificar este registro de la tabla de contraseñas?	Si / No: ")

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
			
					# Ejecución y comprobación de que los valores hayan entrado a la DB.
					dbcursor.execute( * modifyQuery)
					MurkyDBConnection.commit()

					print()
					print("El registro del Sitio Web o Aplicación: '" + customPlace + "', se ha modificado correctamente.")
					print()

					anotherTry = input("Quieres modificar el registro de otro Sitio Web o Aplicación?	Si / No: ")

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
				else:
					anotherTry = input("Quieres eliminar la contraseña de otro Sitio Web o Aplicación?	Si / No: ")

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

			

	# Mensaje al usuario
	if (MurkyDBConnection):
		clearConsole()

		def showMenu():
			while True:
				print("""
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

0) Salir
					   """)

				option = input("Escoja la opción que desee utilizar: ")

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
					print("No se ha elegido ninguna opción correcta. Seleccione una opción de las mostradas en el menú.")
					print()

		showMenu()				
		
	else:
		print()
		print("No se ha podido conectar correctamente a la Base de Datos...")
else:
	print()
	print("Contraseña incorrecta...")
	exit()