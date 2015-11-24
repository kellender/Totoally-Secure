from subprocess import check_output

# hashes of commits that were already touched
hashes = []

# metadata dictionary
metadata = {}

def add_child( parent_hash, child_hash ) :
    global metadata

    child_num = 2

    while true :
        child = "child"+`child_num`

        if metadata[parent_hash][child] :
            child_num += 1
        else :
            metadata[parent_hash][child] = child_hash
            break

def add_timestamps( commit_hash ) :
    global metadata

    metadata[commit_hash]["author_timestamp"] = check_output(
        ["git", "show", "-s", "--format=%ai", commit_hash]
        ).strip( )

    metadata[commit_hash]["commit_timestamp"] = check_output(
        ["git", "show", "-s", "--format=%ci", commit_hash]
        ).strip( )

# Recurse thought the tree until the initial commit is reached.
def traverse( commit_hash, child_hash = None ) :
    global metadata

    metadata[commit_hash] = {}

    if child_hash:
        metadata[commit_hash]["child1"] = child_hash

    # text of the current git commit object
    # elements of current_commit are in the format "<label> <value>"
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]
        ).split( "\n" )
    
    # parents of the current commit
    parents = []
    merge = False

    # find all parents of the current commit
    for line in current_commit :
        if len( line ) != 0 :
            if line.startswith( "parent" ) :
                parents.append( line )
            elif line.startswith( "author" ) :
                author = line.split( " ", 1 )[:line.find( ">" )+1]
                metadata[commit_hash]["author"] = author
            elif line.startswith( "committer" ) :
                committer = line.split( " ", 1 )[:line.find( ">" )+1]
                metadata[commit_hash]["committer"] = committer

    add_timestamps( commit_hash )

    if len( parents ) > 0 :
        for x in range( 0, len( parents )  ) :
            parent_hash = parents[x].split( )[1]

            metadata[commit_hash]["parent"+`x+1`] = parent_hash

            global hashes
            if parent_hash not in hashes :
                hashes.append( parent_hash )
                traverse( parent_hash, commit_hash )
            else :
                add_child( parent_hash, commit_hash )


# hash of the HEAD commit
head = check_output( ["git", "rev-parse", "HEAD"] ).strip( )
hashes.append( head )
traverse( head )

