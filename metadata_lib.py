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
import json, sys, os.path, re

def check_acl(metadata, acl_name, violation):
	"""
	<Purpose>
		Checks metadata against a list of permissions.
		ALGORITHM OF THIS FUNCTION IS DEFINITELY NOT OPTIMIZED.
		ONE TO THREE SUB FUNCTION SHOULD HANDLE commit, merge, and write.
    
    <Arguments>
		metadata dictionary
		acl_name or file name to permissions
		violation is the output file name
    
    <Exceptions>
        None
    
    <Returns>
        Dict
    """
	acl = {}
	if not os.path.isfile(acl_name):
		print "Permission List does not exist."
		sys.exit()
	else:
		acl = read_json(acl_name)
	
	unreviewed = detect_unreviewed_merges(metadata)
	
	violations = {}
	
	for commit in metadata:
		errors = ""
		if commit in unreviewed:
			errors += "Merge not code reviewed. "
		if metadata[commit]["author"] not in acl:
			errors += "Author " + str(metadata[commit]["author"]) + " not in ACL. "
		if metadata[commit]["committer"] not in acl:
			errors += "Committer " + str(metadata[commit]["committer"]) + " not in ACL. "
			if "merge" in metadata[commit]["commit_type"]:
				errors += "Merger " + str(metadata[commit]["committer"]) + " not in ACL. "

		if "merge" in metadata[commit]["commit_type"] and metadata[commit]["committer"] in acl:
			if "merge" in acl[metadata[commit]["committer"]]:
				if "start" in acl[metadata[commit]["committer"]]["merge"]:
					if isinstance(acl[metadata[commit]["committer"]]["merge"]["start"], bool):
						if acl[metadata[commit]["committer"]]["merge"]["start"] == True:
							print "Merger of " + str(commit) + " has open date for start merge permission."
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge start permission. "
					else:
						if compare_time(acl[metadata[commit]["committer"]]["merge"]["start"], metadata[commit]["commit_timestamp"]) == False:
							errors += "Merger " + str(metadata[commit]["committer"]) + " merged before permission was granted. "
				else:
					errors += "ACL does not have start merge time for " + metadata[commit]["committer"] + ". "
				if "end" in acl[metadata[commit]["committer"]]["merge"]:
					if isinstance(acl[metadata[commit]["committer"]]["merge"]["end"], bool):
						if acl[metadata[commit]["committer"]]["merge"]["end"] == True:
							print "Merger of " + str(commit) + " has open date for end merge permission."
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge end permission. "
					else:
						if compare_time(metadata[commit]["commit_timestamp"], acl[metadata[commit]["committer"]]["merge"]["end"]) == False:
							errors += "Merger " + str(metadata[commit]["committer"]) + " merged after permission has expired. "
				else:
					errors += "ACL does not have end merge time for " + metadata[commit]["committer"] + ". "
				if "layer" in acl[metadata[commit]["committer"]]["merge"]:
					if isinstance(acl[metadata[commit]["committer"]]["merge"]["layer"], bool):
						if acl[metadata[commit]["committer"]]["merge"]["layer"] == True:
							print "Merger of " + str(commit) + " can merge in any layer."
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in layer " + str(metadata[commit]["layer"]) + ". "
					else:
						if str(metadata[commit]["layer"]) in acl[metadata[commit]["committer"]]["merge"]["layer"]:
							print "Merger of " + str(commit) + " can merge in layer " + str(metadata[commit]["layer"])
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in layer " + str(metadata[commit]["layer"]) + ". "
				else:
					errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in layer " + str(metadata[commit]["layer"]) + ". "
				if "branch" in acl[metadata[commit]["committer"]]["merge"]:
					if isinstance(acl[metadata[commit]["committer"]]["merge"]["branch"], bool):
						if acl[metadata[commit]["committer"]]["merge"]["branch"] == True:
							print "Merger of " + str(commit) + " can write in any branch."
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in branch " + str(metadata[commit]["branch"]) + ". "
					else:
						if str(metadata[commit]["branch"]) in acl[metadata[commit]["committer"]]["merge"]["branch"]:
							print "Merger of " + str(commit) + " can merge in branch " + str(metadata[commit]["branch"])
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in branch " + str(metadata[commit]["branch"]) + ". "
				else:
					errors += "Merger " + str(metadata[commit]["committer"]) + " does not have merge permissions in branch " + str(metadata[commit]["branch"]) + ". "
					
				
		if metadata[commit]["author"] in acl:
			if "write" in acl[metadata[commit]["author"]]:
				if "start" in acl[metadata[commit]["author"]]["write"]:
					if isinstance(acl[metadata[commit]["author"]]["write"]["start"], bool):
						if acl[metadata[commit]["author"]]["write"]["start"] == True:
							print "Author of " + str(commit) + " has open date for start write permission."
						else:
							errors += "Author " + str(metadata[commit]["author"]) + " does not have write start permission. "
					else:
						if compare_time(acl[metadata[commit]["author"]]["write"]["start"], metadata[commit]["author_timestamp"]) == False:
							errors += "Author " + str(metadata[commit]["author"]) + " wrote before permission was granted. "
				else:
					errors += "ACL does not have start write time for " + metadata[commit]["author"] + ". "
				if "end" in acl[metadata[commit]["author"]]["write"]:
					if isinstance(acl[metadata[commit]["author"]]["write"]["end"], bool):
						if acl[metadata[commit]["author"]]["write"]["end"] == True:
							print "Author of " + str(commit) + " has open date for end write permission."
						else:
							errors += "Author " + str(metadata[commit]["committer"]) + " does not have write end permission. "
					else:
						if compare_time(metadata[commit]["author_timestamp"], acl[metadata[commit]["author"]]["write"]["end"]) == False:
							errors += "Author " + str(metadata[commit]["author"]) + " wrote after permission has expired. "
				else:
					errors += "ACL does not have end write time for " + metadata[commit]["author"] + ". "
				if "layer" in acl[metadata[commit]["author"]]["write"]:
					if isinstance(acl[metadata[commit]["author"]]["write"]["layer"], bool):
						if acl[metadata[commit]["author"]]["write"]["layer"] == True:
							print "Author of " + str(commit) + " can write in any layer."
						else:
							errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in layer " + str(metadata[commit]["layer"]) + ". "
					else:
						if str(metadata[commit]["layer"]) in acl[metadata[commit]["author"]]["write"]["layer"]:
							print "Author of " + str(commit) + " can write in layer " + str(metadata[commit]["layer"])
						else:
							errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in layer " + str(metadata[commit]["layer"]) + ". "
				else:
					errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in layer " + str(metadata[commit]["layer"]) + ". "
				if "branch" in acl[metadata[commit]["author"]]["write"]:
					if isinstance(acl[metadata[commit]["author"]]["write"]["branch"], bool):
						if acl[metadata[commit]["author"]]["write"]["branch"] == True:
							print "Author of " + str(commit) + " can write in any branch."
						else:
							errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in branch " + str(metadata[commit]["branch"]) + ". "
					else:
						if str(metadata[commit]["branch"]) in acl[metadata[commit]["author"]]["write"]["branch"]:
							print "Author of " + str(commit) + " can write in branch " + str(metadata[commit]["branch"])
						else:
							errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in branch " + str(metadata[commit]["branch"]) + ". "
				else:
					errors += "Author " + str(metadata[commit]["author"]) + " does not have write permissions in branch " + str(metadata[commit]["branch"]) + ". "


		if metadata[commit]["committer"] in acl and "merge" not in metadata[commit]["commit_type"]:
			if "commit" in acl[metadata[commit]["committer"]]:
				if "start" in acl[metadata[commit]["committer"]]["commit"]:
					if isinstance(acl[metadata[commit]["committer"]]["commit"]["start"], bool):
						if acl[metadata[commit]["committer"]]["commit"]["start"] == True:
							print "Committer of " + str(commit) + " has open date for start commit permission."
						else:
							errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit start permission. "
					else:
						if compare_time(acl[metadata[commit]["committer"]]["commit"]["start"], metadata[commit]["commit_timestamp"]) == False:
							errors += "Committer " + str(metadata[commit]["committer"]) + " committed before permission was granted. "
				else:
					errors += "ACL does not have start commit time for " + metadata[commit]["committer"] + ". "
				if "end" in acl[metadata[commit]["committer"]]["commit"]:
					if isinstance(acl[metadata[commit]["committer"]]["commit"]["end"], bool):
						if acl[metadata[commit]["committer"]]["commit"]["end"] == True:
							print "Committer of " + str(commit) + " has open date for end write permission."
						else:
							errors += "Merger " + str(metadata[commit]["committer"]) + " does not have commit end permission. "
					else:
						if compare_time(metadata[commit]["commit_timestamp"], acl[metadata[commit]["committer"]]["commit"]["end"]) == False:
							errors += "Committer " + str(metadata[commit]["committer"]) + " committed after permission has expired. "
				else:
					errors += "ACL does not have end commit time for " + metadata[commit]["committer"] + ". "
				if "layer" in acl[metadata[commit]["committer"]]["commit"]:
					if isinstance(acl[metadata[commit]["committer"]]["commit"]["layer"], bool):
						if acl[metadata[commit]["committer"]]["commit"]["layer"] == True:
							print "Committer of " + str(commit) + " can commit in any layer."
						else:
							errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in layer " + str(metadata[commit]["layer"]) + ". "
					else:
						if str(metadata[commit]["layer"]) in acl[metadata[commit]["committer"]]["commit"]["layer"]:
							print "Committer of " + str(commit) + " can commit in layer " + str(metadata[commit]["layer"])
						else:
							errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in layer " + str(metadata[commit]["layer"]) + ". "
				else:
					errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in layer " + str(metadata[commit]["layer"]) + ". "
				if "branch" in acl[metadata[commit]["committer"]]["commit"]:
					if isinstance(acl[metadata[commit]["committer"]]["commit"]["branch"], bool):
						if acl[metadata[commit]["committer"]]["commit"]["branch"] == True:
							print "Committer of " + str(commit) + " can commit in any branch."
						else:
							errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in branch " + str(metadata[commit]["branch"]) + ". "
					else:
						if str(metadata[commit]["branch"]) in acl[metadata[commit]["committer"]]["commit"]["branch"]:
							print "Committer of " + str(commit) + " can commit in branch " + str(metadata[commit]["branch"])
						else:
							errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in branch " + str(metadata[commit]["branch"]) + ". "
				else:
					errors += "Committer " + str(metadata[commit]["committer"]) + " does not have commit permissions in branch " + str(metadata[commit]["branch"]) + ". "
		
		violations[commit] = errors
	counter = 0
	for i in violations:
		if violations[i] != "":
			counter += 1
	print "There are " + str(counter) + " commits/hashes with violations."
	write_json(violation, violations)
	return violations
						


def compare_time(start, end):
	"""
	<Purpose>
		Manually compares two times.
        Returns True if end time is more recent than start time.
		Returns False otherwise.
    
    <Arguments>
		start time
		end time
    
    <Exceptions>
        None
    
    <Returns>
        Bool
    """
	s = re.split('-|\+|:| ', start)
	e = re.split('-|\+|:| ', end)
	if s[0] > e[0]:
		return False
		if s[1] > e[1]:
			return False
			if s[2] > e[2]:
				return False
				if s[3] > e[3]:
					return False
					if s[4] > e[4]:
						return False
						if s[5] > e[5]:
							return False
	return True

def read_json(name):
    """
	<Purpose>
        Reads JSON file and returns it as a dictionary.
    
    <Arguments>
		Name of input file
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns dictionary
    """
    with open(name) as f:    
    	data = json.load(f)
	return data

def write_json(name, data):
	"""
	<Purpose>
        Writes dictionary to JSON file.
    
    <Arguments>
		Name of output file
		Dictionary to write in file
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Returns Nothing
    """
	with open(name, "w") as ofs :
		ofs.write(json.dumps(data, indent = 4 ))

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
        if value not in metadata[key][sub_key]:
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
        if value not in metadata[key][sub_key] and type_ in metadata[key]["commit_type"]:
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

