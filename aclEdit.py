'''
<Purpose> 
    Provide user friendly method for editing permissions list for 
    check.py

<Arguments>
    acl.json file (should be in same directory)
    user input at run time

<Returns>
    modified acl.json

<Issues>
    Time restricted permissions do not currently support None type. 
    An implementation was attempted but results in an error.
'''

import json
import os.path
from dateutil.parser import parse
from pytz import utc

if not os.path.isfile('acl.json'):
    print 'No such file exists.  Creating...'
    with open('acl.json', 'w') as f:
        f.write('{}')
    acl = {}
else:
    with open('acl.json', 'r') as f:
        try:
            acl = json.load(f)
            print 'Permissions list found and loaded!'
        except ValueError:
            acl = {}
            print 'Problem loading permissions, creating new list'

while True:
    key = raw_input('What do you want to do?  Type help for options: ')

    if key == 'help':
        print 'done    -- end session'
        print 'user ID -- look up or edit user permissions'
        print 'all     -- look up or edit permissions for all users'
        continue

    if key == 'done' or key == 'quit' or key == 'q':
        with open('acl.json', 'w') as f:
            json.dump(acl, f)
        break

    if key not in acl:
        response = raw_input('User ID not found.  Would you like to add? (y/n) ').lower()
        if response == 'y' or response == 'yes':
            acl[key] = {}
            print 'User created.'
            with open('acl.json', 'w') as f:
                json.dump(acl, f)
            
    else:
        print 'User permissions:'
        print acl[key]
        print
        response = raw_input('Would you like to make changes? (y/n) ').lower()
        if response == 'y' or response == 'yes':
            while True:
                response = raw_input('Input a change you would like to make, or type "help" for options: ').lower()
                if response == 'done' or response == 'quit' or response == 'q':
                    with open('acl.json', 'w') as f:
                        json.dump(acl, f)
                    break
                elif response == 'help':
                    print 'OPTIONS:'
                    print 'done   -- return to user ID lookup'
                    print 'delete -- delete user ID from permissions'
                    print 'revoke -- remove permission from user'
                    print 'add    -- grant user new permission'
                elif response == 'delete':
                    del acl[key]
                    with open('acl.json', 'w') as f:
                        json.dump(acl, f)
                    break
                elif response == 'revoke':
                    valid_entry = False
                    while not valid_entry:
                        permission = raw_input('Which permission do you want to revoke? (write/commit/merge): ').lower()
                        if permission != 'commit' and permission != 'merge' and permission != 'write':
                            print 'Invalid entry'
                        else:
                            valid_entry = True
                    acl[key][permission] = False
                    with open('acl.json', 'w') as f:
                        json.dump(acl, f)
                elif response == 'add':
                    valid_entry = False
                    while not valid_entry:
                        permission = raw_input('Which permission do you want to add? (write/commit/merge): ').lower()
                        if permission != 'commit' and permission != 'merge' and permission != 'write':
                            print 'Invalid entry'
                        else:
                            valid_entry = True
                    response = raw_input('Would you like to set time restrictions? (y/n): ').lower()
                    if response == 'y' or response == 'yes':
                        begin = raw_input('Input begin date (YYYY-MM-DD hh:mm:dd): ').lower()
                        end = raw_input('Input end date (YYYY-MM-DD hh:mm:dd): ').lower()
                        val = begin, end
                    else:
                        val = True
                    acl[key][permission] = val
                    with open('acl.json', 'w') as f:
                        json.dump(acl, f)
