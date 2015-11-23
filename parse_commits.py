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

from subprocess import check_output

# hashes of commits that were already touched
hashes = []

meta_metadata = {}

def traverse( commit_hash ):
    """
    <Purpose>
        This function takes in the HEAD node and recurses backwards
        while visiting each node.
    
    <Arguments>
        HEAD node.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    f = open('vscode_metadata.txt','a')

    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash] ).split("\n")
    
    f.write(str(current_commit))
    f.write('\n')
    
    parse_metadata(current_commit, commit_hash)

    parents = []

    for line in current_commit:
        if ( len( line ) != 0 ) and ( line.find( "parent" ) == 0 ):
            parents.append( line )
    
    if len( parents ) > 0:
        for parent in parents:
            parent_hash = parent.split()[1]

            global hashes
            if parent_hash not in hashes:
                hashes.append( parent_hash )
                traverse( parent_hash )
            else:
                f.write("\t\t\tBRANCH/FORK\n")
    
    f.close()



def parse_metadata(current_commit, commit_hash):
    """
    <Purpose>
        Parses a node's metadata and stores it in the "meta_metadata"
        data structure in the form ofa dictionary. "commit_hash" is
        the key.
    
    <Arguments>
        A node and its hash.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    global meta_metadata
    metadata = {}
    for item in current_commit:
        
        if item == '':
            break
        if item.split()[0] == "parent":
                metadata['parent'] = item.split()[1]
        if item.split()[0] == "committer" or item.split()[0] == "author":
            
            sz = len(item.split()) - 1
            string = ''
            for i in range(1, sz):
                string += (str(item.split()[i]) + " ")
            key = str(item.split()[0])
            
            metadata[key] = string
    meta_metadata[commit_hash] = metadata


head = check_output( ["git", "rev-parse", "HEAD"] ).strip()
hashes.append( head )
traverse( head )


counter = 0
for key in meta_metadata:
    counter += 1

print meta_metadata
print "Keys in meta_metadata: " + str(counter)



