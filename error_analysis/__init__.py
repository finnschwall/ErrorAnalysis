"""
See also https://github.com/finnschwall/error_analysis
"""
from collections import namedtuple

from error_analysis.evar import *
# REMOVE BEFORE UPLOAD

# for generating and formatting documentation
# doc gen: pdoc3 --html -f --config show_source_code=False  error_analysis -o C:\Users\finns\Downloads\test2
__pdoc__ = {}
Table = namedtuple('error_analysis', ['tools', 'debug'])
__pdoc__["error_analysis.tools"] = False
__pdoc__["error_analysis.debug"] = False
__pdoc__["Table"] = False
__pdoc__["tools"] = False