# Persistent class is imported so the Class can 
# be saved later in ZODB
from persistent import Persistent

class Catalogo(Persistent):

	def __init__(self):
	
		self.catalogo = []
		
	def anadir(self, codigo, nombre, siglo):
	
		self.catalogo.append(Antiguedad(codigo,nombre,siglo))
		
	def buscar(self, codigo):
	
		for antiguedad in self.catalogo :
			#print antiguedad.codigo
			if codigo == antiguedad.codigo :
				print "Esta en el catalogo"
				break
			
		print "No esta en el catalogo"
				
				
		

class Antiguedad(Persistent):
	""" Tres Atributos"""

	def __init__(self, codigo, nombre, siglo):
	
		self.codigo = codigo
		self.nombre = nombre
		self.siglo = siglo
		
		
if __name__ == "__main__":


	
	catalogo = Catalogo()
	
	catalogo.anadir(1, "Pintura", "XVII")
	catalogo.anadir(2, "Esculutura", "XV")
	
	catalogo.buscar(3)
	
	print type(catalogo.catalogo[0])
	
	print catalogo.catalogo[0].codigo
	print catalogo.catalogo[0].nombre
	
	
	import ZODB, ZODB.FileStorage
	import transaction
	
	storage = ZODB.FileStorage.FileStorage('mydata.fs')
	db = ZODB.DB(storage)
	connection = db.open()
	root = connection.root
	
	root.catalogo = catalogo
	
	# root.catalogo.anadir(1, "Pintura", "XVII")
	# root.catalogo.anadir(2, "Esculutura", "XV")
	
	transaction.commit()
	
	connection.close()
	
	


	
	
	
	
	
		
		
		