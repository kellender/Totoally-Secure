#! /usr/bin/env python

"""
<Program Name>
    pattern_driver.py

<Authors>
    Team Totolly Secure

<Started>
    November 2015.



<Purpose>
    The following shell command recurses through a respository to
    find the pattern matching algorithm used in Toto. This script
    is merely used as a means of convinence.
"""

import os, sys

if len(sys.argv) != 2:
    raise Exception("Invalid Number of arguments")

def recurse_dir():
    """
    <Purpose>
        This script calls Toto's pattern matching algorithm in the file named
        "parse_commits.py"
    
    <Arguments>
        None.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    # Ideal file path: "C:\Users\User\Documents\TUF"
    for root, sub_dirs, files in os.walk(sys.argv[1]):
        for file in files:
            #print os.path.join(root, file)
            if file == "parse_commits.py":
                os.system(file)

recurse_dir()
