'''
<Purpose> 
    Check commit history against user permissions.

<Arguments>
    Git metadata dictionary, permissions list (ACL).  If beginning 
    and end dates are in ACL, they must be datetime.datetime type

<Returns>
    Dictionary with commits as keys, permission violations as values

<Issues>
    Time restricted permissions do not currently support None type. 
    An implementation was attempted but results in an error.
'''

import time, json, metadata_lib
from datetime import datetime
from dateutil.parser import parse
from pytz import utc

def checker(metadata, permissions):
    unreviewed = metadata_lib.detect_unreviewed_merges(metadata)
    violations = {}
    if 'all' not in permissions:
        permissions['all'] = {}
    for commit in metadata:
        errStr = ''
        if commit in unreviewed:
            errStr += 'Unreviewed merge. '
        author = metadata[commit]['author']
        if 'write' in permissions['all'] and permissions['all']['write'] == True:
            pass
        elif author not in permissions:
            errStr += 'Author not in permissions. '
        elif 'write' not in permissions[author] or permissions[author]['write'] == False:
            errStr += 'Author does not have permission to write. '
        elif type(permissions[author]['write']) == datetime:
            time_stamp = parse(metadata[commit]['author_timestamp'])
            begin = parse(permissions[committer]['write'][0])
            end = parse(permissions[committer]['write'][1])
            if begin == None:
                assert time_stamp > begin
            if end == None:
                assert time_stamp < end
            if time_stamp < begin:
                errStr += 'Write occured before author had write permission. '
            elif time_stamp > end:
                errStr += "Write occured after author's write permission expired. "

        committer = metadata[commit]['committer']
        if 'commit' in permissions['all'] and permissions['all']['commit'] == True:
            pass
        elif committer not in permissions:
            errStr += 'Committer not in permissions. '
        elif 'commit' not in permissions[committer] or permissions[committer]['commit'] == False:
            errStr += 'Committer does not have permission to commit. '
        elif type(permissions[committer]['commit']) == tuple:
            time_stamp = parse(metadata[commit]['commit_timestamp'])
            if permissions[committer]['commit'][0] == None:
                assert time_stamp > permissions[committer]['commit'][0]
            if permissions[committer]['commit'][1] == None:
                assert time_stamp < permissions[committer]['commit'][1]
            if time_stamp < permissions[committer]['commit'][0]:
                errStr += 'Commit occured before committer had commit permission. '
            elif time_stamp > permissions[committer]['commit'][1]:
                errStr += "Commit occured after committer's commit permission expired. "

        if committer in permissions and 'merge' in metadata[commit]['commit_type']:
            if 'merge' in permissions['all'] and permissions['all']['merge'] == True:
                pass
            elif 'merge' not in permissions[committer] or permissions[committer]['merge'] == False:
                errStr += 'Committer does not have permission to merge. '
            elif type(permissions[committer]['merge']) == datetime:
                time_stamp = parse(metadata[commit]['commit_timestamp'])
                if permissions[committer]['merge'][0] == None:
                    assert time_stamp > permissions[committer]['merge'][0]
                if permissions[committer]['merge'][1] == None:
                    assert time_stamp < permissions[committer]['merge'][1]
                if time_stamp < permissions[committer]['merge'][0]:
                    errStr += 'Merge occured before committer had merge permission. '
                elif time_stamp > permissions[committer]['merge'][1]:
                    errStr += "Merge occured after committer's merge permission expired. "
        
        if errStr == '':
            violations[commit] = 'OK'
        else:
            violations[commit] = errStr
    return violations

def check(metadata, acl, violation):
    acl_data = metadata_lib.read_json(acl)
    metadata_lib.write_json(violation, checker(metadata, acl_data))

'''
if __name__ == '__main__':
    with open('acl.json', 'r') as f:
        acl = json.load(f)
	"""
    dat = {
        '1':{'author':'Tacos', 'committer':'Juan', 'type':'commit', 'commit_timestamp': "2015-11-20 08:42:27 +0100"},
        '2':{'author':'Juan', 'committer':'Tacos', 'type':'merge', 'commit_timestamp': "2015-11-20 08:42:27 +0100"},
           }
	"""
	dat = metadata_lib.read_json("metadata.json")
    metadata_lib.write_json("violations.json", checker(dat, acl))
'''

