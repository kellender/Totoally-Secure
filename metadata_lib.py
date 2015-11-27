"""
<Program Name>
    metadata_lib.py
    
<Authors>
    Team Totolly Secure
    
<Started>
    November 2015.

    
<Purpose>
    To provide a list of functions that may assist with parsing metadata data
    structure with a given policy.
"""


def check(sub_key, value, metadata):
    """
        Runs list of keys for sub_metadata that have a value that does not
        match the value passed in.
    """
    lst = []
    for key in metadata:
        if metadata[key][sub_key] != value:
            lst.append(key)
    return lst

def check_with_type(sub_key, value, metadata, type_):
    """
        Runs list of keys for sub_metadata that have a value that does not
        match the value passed in for a specific type of commit.
    """
    lst = []
    for key in metadata:
        if metadata[key][sub_key] != value and metadata[key]["type"] == type_:
            lst.append(key)
    return lst

def list_merges(metadata):
    """
        Runs list of keys for sub_metadata that have merges.
    """
    lst = []
    for key in metadata:
        if "parent1" in metadata[key] and "parent2" in metadata[key]:
            lst.append(key)
    return lst

def list_branches(metadata):
    """
        Runs list of keys for sub_metadata that have branches.
    """
    lst = []
    for key in metadata:
        if "child1" in metadata[key] and "child2" in metadata[key]:
            lst.append(key)
    return lst

def author_committer_same(metadata):
    """
        Runs list of keys for sub_metadata that have same author and committer.
    """
    lst = []
    for key in metadata:
        if metadata[key]["author"] == metadata[key]["committer"]:
            lst.append(key)
    return lst

def author_committer_differ(metadata):
    """
        Runs list of keys for sub_metadata that have same author and committer.
    """
    lst = []
    for key in metadata:
        if metadata[key]["author"] != metadata[key]["committer"]:
            lst.append(key)
    return lst
    
