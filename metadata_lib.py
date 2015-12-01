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
from collections import Counter


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

# ______________________________________________________________________________
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

# ______________________________________________________________________________
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
        Runs list of keys for sub_metadata that have different author and committer.
    """
    lst = []
    for key in metadata:
        if metadata[key]["author"] != metadata[key]["committer"]:
            lst.append(key)
    return lst
    
# ______________________________________________________________________________
def detect_mergers(metadata):
    """
        Returns the mergers and their respective merges count.
    """
    
    lst = []
    for key in metadata:
        lst.append(metadata[key]["committer"])

    # Finding the mode merger and its count along with any other mergers
    data = Counter(lst)
    counters = data.most_common()   # List of Tuples
    
    return counters, len(lst)

def get_infamous_mergers(metadata):
    """
        Returns hashes to mergers that merges less than 10% of the time.
    """
    lst = []
    counters, mergers = detect_mergers(metadata)
    for merger in counters:         # List of Tuples traversal
        if merger[1] / mergers < 0.1:
            print "Possible Infamous Merger: " + str(merger[0])
            lst.append(merger[0])

    infamous_hashes = []
    for key in metadata:
        if metadata[key]["committer"] in lst:
            infamous_hashes.append(metadata[key])
    return infamous_hashes
    
# ______________________________________________________________________________
# WORKFLOW FUNCTIONS

def dictator_lieutenent_workflow(metadata):
	"""
		Returns true if repository follows a dictator-lieutenent
		workflow.
		<Perhaps incomplete - this so far only works on Master clones>
	"""
	print "Checking if Dictator-Lieutenent Workflow..."
	is_workflow = True
	infamous_mergers = get_infamous_mergers(metadata)
	if len(infamous_mergers) != 1:
		is_workflow = False
		print "Not a dictator-lieutenent workflow"
	
	return is_workflow
