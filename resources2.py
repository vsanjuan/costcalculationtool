#import the model class from peewee to model the classes and properties as tables
#and fields in the Sqlite Database
from peewee import *

database = SqliteDatabase('productcost.db')

#model definitions -- the standard "pattern" is to define a base model class
#that specifies which database to use. Then, any subclasses will automatically
#use the correct storage.
class BaseModel(Model):
	class Meta:
		database = database


#the Resource model specifies its fields declaratively
class Resource(BaseModel):
	"""Represents the resources used by the different activities.
	
	Attributes:
		name: Resource name.
		resource_code: A unique alphanumeric that identifies the resource.
		measure_unit : Unity of measure in which the resource usage and cost 
		is measured.
		cost: Cost in Euros of the resource per measure_unit. This value is 
		calculated for its child from its properties. 
	
	"""
	name = CharField()
	resource_code = CharField(unique = True)
	measure_unit = CharField()
	cost = FloatField()
	

	# def __init__(self, name, resource_code, measure_unit, cost):
	
		# self.name = name
		# self.resource_code = resource_code
		# self.measure_unit = measure_unit
		# self.cost = cost
		
	def calculate_cost():
		"""Calculates the cost per unit of measure for each resource depending
		of the properties of each child resource.
		
		Args:
			Defined in the child class
			
		Returns:
			A cost in Euros per measure_unit
			
		"""
		
		pass
		
		
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
	
	job_category = CharField()
	gross_salary = DecimalField(2)
	benefits = DecimalField(2)
	annual_hours = IntegerField()
	effective_working_rate = DecimalField(2)
	cost = DecimalField()  # cost per hour
	
	
	# def __init__(self, job_category, resource_code, gross_salary, benefits, annual_hours, effective_working_rate):
		# """Inits JobCategory."""
		# Resource.__init__(self, job_category, resource_code, "hours", 0)
		# self.job_category = job_category
		# self.gross_salary = gross_salary

		# self.benefits = benefits
		# self.annual_hours = annual_hours
		# self.effective_working_rate = effective_working_rate / 100.0
		
		# self.cost = self.calculate_cost()
		
	def calculate_cost(self):
		"""Calculates the cost per effective working hour based on the object
		properties"""
		
		hourly_cost = ( self.gross_salary + self.benefits) / (self.annual_hours * self.effective_working_rate)
		
		return hourly_cost
		
		
if __name__ == "__main__":

	#database = SqliteDatabase('productcost.db')
	
	#database.create_tables([Resource])
	
	maquina = Resource.create(name = "Tractor", resource_code="A24", measure_unit="unit", cost = 50000)
	
	print maquina.name, maquina.resource_code

	# designer = JobCategory.create("Designer", 10, 30000, 10000, 1800, 80 )
	# print "Name ", designer, "\nJob Category", designer.job_category   
	# print "Gross Salary: {:,}. \nBenefits: {:,}.".format(designer.gross_salary, designer.benefits) 
	# print "Annual Hours:{:,}. \nWorking rate: {:.2f}%".format(designer.annual_hours, designer.effective_working_rate * 100)
	# print "Measure unit: %s" % designer.measure_unit 
	# designer_hourly_rate = designer.calculate_cost()
	# print "Designer hourly rate: %.2f" % designer_hourly_rate
	# print "Cost: %.2f" % designer.cost
	
	
		
		
	