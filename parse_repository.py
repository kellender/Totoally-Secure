"""
<Program Name>
    parse_repository.py

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
import json, metadata_lib

# hashes of commits that were already touched
hashes = []

# metadata dictionary
metadata = {}

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
        # child label in metadata
        child = "child"+`child_num`

        # if a child with this lable exists increment the child number
        # else add the label and passed child hash to the parent's metadata
        if child in metadata[parent_hash] :
            child_num += 1
        else :
            metadata[parent_hash][child] = child_hash
            break

def add_timestamps( commit_hash ) :
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

    # git command for getting the author timestamp
    metadata[commit_hash]["author_timestamp"] = check_output(
        ["git", "show", "-s", "--format=%ai", commit_hash]
        ).strip( )

    # git command for getting the commit timestamp
    metadata[commit_hash]["commit_timestamp"] = check_output(
        ["git", "show", "-s", "--format=%ci", commit_hash]
        ).strip( )

# for now types include: HEAD, TAIL, commit, pre-branch/fork. amd merge
def add_type( commit_hash, commit_type ) :
    """
    <Purpose>
        Adds the "Type" of action attribute to the metadata.
    
    <Arguments>
        The commit's hash and commit's type from another call is required.
    
    <Exceptions>
        None. Program will fail silently if algorithm is not found.
    
    <Returns>
        Nothing.
    """
    
    global metadata

    # if there is no commit type for the passed commit, add it
    # else append the passed type to the "commit_type" attribute
    if "commit_type" not in metadata[commit_hash] :
        metadata[commit_hash]["commit_type"] = commit_type
    else :
        # could be "pre-branch/fork" and "merge" simultaneously
        metadata[commit_hash]["commit_type"] += "; "+commit_type

def check_code_review( commit_hash ) :
    global metadata

    # 'stack' to hold all commits that are merges
    merges = []
    # the current commit being checked for code review
    current = commit_hash

    # initial code review check; only goes through branch of passed commit
    # it is assumed the passed commit is the HEAD commit
    while True :
        # if the commit is a merge, push it to the "merges" stack
        # any other commits get checked for code review immediately
        if "merge" in metadata[current]["commit_type"] :
            merges.append( current )
        else :
            metadata[current]["code_reviewed"] = \
                `metadata[current]["author"] != \
                metadata[current]["committer"]`

        # name the branch; assumed it's the master branch
        metadata[current]["branch"] = "master"
        metadata[current]["layer"] = 0
        # if the current commit has at least one parent, continue the loop
        # on that parent
        # else it's the TAIL commit; exit the loop
        if "parent1" in metadata[current] :
            current = metadata[current]["parent1"]
        else :
            break

    # used for naming branches; i.e. "branch1", "branch2", ..., "branchN",
    # where N is some positive integer
    branch_num = 1
    layer = 1
    # while the merges stack is still populated (there are still merges
    # to check for code review)
    while len( merges ) > 0 :
        # pop the next merge to check
        merge_commit = merges.pop( )
        layer = 1
        # default value for the merge code review check
        merge_reviewed = True

        # list to hold the parents of the merge
        parents = []

        # used to grab the parents; i.e. "parent2", ..., "parentN"
        # starts at 2 because the first parent's branch would have already
        # been traversed
        parent_count = 2
        # while the parent label exists in the current merge commit's
        # metadata, store the parent hahs and increment the parent count
        while "parent"+`parent_count` in metadata[merge_commit] :
            parents.append( \
                metadata[merge_commit]["parent"+`parent_count`] )
            parent_count += 1

        # loop through the parents of the merge commit
        for parent in parents:
            current = parent
            
            # keep looping until a checked commit is run into
            # a checked commit represents the end of the branch
            while "code_reviewed" not in metadata[current] :
                # if the current commit is a merge, push it to the stack
                # else check the commit for code review, and compare it
                # against the merge to check the merge for code review
                if "merge" in metadata[current]["commit_type"] :
                    merges.append( current )
                    layer += 1
                else :
                    metadata[current]["code_reviewed"] = \
                        `metadata[current]["author"] != \
                        metadata[current]["committer"]`
                    
                    # if the merge is still conisdered properly reviewed
                    # compare the merge against the current commit
                    if merge_reviewed :
                        merge_reviewed = metadata[current]["committer"] != \
                            metadata[merge_commit]["committer"]

                # give the current commit a branch name
                metadata[current]["branch"] = "branch"+`branch_num`
                metadata[current]["layer"] = layer
                # move to the next commit; the parent of the current
                current = metadata[current]["parent1"]

        # add code review check to current merge commit
        metadata[merge_commit]["code_reviewed"] = `merge_reviewed`

        # increment the branch number
        branch_num += 1
        
            
# Recurse thought the tree until the initial commit is reached.
def traverse( commit_hash, child_hash = None ) :
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
    
    global hashes
    global metadata

    # initialize the current commit as dictionary
    metadata[commit_hash] = {}

    # if a child hash was passed, add it to the current commit's metadata
    if child_hash :
        metadata[commit_hash]["child1"] = child_hash

    # text of the current git commit object
    # elements of current_commit are in the format "<label> <value>"
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]
        ).split( "\n" )
    
    # parents of the current commit
    parents = []

    # loop through all the lines of the commit
    for line in current_commit :
        # if the line isn't blank
        if len( line ) != 0 :
            # if the line has a parent hash, store the line
            # if the line has the commit's author, add it to the metadata
            # if the line has the commit's committer, add it to the metadata
            if line.startswith( "parent" ) :
                parents.append( line )
            elif line.startswith( "author" ) :
                author = line.split( " ", 1 )[1]
                metadata[commit_hash]["author"] = \
                    author[:author.find( ">" )+1]
            elif line.startswith( "committer" ) :
                committer = line.split( " ", 1 )[1]
                metadata[commit_hash]["committer"] = \
                    committer[:committer.find( ">" )+1]

    # add the author and committer timestamps to the commit's metadata
    add_timestamps( commit_hash )
    

    # if the commit has parents
    if len( parents ) > 0 :
        # for each parent, add them to the current commit's metadata
        # and add the current commit as each parent's child
        for i in range( 0, len( parents )  ) :
            # get the parent hash from the git commit object's line
            parent_hash = parents[i].split( )[1]

            # add the parent hash to the current commit
            metadata[commit_hash]["parent"+`i+1`] = parent_hash
            
            # if the parent hash isn't in hashes, add it and traverse the
            # parent commit
            # else add the current commit to the parent as a child
            if parent_hash not in hashes :
                hashes.append( parent_hash )
                traverse( parent_hash, commit_hash )

            else :
                add_child( parent_hash, commit_hash )



# hash of the HEAD commit
head = check_output( ["git", "rev-parse", "HEAD"] ).strip( )
# add the head commit to hashes
hashes.append( head )
# start the git commit object traversal
traverse( head )

# add a commit type to each commit
for commit in metadata :
    # is it the head or tail commit
    hORt = False

    # if there are two or more children, it's a pre-branch/fork commit
    # if there are no children, it's a HEAD commit
    if "child2" in metadata[commit] :
        add_type( commit, "pre-branch/fork" )
    elif "child1" not in metadata[commit] :
        add_type( commit, "HEAD" )
        hORt = True

    # if there are two or more parents, it's a merge commit
    # if there are no parents, it's the tail commit
    # also no need to mark as the TAIL if it's the HEAD
    if "parent2" in metadata[commit] :
        add_type( commit, "merge" )
    elif "parent1" not in metadata[commit] and not hORt :
        add_type( commit, "TAIL" )
        hORt = True

    # if there are neither multiple parents nor multiple children
    # it's a normal commit
    if "parent2" not in metadata[commit] and \
        "child2" not in metadata[commit] and not hORt :
        add_type( commit, "commit" )

# check for code review
check_code_review( head )

print "Merges that have not been reviewed:"
not_reviewed_merges = metadata_lib.detect_unreviewed_merges(metadata)
if len(not_reviewed_merges) == 0:
	print "None"
else:
	for hashes in not_reviewed_merges:
		print hashes

# write metadata to a file in a json format
with open( "metadata.json", "w" ) as ofs :
    ofs.write( json.dumps( metadata, indent = 4 ) )
