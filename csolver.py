'''
Integer Constraint Solver to generate 
actual (and valid) CHiLL script instances
'''
from constraint import *


problem = Problem()

def generate_parameter_domain(superscript):
    file = open(superscript)
    
    for line in file:
        if(line is "@start_parame_region"):


#scan through the code and add variables and constraints
# Then ask the solver to to give us valid points






    file.close()
