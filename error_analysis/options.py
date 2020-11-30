# TODO add option for working with single error
# TODO implement fast mode
# BUG options don't work as parameters
#
print_as_latex = True
"""when false than string will be printed in more readable format"""

gauss_error_name = "stat"
"""name of gauss error for printing """

max_error_name = "sys"
""" name of maximum error for printing"""

no_rounding = False
""" library will normaly look for siginificant places and cut numbers accordingly.
can be deactivated with this option"""

simplify_eqs = True
"""simplify equations before printing them
some simplifcations like sqrt(b*b)=sqrt(b^2)=|b| cannot be prevented"""



# unfinished or buggy

single_error_mode = False
"""Will cause all error output to be combined with sigma= sqrt(gauss^2+max^2) 
Does not change internal calculations. So a set maximum error will still be calculated like a maximum error"""

max_digits = 8
"""At this digit all output will be rounded despite being more precise"""

fast_mode = False
"""Ignore expressions and just calculate. Significantly faster but doesn't allow
printing of gauss max or own expression.
WARNING: this will cause immediate garbage collection
"""
