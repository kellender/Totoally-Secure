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

def get_timestamps( commit_hash, merge ) :
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
    global metadata

    # text of the current git commit object
    # elements of current_commit are in the format "<label> <value>"
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]
        ).split( "\n" )
    
    # parents of the current commit
    parents = []
    merge = false

    # find all parents of the current commit
    for line in current_commit :
        if len( line ) != 0 :
            if line.startswith( "parent" ) :
                parents.append( line )
            elif line.startswith( "author" ) :
                metadata[current_hash]["author"] = line.split( " ", 1 )
            elif line.startswith( "committer" ) :
                metadata[current_hash]["merger"] = line.split( " ", 1 )
                merge = true

    get_timestamps( commit_hash, merge )

    if merge :
        metadata[commit_hash]["type"] = "merge"
    else :
        metadata[commit_hash]["type"] = "commit"

    if len( parents ) > 0 :
        for x in range( 1, len( parents )+1  ) :
            parent_hash = parents[x].split( )[1]

            metadata[commit_hash]["parent"+`x`] = parent_hash

            global hashes
            if parent_hash not in hashes :
                hashes.append( parent_hash )
                metadata[parent_hash]["child1"] = commit_hash
                traverse( parent_hash )
            else :
                add_child( parent_hash, commit_hash )


# hash of the HEAD commit
head = check_output( ["git", "rev-parse", "HEAD"] ).strip( )
hashes.append( head )
traverse( head )

