# Persistent class is imported so the Class can 
# be saved later in ZODB
from persistent import Persistent
from ZODB import FileStorage, DB
import transaction
from copy import deepcopy

storage = FileStorage.FileStorage('activity_costing.fs')
db = DB(storage)



class Resource(Persistent):
	"""Represents the resources used by the different activities.
	
	Attributes:
		name: Resource name.
		resource_code: A unique alphanumeric that identifies the resource.
		measure_unit : Unity of measure in which the resource usage and cost 
		is measured.
		cost: Cost in Euros of the resource per measure_unit. This value is 
		calculated for its child from its properties. 
	
	"""

	def __init__(self, name, resource_code, measure_unit, cost):
	
		self.name = name
		self.resource_code = resource_code
		self.measure_unit = measure_unit
		self.cost = cost
		
	def calculate_cost():
		"""Calculates the cost per unit of measure for each resource depending
		of the properties of each child resource.
		
		Args:
			Defined in the child class
			
		Returns:
			A cost in Euros per measure_unit
			
		"""
		
		pass
		
		
class ResourceCatalogue(Persistent):
	""" Represents a catalogue of the resources available and the
	methods used to manage the catalogue. This class has no attributes """


	def __init__(self):
	
		connection, root = self.connect_ZODB()
		
		try: 
			self.resource_catalogue = deepcopy(root.resource_catalogue)
		except:
			self.resource_catalogue = {}
			
			
		connection.close()
		
	def connect_ZODB(self):
		"""Opens a connection to the ZODB"""
	
		connection = db.open()
		root = connection.root()
			
		return connection, root
		
	def save_ZODB(self, resource):
		"""Saves de catalogue to the ZODB"""
	
		connection, root = self.connect_ZODB()
		
		self.resource_catalogue[resource.resource_code] = resource
		
		root.resource_catalogue = self.resource_catalogue

		transaction.commit()
		connection.close()
	
		
	def add_resource(self) :
		""" Method to be implemented by the child class to add a new
		resource"""
		pass
		
		
	def search_resource(self, resource_code = "", resource_name = ""):
		"""Method to search and retrieve a resource by code or name.
		If the resource is found returns a ResourceCategory object. If
		not returns None."""
		
		if resource_code in self.resource_catalogue:
			return self.resource_catalogue[resource_code]
		else:
			return None
		
		for resource in self.resource_catalogue.values():
			if ( resource.name == resource_name) :
				 return resource
		
		return None
		
	
	def list_resources(self, typeofresource = None):
		"""List all items included in the catalogue.
		Each child from this class has its own __str__ method"""
		
		
		catalogue = self.resource_catalogue.values()
		
		print "*" * 80
		print "*" * 30 + "Lista de recursos" + "*" * 33
		print "*" * 80
		
		for resource in catalogue:
			if type == None:
				print resource
				print "*" * 80
			else:
				if type(resource) == typeofresource:
					print resource
					print "*" * 80
					
		
	def delete_resource(self, resource_code):
	
		pass
	
		
		
		
				
						
		
class JobCatalogue(ResourceCatalogue):
	"""Represent a catalogue of the different job categories from where
	they can be managed and puts it in persistent ZODB storage
	"""
	
	def __init__(self):
		"""Adds a new Job Category list to the root ZODB if it hasn't
		been created yet. Otherwise it loads the information from the database.
		"""
		
		ResourceCatalogue.__init__(self)
		
		
	def add_resource(self, job_category, resource_code, gross_salary, benefits, annual_hours, effective_working_rate):
		"""Adds a new job category to the job catalogue and returns the JobCategory object
		"""	
		
		new_category = JobCategory(job_category, resource_code, gross_salary, benefits, annual_hours, effective_working_rate)
		
		
		# checks if the resource code is in the database. If so warns the user before committing the changes
		if  resource_code not in self.resource_catalogue:
			
			#Save the new_category object
			self.save_ZODB(new_category)

			return new_category
		else:
			print "Resource {} code already exists. ".format(resource_code) 
			resource = self.search_resource(resource_code)
			print resource
			print "Please check and try again"
			return new_category # The object is returned to the user to modify it.
		
	# def search_job(self, resource_code):
		""" Returns a job object if it matches the code or False if there
		is no job category with the resource code """
			
		
		
class JobCategory(Resource):
	"""Represents the different job categories employed in each activity 
	according to its qualifications
	
	Attributes:
		job_category: job performed.
		gross_salary: annual income before taxes 
		benefits: annual monetary cost of extra costs as social security, health 
		insurance, etc..
		annual_hours: yearly hours worked according to law and labour agreements.
		effective_working_rate: estimated percentage of effective working hours.
		Default value is 80%. The value is stored as a percentage.	
	"""
	
	def __init__(self, job_category, resource_code, gross_salary, benefits, annual_hours, effective_working_rate):
		"""Inits JobCategory."""
		Resource.__init__(self, job_category, resource_code, "hours", 0)
		self.gross_salary = gross_salary
		self.benefits = benefits
		self.annual_hours = annual_hours
		self.effective_working_rate = effective_working_rate / 100.0
		
		self.cost = self.calculate_cost()
		
		
	def __str__(self):
	
		return 	("Resource Code: " + str(self.resource_code) + 
				" \nJob category: " + str(self.name) + 
				" \nGross salary: {:,}".format(self.gross_salary) + 
				" \nBenefits {:,} ".format(self.benefits) + 
				" \nAnnual working hours: {:,}".format(self.annual_hours) + 
				" \nEffective working rate {:.2%} ".format(self.effective_working_rate) + 
				" \nHourly cost: {:.2f} ".format(self.cost))
				
		
	def calculate_cost(self):
		"""Calculates the cost per effective working hour based on the object
		properties"""
		
		hourly_cost = ( self.gross_salary + self.benefits) / (self.annual_hours * self.effective_working_rate)
		
		return hourly_cost
		
		
class Equipment(Resource):
	"""Represents the equipment used in the company to peform different activities.
	
	Attributes:
	
	Resouce_code : A unique code that identifies the equipment
	Equipment_name: Name of the equipment 
	Measure_unit: Unit of measure in which the equipment is kept in inventory.
	Acquisition_cost : Cost of the equipment installed and working in the company including transport
	and installation expenses.
	Useful_life : Time in which the equipment will be productive.
	Useful_life_time_unit = It can be hours or years depending on the type of equipment.
	
	"""

	def __init__(self, resource_code, equipment_name, measure_unit, acquisition_cost, useful_life, useful_life_time_unit="hours"):
	
		Resource.__init__(self, equipment_name, resource_code, measure_unit, 0)
		
		self.acquisition_cost = acquisition_cost				  # acquisition in Euros.
		self.useful_life = useful_life							  # useful life in hours
		self.useful_life_time_unit = useful_life_time_unit        # it has to be a time object that allows conversions
		
		self.cost = self.calculate_cost()
		
		
	def calculate_cost(self):
		""" Calculates the cost of the equipment per unit of time"""
	
		return self.acquisition_cost / self.useful_life
		
	def __str__(self):
		
		return ("Equipment code: {} ".format(self.resource_code) +
				"\nEquipment name: {} ".format(self.name) +
				"\nMeasure unit: {} ".format(self.measure_unit) +
				"\nAcquisition cost: {:,} ".format(self.acquisition_cost) +
				"\nUseful life: {:,}".format(self.useful_life) +
				"\nUseful life time unit: {}".format(self.useful_life_time_unit) +
				"\nCost per time unit: {:.2f}".format(self.cost))
		
class Space(Resource):

	"""Represents the space available for the activities performed in the company.
	
	"""

	
		
		
		
if __name__ == "__main__":


	prensa = Equipment(21, "Prensa", "Maquina", 20000, 10000)
	
	print prensa
	
	resource = ResourceCatalogue()
	
	resource.list_resources()
	

	# job_catalogue = JobCatalogue()	
	
	# # paleta = job_catalogue.add_resource("Paleta", 16, 15000, 5000, 1800, 50 )
	
	# # print "*" * 80
	
	# # designer = job_catalogue.add_resource("Designer", 15, 30000, 10000, 1800, 80 )
	
	# # print "*" * 80
	
	# resource = job_catalogue.search_resource(15)
	# print "El recurso quince es: ",  resource
	
	# job_catalogue.list_resources(JobCategory)
	
	#job_catalogue.list_resources()
	# print job
	# print paleta
	# print job.gross_salary

	

	
	
	
	
	
		
		
	