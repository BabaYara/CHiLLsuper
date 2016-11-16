A parser to generate CHiLL script instances from a parameterized CHiLL superscript.

    import csolver
    csolver.generate_parameter_domain('path-to-superscript')
    
CHiLL superscript syntax overview

    @begin_param_region         #start a parameterized region 
    param(x,enum,[v1,...,vn])   #introduce a new 'enum' type parameter x with its domain [v1,...,vn]
    known(c1,...,cn)            #define constraints between parameters
    t(f(x))                     #call CHiLL transformation t in terms of defined parameters
    @end_param_region           #end the innermost parameterized region
