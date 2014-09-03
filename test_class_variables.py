from persistent import Persistent

class Test_variables(Persistent):

	def __init__(self):
	
		connection, root = self.connect_ZODB()
		
		try: 
			self.catalogue = root.catalogue
		except:
			self.catalogue = {}
			
		connection.close()
			
		
	def connect_ZODB(self):

		#import persistent
		from ZODB import FileStorage, DB
		storage = FileStorage.FileStorage('mydatabase.fs')
		db = DB(storage)
		connection = db.open()
		root = connection.root()
		
		# print ( "Lo que hay en root: ", root.items())
		# print type(root)
		
		
		# if not root.catalogue:
			# root.catalogue = {}
			# for job in self.catalogue.keys():
				# print job, self.catalogue[job]
				# root.catalogue[job] = self.catalogue[job]
		# else:
			# for job in self.catalogue.keys():
				# root.catalogue[job] = self.catalogue[job]
			
			
		# print("Variable catalogo de la clase " ,self.catalogue.keys())	
		
		# print("Diccionario ZODB " , root.catalogue)
		
		# print type(root)
		# print type(root.catalogue)
			
		# import transaction
		# transaction.commit()
		# connection.close()
			
		return connection, root
		
	def add_job(self, position, gross_salary):
	
		if position in self.catalogue:
			print "La posicion ya existe"
			seguir = raw_input("Quiere modificar el salario? (S/N) ")
			if seguir == "y":
				self.catalogue[position] = gross_salary
				print "Salario actualizado"
			else:
				print "Ok"
		else:
			self.catalogue[position] = gross_salary
		
		#opens a connection to ZODB to make the changes permament
		connection, root = connect_ZODB()
		
		root.catalogue = self.catalogue
		
		import transaction
		transaction.commit()
		connection.close()
			
			
if __name__ == "__main__":

	catalogue = Test_variables()
	
	print catalogue.catalogue
	
	catalogue.add_job('juerguista',20000)
	catalogue.add_job('secretario', 15000)
	catalogue.add_job('zorro', 150000000)
	
	print catalogue.catalogue
	
	# connection, root = catalogue.connect_ZODB()
	
	# import transaction
	# transaction.commit()
	
	
	
	
	# print("Diccionario root fuera de la funcion " , root.catalogue.items())
	
	
	
					
