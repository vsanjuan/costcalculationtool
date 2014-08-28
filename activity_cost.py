
class Activity(object):
    
    """ Represents an activity to be performed in order to deliver the product
    to the customer.
    """

    def __init__(self, name, code, output_unit, throughput, output_time_unit, fixed_cost = 0, variable_cost = 0):
        
        """Initialize a new activity by specifying its name, identification code,
        output, and throughput ( output per unit of time) and time unit. The time unit
        is very important for capacity and cost calculation purposes. If no unit is
        declared it is assumed it will be hours
        """

        self.name = name
        self.code = code
        self.output_unit = output_unit
        self.throughput = throughput
        self.output_time_unit = output_time_unit
        self.fixed_cost = fixed_cost
        self.variable_cost = variable_cost
        #print "Initializing Activity", self.name, self.code, self.throughput, self.output_unit, self.output_time_unit



    def calculate_cost(self):
        """Calculate the cost per unit of activity. Some activities will have fixed cost so
        the cost will be divided by the expected output during the period """
		print "Method to be implemented by each child"



    def calculate_ouput(self):
        """Calculate the total activity units produced in a given period"""
		print "Method to be implemented by each child"

        

        
class Service(Activity):
    """Services activities have tied up resources in order to provide a service wether or not its capacity is used. In
    order to calculate the cost per unit of output for this type of activity we need to add the service hours"""

    def __init__(self, name, code, output_unit, throughput, output_time_unit,  working_days, hours_per_day):
        """The service class extends Activity by adding information about availability of the activity"""

        Activity.__init__(self, name, code, output_unit, throughput, output_time_unit)
        self.working_days = working_days
        self.hours_per_day = hours_per_day

        print "Initializing service ", self.working_days, self.hours_per_day

    def calculate_output(self):

        return self.working_days * self.hours_per_day * self.throughput


if __name__ == "__main__":
    

    correr = Activity("Correr", 1, "meters", 1000, "hour")

    dormir = Service("Dormir", 2, "hours", 8, "day", 365, 8)

    horas_sueno = dormir.calculate_output()

    print horas_sueno



        
        
        
