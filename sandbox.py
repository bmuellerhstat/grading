import os
import pprint
from re import search

pattern = '(function mouse|function key)'
code = 'function ky'

if search(pattern.lower(), code.lower()):
    print("Found!")
else:
    print(":(")