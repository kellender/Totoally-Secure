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
import json

# hashes of commits that were already touched
hashes = []

# metadata dictionary
metadata = {}

def parse_metadata(current_commit, commit_hash):
    """
    <Purpose>
        Parses a node's metadata and stores it in the "metadata"
        dictionary of dictionaries. "commit_hash" is the key.
    
    <Arguments>
        A node and its hash.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    global metadata
    temp_metadata = {}
    
    for item in current_commit:
        if item == '':
            break
        if item.split()[0] == "parent":
                temp_metadata['parent'] = item.split()[1]
        if item.split()[0] == "committer" or item.split()[0] == "author":
            sz = len(item.split())
            string = ''
            for i in range(1, sz):
                string += (str(item.split()[i]) + " ")
            key = str(item.split()[0])
            temp_metadata[key] = string
    
    metadata[commit_hash] = temp_metadata

def add_child( parent_hash, child_hash ) :
    """
    <Purpose>
        This function assigns child nodes to metadata for the current node.
        Value added will be the child hash.
    
    <Arguments>
        Parent and childs' hashes.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    global metadata
    
    child_num = 2

    while True :
        child = "child"+`child_num`

        if child in metadata[parent_hash] :
            child_num += 1
        else :
            metadata[parent_hash][child] = child_hash
            break

def add_timestamps( commit_hash, merge ) :
    """
    <Purpose>
        This function adds timestamps to metadata associated with action.
    
    <Arguments>
        Committer's hash and a bool value indicating whether action
        is a merge or not.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    global metadata
    
    metadata[commit_hash]["author_timestamp"] = check_output(
        ["git", "show", "-s", "--format=%ai", commit_hash]
        ).strip( )

    if merge :
        metadata[commit_hash]["merge_timestamp"] = check_output(
            ["git", "show", "-s", "--format=%ci", commit_hash]
            ).strip( )

# Recurse thought the tree until the initial commit is reached.
def traverse( commit_hash ) :
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
    
    global metadata
    global hashes
    # text of the current git commit object
    # elements of current_commit are in the format "<label> <value>"
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]
        ).split( "\n" )
    
    # parents of the current commit
    parents = []
    merge = False
    
    parse_metadata(current_commit, commit_hash)
    
    # find all parents of the current commit
    for line in current_commit :
        if len( line ) != 0 :
            if line.startswith( "parent" ) :
                parents.append( line )
            elif line.startswith( "author" ) :
                metadata[commit_hash]["author"] = line.split( " ", 1 )
            elif line.startswith( "committer" ) :
                metadata[commit_hash]["merger"] = line.split( " ", 1 )
                merge = True

    add_timestamps( commit_hash, merge )

    if merge :
        metadata[commit_hash]["type"] = "merge"
    else :
        metadata[commit_hash]["type"] = "commit"
    
    
    if len( parents ) > 0 :
        for x in range( 0, len( parents ) ) :
            parent_hash = parents[x].split()[1]
            
            metadata[commit_hash]["parent"+`x+1`] = parent_hash

            
            if parent_hash not in hashes :
                
                hashes.append( parent_hash )
                meta = {"child1": commit_hash}
                metadata[parent_hash] = meta
                traverse( parent_hash )
            else :
                add_child( parent_hash, commit_hash )

def output_json(name, action, data, indent):
    with open(name + ".json", action) as ofs:
        ofs.write(json.dumps(data, indent = 4))

# hash of the HEAD commit
head = check_output( ["git", "rev-parse", "HEAD"] ).strip( )
hashes.append( head )
traverse( head )
output_json("meta_metadata", 'w', metadata, 4)
