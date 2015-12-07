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

def return_hashes(metadata):
	"""
	<Purpose>
        Returns metadata keys in a list.
    
    <Arguments>
		Metadata object
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
	hashes = []
	for key in metadata:
		hashes.append(key)
	return hashes

def check(sub_key, value, metadata):
    """
	<Purpose>
        Runs list of keys for sub_metadata that have a value that does not
        match the value passed in.
    
    <Arguments>
		sub_key that can be "code_reviewed", "committer", "branch", etc...
		Expected value for the above sub_key
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if metadata[key][sub_key] != value:
            lst.append(key)
    return lst

def check_with_type(sub_key, value, metadata, type_):
    """
	<Purpose>
        Runs list of keys for sub_metadata that have a value that does not
        match the value passed in for a specific type of commit.
    
    <Arguments>
		sub_key that can be "code_reviewed", "committer", "branch", etc...
		Expected value for the above sub_key
		Metadata object.
		type of commit to check for in the Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if metadata[key][sub_key] != value and metadata[key]["commit_type"] == type_:
            lst.append(key)
    return lst

# ______________________________________________________________________________
def list_merges(metadata):
    """
    <Purpose>
        Finds all merging commits.
    
    <Arguments>
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if "parent1" in metadata[key] and "parent2" in metadata[key]:
            lst.append(key)
    return lst

def list_branches(metadata):
    """
    <Purpose>
        Finds all branching/forking commits.
    
    <Arguments>
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if "child1" in metadata[key] and "child2" in metadata[key]:
            lst.append(key)
    return lst

# ______________________________________________________________________________
def author_committer_same(metadata):
    """
    <Purpose>
        Checks commits where author and committer are the same.
    
    <Arguments>
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if metadata[key]["author"] == metadata[key]["committer"]:
            lst.append(key)
    return lst

def author_committer_differ(metadata):
    """
    <Purpose>
        Checks commits where author and committer differ.
    
    <Arguments>
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
    lst = []
    for key in metadata:
        if metadata[key]["author"] != metadata[key]["committer"]:
            lst.append(key)
    return lst
    
# ______________________________________________________________________________
def detect_unreviewed_merges(metadata):
	"""
    <Purpose>
        Checks all merges that have not been code reviewed.
    
    <Arguments>
		Metadata object.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a list of hashes.
    """
	return check_with_type("code_reviewed", "True", metadata, "merge")

def detect_mergers(metadata):
    """
    <Purpose>
        Returns mergers and associated number of merges in
		the form of a list of tuples. Also returns
		number of unique mergers.
    
    <Arguments>
		Metadata object
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns list of tuples and length of list
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
	<Purpose>
        Returns hashes to mergers that merges less than 10% of the time.
		THIS FUNCTION HAS BEEN DEEMED USELESS
    
    <Arguments>
		Metadata object
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns list of hashes
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

def __dictator_lieutenent_workflow_scrap(dictator, lieut_list, metadata):
	"""
		DO NOT USE
	"""
	print "Checking if Dictator-Lieutenent Workflow..."
	is_workflow = True
	infamous_mergers = get_infamous_mergers(metadata)
	if len(infamous_mergers) != 1:
		is_workflow = False
		print "Not a dictator-lieutenent workflow"
	
	return is_workflow

def dictator_lieutenent_driver(acl, dictator_names, lieut_names, metadata):
	"""
    <Purpose>
        This function takes names of dictators and lieutenents and calls the
		actual function that detects if repository follows a dictator-
		lieutenent workflow.
    
    <Arguments>
        Access Control List (dictionary of dictionaries)
			{
				user1:{
					write:"True",
					commit:"True",
					merge:(<str>,<str>)
				},
				user2:{
					write:"True"
				},
				...
			}
		Dictator names (list of strings)
		Liuetenent names (list of strings)
		Metadata object
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a boolean value.
    """
	dictator_dict = {}
	lieut_dict = {}
	for key in acl:
		if key in dictator_names:
			temp = {}
			temp[key] = acl[key]
			dictator_dict[key] = temp
		elif key in dictator_names:
			temp = {}
			temp[key] = acl[key]
			dictator_dict[key] = temp
	return __dictator_lieutenent_workflow(dictator_dict, lieut_dict, metadata)
	

def __dictator_lieutenent_workflow(dictator_dict, lieut_dict, metadata):
	"""
    <Purpose>
        Checks if merges in the master is done only by the dictator and
		any repositories that are one merge away from the master has
		merges that have been done by lieutenent.
    
    <Arguments>
		Dictator's dictionary from driver function
		Liuetenent's dictionary from driver function
		Metadata object
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns a boolean value.
    """
	print "Checking if Dictator-Lieutenent Workflow..."
	is_workflow = True
	merges = list_merges(metadata)		# Returns list of hashes for merges
	
	for hashes in merges:
		if metadata[hashes]["committer"] in dictator_dict and metadata[hashes]["layer"] == 0:
			if "merge" in dictator_dict[metadata[hashes]["committer"]]:
				if isinstance(dictator_dict[metadata[hashes]["committer"]]["merge"], tuple):
					if metadata[hashes]["commit_timestamp"] > dictator_dict[metadata[hashes]["committer"]]["merge"][0] and metadata[hashes]["commit_timestamp"] < dictator_dict[metadata[hashes]["committer"]]["merge"][1]:
						print "Dictator is fine"
					else:
						is_workflow = False
				elif isinstance(dictator_dict[metadata[hashes]["committer"]]["merge"], str):
					if dictator_dict[metadata[hashes]["committer"]]["merge"] == "True":
						print "Dictator is fine"
					else:
						is_workflow = False
				else:
					is_workflow = False
	
	for hashes in merges:
		if metadata[hashes]["committer"] in lieut_dict and metadata[hashes]["layer"] == 1:
			if "merge" in lieut_dict[metadata[hashes]["committer"]]:
				if isinstance(lieut_dict[metadata[hashes]["committer"]]["merge"], tuple):
					if metadata[hashes]["commit_timestamp"] > lieut_dict[metadata[hashes]["committer"]]["merge"][0] and metadata[hashes]["commit_timestamp"] < lieut_dict[metadata[hashes]["committer"]]["merge"][1]:
						print "Lieutenent is fine"
					else:
						is_workflow = False
				elif isinstance(lieut_dict[metadata[hashes]["committer"]]["merge"], str):
					if lieut_dict[metadata[hashes]["committer"]]["merge"] == "True":
						print "Lieutenent is fine"
					else:
						is_workflow = False
				else:
					is_workflow = False

	if is_workflow == False:
		print "Not Dictator-Lieutenent Workflow"
	return is_workflow

