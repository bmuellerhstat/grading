import os
import pprint
from re import search

# pattern = '\/\/(?! JS)'
pattern = '(?<!ntent..|device\-)width'
code = 'ellipse(width)'

if search(pattern.lower(), code.lower()):
    print("Found!")
else:
    print(":(")