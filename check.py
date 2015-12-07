'''
<Purpose> 
    Check commit history against user permissions.

<Arguments>
    Git metadata dictionary, permissions list (ACL)

<Returns>
    Dictionary with commits as keys, permission violations as values

'''

def checker(metadata, permissions):
    violations = {}
    for commit in metadata:
        errStr = ''
        author = metadata[commit]['author']
        if author not in permissions:
            errStr += ' Author not in permissions.'
        elif permissions[author]['write'] == False or 'write' not in permissions[author]:
            errStr += ' Author does not have permission to write.'

        committer = metadata[commit]['committer']
        if committer not in permissions:
            errStr += ' Committer not in permissions.'
        elif 'commit' not in permissions[committer] or permissions[committer]['commit'] == False:
            errStr += ' Committer does not have permission to commit.'
        if committer in permissions and 'merge' in metadata[commit]['type']:
            if permissions[committer]['merge'] == False or 'merge' not in permissions[committer]:
                errStr += ' Committer does not have permission to merge.'
        
        if errStr == '':
            violations[commit] = 'OK'
        else:
            violations[commit] = errStr
    return violations

if __name__ == '__main__':
    dat = {
        '1':{'author':'Juan', 'committer':'Pablo', 'type':'merge'},
           }
    acl = {
        'Juan':{'write':True},
        'Pablo':{'commit':True,'merge':False}
            }
    print checker(dat, acl)
