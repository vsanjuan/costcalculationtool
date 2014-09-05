from persistent import Persistent
from ZODB import FileStorage, DB
import transaction

storage = FileStorage.FileStorage('myfatabase.fs')
db = DB(storage)

class Test_variables(Persistent):

	def __init__(self):
	
		connection, root = self.connect_ZODB()
		
		try: 
			self.catalogue = root.catalogue
		except:
			self.catalogue = {}
			
		connection.close()
			
		
	def connect_ZODB(self):
		
		connection = db.open()
		root = connection.root()
			
		return connection, root
		
	def save_ZODB(self):
	
		connection, root = self.connect_ZODB()
		
		root.catalogue = self.catalogue

		transaction.commit()
		connection.close()
		
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
		
		#opens a connection to ZODB to make the changes permanent
		self.save_ZODB()
			
			
if __name__ == "__main__":

	catalogue = Test_variables()
	
	catalogue.add_job('concejal', 50000)
	
	print catalogue.catalogue
	
	# catalogue.add_job('juerguista',20000)
	# catalogue.add_job('secretario', 15000)
	# catalogue.add_job('zorro', 150000000)
	
	# print catalogue.catalogue
	
	# connection, root = catalogue.connect_ZODB()
	


	
	
					
