'''
Integer Constraint Solver to generate 
actual (and valid) CHiLL script instances
'''
from constraint import *
    
xforms = [] #list of xforms in order
problem = Problem()

def generate_parameter_domain(superscript):
    prefix = ""
    suffix = ""

    file = open(superscript,'r')
    lines = file.readlines()
    nlines = len(lines)
    lno = 0
    while ('@start_param_region' not in lines[lno]):
        
        if(lines[lno].startswith('#')):
            lno += 1
            continue

        prefix += lines[lno]
        lno += 1
    
    #scan through the code and add variables and constraints
    # Then ask the solver to to give us valid points

 
    
    while('@end_param_region' not in lines[lno]):
        if(lines[lno].startswith('param')):
            print 'param line'
        
        elif(lines[lno].startswith('known')):
            print 'known line'

        elif(lines[lno].startswith('')):
            pass

        lno += 1
        

    while(lno<nlines):
        suffix += lines[lno]
        lno += 1

    print suffix
    
    
    file.close()


