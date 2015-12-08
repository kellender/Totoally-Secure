'''
<Purpose> 
    Check commit history against user permissions.

<Arguments>
    Git metadata dictionary, permissions list (ACL).  If beginning 
    and end dates are in ACL, they must be datetime.datetime type

<Returns>
    Dictionary with commits as keys, permission violations as values

'''
import time
from datetime import datetime
from dateutil.parser import parse
from pytz import utc

def checker(metadata, permissions):
    violations = {}
    for commit in metadata:
        errStr = ''
        author = metadata[commit]['author']
        if author not in permissions:
            errStr += ' Author not in permissions.'
        elif permissions[author]['write'] == False or 'write' not in permissions[author]:
            errStr += ' Author does not have permission to write.'
        elif type(permissions[author]['write']) == datetime:
            time_stamp = parse(metadata[commit]['author_timestamp'])
            print time_stamp
            if time_stamp < permissions[author]['commit'][0]:
                errStr += ' Write occured before author had write permission.'
            elif time_stamp > permissions[author]['commit'][1]:
                errStr += " Write occured after author's write permission expired."

        committer = metadata[commit]['committer']
        if committer not in permissions:
            errStr += ' Committer not in permissions.'
        elif 'commit' not in permissions[committer] or permissions[committer]['commit'] == False:
            errStr += ' Committer does not have permission to commit.'
        elif type(permissions[committer]['commit']) == tuple:
            time_stamp = parse(metadata[commit]['commit_timestamp'])
            print time_stamp
            if time_stamp < permissions[committer]['commit'][0]:
                errStr += ' Commit occured before committer had commit permission.'
            elif time_stamp > permissions[committer]['commit'][1]:
                errStr += " Commit occured after committer's commit permission expired."

        if committer in permissions and 'merge' in metadata[commit]['type']:
            if permissions[committer]['merge'] == False or 'merge' not in permissions[committer]:
                errStr += ' Committer does not have permission to merge.'
            elif type(permissions[committer]['merge']) == datetime:
                time_stamp = parse(metadata[commit]['commit_timestamp'])
                print time_stamp
                if time_stamp < permissions[committer]['merge'][0]:
                    errStr += ' Merge occured before committer had merge permission.'
                elif time_stamp > permissions[committer]['merge'][1]:
                    errStr += " Merge occured after committer's merge permission expired."
        
        if errStr == '':
            violations[commit] = 'OK'
        else:
            violations[commit] = errStr
    return violations

if __name__ == '__main__':
    a = utc.localize(datetime.now())
    time.sleep(10)
    b = utc.localize(datetime.now())
    dat = {
        '1':{'author':'Juan', 'committer':'Pablo', 'type':'merge', 'commit_timestamp': "2015-11-20 08:42:27 +0100"},
           }
    acl = {
        'Juan':{'write':True},
        'Pablo':{'commit':(a,b),'merge':True}
            }
    print checker(dat, acl)
