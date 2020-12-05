"""
Options to control library behaviour

Notes
----------
If an option is also a function parameter, the here specified values are for fallback.

e. g. calling a.to_get_expr(as_latex=False) will return as non latex string even if options.as_latex=True
If nothing is specified the assumed value will be options.as_latex.
"""

# TODO implement max digits

as_latex = True
"""wether string will be returned in more console friendly format or for latex parsing"""

gauss_error_name = "stat"
"""name of gauss error for printing. Printing gauss error gives \\sigma_{options.gauss_error_name} """

max_error_name = "sys"
""" name of maximum error for printing"""

no_rounding = False
""" library will normaly look for significant places and cut numbers accordingly.
can be deactivated with this option

Notes
----------
(1.032112+-0.0122+-0.042221) will be cut to (1.032+-0.012+-0.042)
"""

simplify_eqs = True
"""Simplify equations before printing them.
Some simplifcations like 
    
    sqrt(b*b)=sqrt(b^2)=|b| 
cannot be prevented"""

error_mode = 2
"""Specify how error output works. Does not effect calculations. 

See Also
----------
error_analysis.evar.ErrorMode"""

# unfinished or buggy


max_digits = 8
"""At this digit all output will be rounded despite being more precise

.. warning:: not working yet"""

correct_garbage_collection = False
"""Decides wether to delete out of scope objects. 

Working with library is far less error prone without correct gc. However correct gc massively improves memory usage.
Examples
----------
If True this

     a= evar(..)*10
     print(a.get_expr())
will fail.
However this

    a=evar(..)
    a*=10
    print(a.get_expr())
will not. All functions which retrieve expressions will have to resolve their dependencies.
In the first case the expression for a will be a = UnnamedVariable*10. Since UnnamedVariable has no direct reference 
anymore, it will be deleted. In the second case, as still has an exisiting reference and won't be deleted.
"""
