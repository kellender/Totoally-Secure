"""
<Program Name>
    ctrl.py
    
<Authors>
    Team Totolly Secure
    
<Started>
    December 2015.

    
<Purpose>
    Command line tool to edit permissions in JSON file.
    Tool can be used independently if necessary.
"""

import json, sys, os.path, getopt, re

acl = {}

def __read_json(name):
    """
	<Purpose>
        Reads JSON file and returns it as a dictionary.
    
    <Arguments>
		name of input file
    
    <Exceptions>
        None
    
    <Returns>
        Returns dictionary
    """
    with open(name) as f:    
    	data = json.load(f)
	return data

def __write_json(name, data):
	"""
	<Purpose>
        Writes dictionary to JSON file.
    
    <Arguments>
		name of output file
		data in the form of dictionary to write in file
    
    <Exceptions>
        None
    
    <Returns>
        None
    """
	with open(name, "w") as ofs :
		ofs.write(json.dumps(data, indent = 4))

def __load_json(file_name):
	"""
	<Purpose>
        Reads JSON file and fills global acl dictionary.
    
    <Arguments>
		file_name or name of input file
    
    <Exceptions>
        None
    
    <Returns>
        None
    """
	global acl
	if not os.path.isfile(file_name):
		__write_json(file_name, acl)
	else:
		acl = __read_json(file_name)

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
	

def main(argv):
	global acl

	if len(argv) < 2:
		print "Invalid command - too few arguments"
		sys.exist()

	__load_json("acl.json")
	
	delete = ''
	user = ''
	permission = ''
	start = ''
	end = ''
	layer = []
	branch = []
	
	try:
		opts, args = getopt.getopt(argv[1:], "d:u:p:s:e:l:b:hf", ["delete=","help=","user=","permission=","start=","end=","layer=","branch=","flush="])
	except getopt.GetoptError:
		print "crtl.py -u <username> -p <permission> -s <start-time> -e <end-time> -l <layers> -b <branches>\nctrl.py -d <username>\nctrl.py -d <username> -p <permission>\nctrl -f"
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print "crtl.py -u <username> -p <permission> -s <start-time> -e <end-time> -l <layers> -b <branches>\nctrl.py -d <username>\nctrl.py -d <username> -p <permission>\nctrl.py -f"
			sys.exit()
		elif opt in ("-u", "--user"):
			user = arg
		elif opt in ("-p", "--permission"):
			permission = arg
		elif opt in ("-s", "--start"):
			start = arg
		elif opt in ("-e", "--end"):
			end = arg
		elif opt in ("-l", "--layer"):
			if arg in ("True", "true", "t", "T"):
				layer = True
			elif arg in ("False", "false", "f", "F"):
				layer = False
			else:
				layer = re.split(',|;| ', arg)
		elif opt in ("-b", "--branch"):
			if arg in ("True", "true", "t", "T"):
				branch = True
			elif arg in ("False", "false", "f", "F"):
				branch = False
			else:
				branch = re.split(',|;| ', arg)
		elif opt in ("-d", "--delete"):
			delete = arg
		elif opt in ("-f", "--flush"):
			acl = {}
			__write_json("acl.json", acl)
			sys.exit()
	
	if delete == '':
		if user not in acl:
			if user == '':
				print "Invalid command - username required"
				sys.exit()
			acl[user] = {}
		if permission == '' or permission not in ("commit","merge","write"):
			print "Invalid command - commit/merge/write permission required"
			sys.exit()
		elif permission != '':
			acl[user][permission] = {}
			if start != '' and end != '':
				if compare_time(start, end) == False:
					print "Invalid command - end time must be greater than start time"
					sys.exit()
			if start in ("True", "true", "t", "T"):
				acl[user][permission]["start"] = True
			elif start in ("False", "false", "f", "F"):
				acl[user][permission]["start"] = False
			elif start != '':
				acl[user][permission]["start"] = start
			if end in ("True", "true", "t", "T"):
				acl[user][permission]["end"] = True
			elif start in ("False", "false", "f", "F"):
				acl[user][permission]["end"] = False
			elif end != '':
				acl[user][permission]["end"] = end
			if layer in (True, False):
				acl[user][permission]["layer"] = layer
			elif len(layer) != 0:
				acl[user][permission]["layer"] = layer
			if branch in (True, False):
				acl[user][permission]["branch"] = branch
			elif len(branch) != 0:
				acl[user][permission]["branch"] = branch	
	else:
		if permission == '':
			if delete in acl:
				del acl[delete]
		else:
			if delete in acl:
				if permission in acl[delete]:
					del acl[delete][permission]
	__write_json("acl.json", acl)

main(sys.argv)










