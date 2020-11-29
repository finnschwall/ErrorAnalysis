# TODO add option for working with single error
# TODO implement fast mode
# BUG options don't work as parameters
# when false than string will be printed in more readable format
print_as_latex = True
# name of gauss error for printing
gauss_error_name = "stat"
# name of maximum error for printing
max_error_name = "sys"
# library will normaly look for siginificant places and cut numbers accordingly.
# can be deactivated with this option
no_rounding = False
# Ignore expressions and just calculate. Significantly faster but doesn't allow
# printing of gauss max or own expression.
# WARNING: this will cause immediate garbage collection
# also not finished yet. lol
fast_mode = False
# simplify equations before printing them
# some simplifcations like sqrt(b*b)=sqrt(b^2)=|b| cannot be prevented
simplify_eqs = True
