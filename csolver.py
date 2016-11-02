'''
Integer Constraint Solver to generate 
actual (and valid) CHiLL script instances
'''
from constraint import *
 
params= [] # list of 3-tuples, (name, type, [domain])
knowns = [] # list of constraints
xforms = [] #list of xforms in order, 
problem = Problem()

class Param:
    name = ''
    type = ''
    domain = None

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
            '''
            param line looks like the following
            
            param(name,type,[val0,val1,...,valn])

            name - any alphanumeric constant
            type - Enum
            values - a list of values
            '''

            args = lines[lno][6:-2].split(',') # val0 and valn will have [,] connected to them. Remove
            args[2] = args[2].split('[')[1]
            args[-1] = args[-1].split(']')[0]
    
            p = Param()
            p.name = args[0]
            p.type = args[1]
            p.domain = []
            for val in args[2:]:
                p.domain.append(val)

            #print p.name, p.type, p.domain

            params.append(p)           
            
        
        elif(lines[lno].startswith('known')):
            '''
            known line looks like the following
            
            known(c1,c2,...,cn)

            where ci is a relation between one or more parameters
            '''
            cons = lines[lno][6:-2].split(',')
        
            for c in cons: 
                knowns.append(c)


        elif(lines[lno].startswith('')):
            pass

        lno += 1
        

    while(lno<nlines):
        suffix += lines[lno]
        lno += 1
    
    file.close()


