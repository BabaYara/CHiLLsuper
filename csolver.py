'''
Integer Constraint Solver to generate 
actual (and valid) CHiLL script instances
'''
from constraint import *
import re

varnames = [] # a list of variable names for fast access
params= [] # list of 3-tuples, (name, type, [domain])
knowns = [] # list of constraints
xforms = []
XFORMS = ['tile', 'distribute', 'skew', 'fuse', 'permute', 'omp_par_for', 'partial_sums'] #list of xforms in order, 

problem = Problem()

class Param:
    name = ''
    type = ''
    domain = None

class Xform:
    id = -1     #keeps track of the global ordering of parameterized xforms
    type = ''
    vals = []   #vars involved in the xform

'''
def generate_xfor_regex:
    xregex = ''
    for xform in XFORMS:
        xregex+=xform+'|'
    return xregex[:-1] #chop the last '|' off
'''

def generate_parameter_domain(superscript):
    prefix = ""
    suffix = ""
    num_x = -1

    file = open(superscript,'r')
    lines = file.readlines()
    file.close()

    nlines = len(lines)
    lno = 0
    while ('@start_param_region' not in lines[lno]):
        
        if(lines[lno].startswith('#')):
            lno += 1
            continue

        prefix += lines[lno]
        lno += 1
    
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
            varnames.append(p.name)
            p.type = args[1]
            p.domain = []
            for val in args[2:]:
                p.domain.append(int(val))

            #print p.name, p.type, p.domain

            params.append(p)           
            if p.type == 'enum':
                problem.addVariable(p.name,p.domain)
            
            #TODO:add support to other types

        elif(lines[lno].startswith('known')):
            '''
            known line looks like the following
            
            known(c1,c2,...,cn)

            where ci is a relation between one or more parameters
            '''
            cons = lines[lno][6:-2].split(',')
            
            for c in cons: 
                knowns.append(c)
                # find what variables are in the constraint
                regex = '\+|-|\*|/|==|<=|>=|<|>| '
                terms_in_c = re.split(regex,c)

                if '' in terms_in_c:
                    continue
                #now filter out the variables among the terms
                v = []
                lambda_str = 'lambda '

                for term in terms_in_c:
                    if term in varnames:
                        v.append(term)
                        lambda_str += term+','

                lambda_str = lambda_str[:-1] #remove last ,
                
                lambda_str += ': ('+c+')'
                var_tuple = tuple(v)

                exec('lambda_function ='+lambda_str)

                #now add the constraint to the problem
                problem.addConstraint(lambda_function, var_tuple)

             
        else:
            '''
            we expect everything else inside the param region to represent a parameterized xform, (because a rigorous check is expensive, poor excuse)
            If something's wrong, CHiLL shall(will) catch it
            '''
            num_x += 1
            x = Xform()
            x.id = num_x
            
            toks = re.split('\(|\)',lines[lno])
            #print toks[0]
            if toks[0] in XFORMS:
                #we are good to go
                x.type = toks[0]

                #extract arg values now
                args = toks[1].split(',')
                for arg in args:
                    x.vals.append(arg)

                xforms.append(x)

            else:
                print 'Bad xform found in line '+str(lno)

        lno += 1

    lno += 1 #skip @end_param_region

    #solve the constraint problem
    solutions = problem.getSolutions()
    print solutions

    while(lno<nlines):
        suffix += lines[lno]
        lno += 1

#=================================================================================
# reading, processing done! Next --> codegen

    for script in range(len(solutions)):
        block = ''
        param_values = solutions[script]

        for xform in xforms:
            block += xform.type+'('

            for v in xform.vals:
                if v in varnames:
                    block += str(param_values[v])+','
                else: #direct value
             
                    block += v+','
            
            block = block[:-1]+')\n'
        
        full_script = prefix+'\n'+block+'\n'+suffix
        
        f = open('script_{0}.chill'.format(str(script)),'w')
        f.write(full_script)
        f.close()

