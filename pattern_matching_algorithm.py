#! /usr/bin/env python

"""
<Program Name>
    pattern_matching_algorithm.py

<Authors>
    Team Totolly Secure

<Started>
    November 2015.



<Purpose>
    The following shell command recurses through metadata, detect
    workflow paterns, and log its findings especially those findings
    that are strange when compared to the rest of the pattern.
    Workflows may be of any style.
"""

import repository_lib, repository_tool

# It starts here:
#       One file - located within /tuf-develop/tuf/
#       Do not check on individual workflows... makes no sense
#       Checks to detect a behavior or pattern
#       Functions should include:
#           function to recurse to previous commit
#           using imported functions to grab metadata
#           function that has our algorithm to detect a pattern * the main one
#       The imported libraries have most or all of the TUF metadata grabbing stuff
#       Regular Expressions can be used in the algorithm to find patterns
